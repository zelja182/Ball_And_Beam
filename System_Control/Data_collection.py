"""Collect ball-and-beam serial data and save it as CSV.

Arduino protocol (Ball_and_Beam_final_1.ino):
  - banner: "Ball and Beam v1 (PD)", "G = start, S = stop", header
  - send 'G' to start  -> board prints RUN then CSV rows
  - send 'S' to stop   -> board prints STOP
  - data: time_ms,distance_mm,beam_deg
"""

from __future__ import annotations

import csv
import os
import sys
import time
from datetime import datetime

import serial
import serial.tools.list_ports

PORT = "COM6"
BAUD = 115200
TIMEOUT_S = 1.0
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")


def list_ports() -> None:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return
    print("Available ports:")
    for p in ports:
        print(f"  {p.device}: {p.description}")


def open_arduino(port: str = PORT) -> serial.Serial:
    ser = serial.Serial(port=port, baudrate=BAUD, timeout=TIMEOUT_S)
    time.sleep(2.0)  # wait for board reset after opening the port
    return ser


def send_cmd(ser: serial.Serial, cmd: str) -> None:
    # Arduino reads one character (G/S) and discards the rest of the line.
    ser.write(f"{cmd[0]}\n".encode("ascii"))
    ser.flush()
    print(f"Sent '{cmd[0]}'")


def read_line(ser: serial.Serial) -> str:
    raw = ser.readline()
    if not raw:
        return ""
    return raw.decode("utf-8", errors="replace").strip()


def parse_data_line(line: str) -> tuple[int, int, float] | None:
    parts = line.split(",")
    if len(parts) != 3:
        return None
    try:
        time_ms = int(float(parts[0]))
        distance_mm = int(float(parts[1]))
        beam_deg = float(parts[2])
    except ValueError:
        return None
    return time_ms, distance_mm, beam_deg


def next_save_path() -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(SAVE_DIR, f"pid_run_{stamp}.csv")


def save_csv(path: str, rows: list[tuple[int, int, float]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["time_ms", "distance_mm", "beam_deg"])
        writer.writerows(rows)


def drain_banner(ser: serial.Serial) -> None:
    """Print whatever the board already sent (banner), without blocking."""
    deadline = time.time() + 0.5
    while time.time() < deadline:
        if not ser.in_waiting:
            time.sleep(0.05)
            continue
        line = read_line(ser)
        if line:
            print(line)


def collect_until_stop(ser: serial.Serial) -> list[tuple[int, int, float]]:
    rows: list[tuple[int, int, float]] = []
    try:
        while True:
            line = read_line(ser)
            if not line:
                continue

            if line == "STOP":
                print(line)
                break
            if (
                line in {"RUN", "Ball and Beam v1", "Ball and Beam v1 (PD)"}
                or line.startswith("G = start")
            ):
                print(line)
                continue
            if line.startswith("time_ms"):
                continue

            parsed = parse_data_line(line)
            if parsed is None:
                print(line)
                continue

            rows.append(parsed)
            time_ms, distance_mm, beam_deg = parsed
            print(f"{time_ms:8d}  {distance_mm:4d} mm  {beam_deg:7.2f} deg")
    except KeyboardInterrupt:
        print("\nStopping...")
        send_cmd(ser, "S")
        deadline = time.time() + 1.5
        while time.time() < deadline:
            line = read_line(ser)
            if not line:
                continue
            parsed = parse_data_line(line)
            if parsed is not None:
                rows.append(parsed)
            if line == "STOP":
                print(line)
                break
    return rows


def collect(ser: serial.Serial) -> list[tuple[int, int, float]]:
    print("Arduino connected. Waiting for banner...")
    drain_banner(ser)

    try:
        input("Place the ball, then press Enter to send G (start)... ")
    except KeyboardInterrupt:
        print("\nCancelled before start.")
        send_cmd(ser, "S")
        return []

    send_cmd(ser, "G")
    print("Running. Press Ctrl+C to send S (stop) and save.\n")
    return collect_until_stop(ser)


def main() -> int:
    list_ports()
    port = PORT
    if len(sys.argv) > 1:
        port = sys.argv[1]

    print(f"\nOpening {port} at {BAUD} baud...")
    try:
        ser = open_arduino(port)
    except serial.SerialException as exc:
        print(f"Could not open {port}: {exc}")
        return 1

    try:
        rows = collect(ser)
    finally:
        if ser.is_open:
            try:
                send_cmd(ser, "S")
            except Exception:
                pass
            ser.close()

    if not rows:
        print("No data rows collected.")
        return 0

    path = next_save_path()
    save_csv(path, rows)
    duration_s = rows[-1][0] / 1000.0
    print(f"Saved {len(rows)} samples ({duration_s:.1f} s) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

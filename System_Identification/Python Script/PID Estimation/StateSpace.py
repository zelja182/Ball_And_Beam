from scipy import signal

def sys_simulation(PIDsys):
    error = 0
    Xiz = 0
    Xi = 15
    Xservo = 0
    Xpid = 0
    output = [Xi]
    Servo_sys = signal.StateSpace()
    O_sys = signal.StateSpace()

    for t in range(1000):
        error= Xiz - Xi
        _, Xpid, _ = signal.lsim(system=PIDsys, U=error, T=t, X0=Xpid)
        _, Xservo, _ = signal.lsim(system=Servo_sys, U=Xpid, T=t, X0=Xpid)
        if Xservo > 90:
            Xservo = 90
        if Xservo < -90:
            Xservo = -90
        _, Xi, _ = signal.lsim(system=O_sys, U=Xservo, T=t, X0=Xi)
        output.append(Xi)

    return output


Kp = 1
Ki = 1
Kd = 1

PIDsys = signal.StateSpace()

    


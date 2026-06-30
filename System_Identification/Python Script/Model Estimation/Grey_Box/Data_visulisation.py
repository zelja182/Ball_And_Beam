"""
Grey-box model estimation results: load, visualize, and rank transfer functions.

Reads validation MSE data exported from MATLAB (Model.csv / Model.json),
ranks unique transfer functions by average validation error, and prints
the best candidates for further analysis or Simulink use.

Typical workflow:
    1. Export results from MATLAB to Model.json
    2. Run workaround() once to create Model.csv (if needed)
    3. Run run_print_top_models() to print the top N models
    4. Run make_new_table() if you also want to save avg/median/worst MSE to CSV
"""

import matplotlib.pyplot as plt
import pandas as pd

matlab_data_path = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Estimation_data/GreyBox/Model.json"

py_data_path = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Estimation_data/GreyBox/Model.csv"


def workaround():
    """
    Convert MATLAB JSON export to CSV for pandas analysis.

    Manual JSON cleanup is required before this works reliably:
        1. Open matlab_data_path
        2. Format JSON (e.g. online formatter)
        3. Replace ``"MSE": {`` with a blank line
        4. Replace ``},`` with ``,``
        5. Remove the trailing ``}``
        6. Format JSON again
        7. Run this function to write Model.csv
        8. Rename the first column to ``test_no`` if it has no header

    Writes:
        Model.csv at py_data_path
    """
    df = pd.read_json(matlab_data_path)
    df = df.T
    df.to_csv(py_data_path)


def show_plot():
    """
    Plot box and violin charts of validation MSE columns.

    Reads Model.csv, drops identifier columns (test_no, num, den), and
    displays the distribution of each mse_* column to spot outliers or
    poorly validated tests.

    Requires:
        Model.csv at py_data_path
    """
    df = pd.read_csv(py_data_path)

    df = df.drop(columns=['test_no', 'num', 'den'])

    plt.style.use('_mpl-gallery')

    _, ax = plt.subplots()
    ax.set_title("MSE Data Visualisation")
    ax.boxplot(df, widths=0.2, patch_artist=True,
               showmeans=False, showfliers=False,
               medianprops={"color": "white", "linewidth": 0.5},
               boxprops={"facecolor": "C0", "edgecolor": "white",
                         "linewidth": 0.5},
               whiskerprops={"color": "C0", "linewidth": 1.5},
               capprops={"color": "C0", "linewidth": 1.5})

    ax.violinplot(df, widths=0.5, showmeans=False, showmedians=False, showextrema=False)
    ax.set_xticklabels(df.columns)

    plt.show()


def prepare_ranked_models(columns_to_drop=None):
    """
    Load model table, compute MSE statistics, and rank unique transfer functions.

    Parameters
    ----------
    columns_to_drop : list[str], optional
        mse_* column names to exclude from ranking (e.g. bad validation runs).

    Returns
    -------
    df : pandas.DataFrame
        Full table with avg_mse, median_mse, worst_mse, and tf_key columns added.
    unique : pandas.DataFrame
        One row per unique transfer function (num + den), sorted by avg_mse.
    mse_cols : list[str]
        Validation MSE columns used for ranking.
    rank_cols : list[str]
        Column names used when printing ranked results.

    Raises
    ------
    ValueError
        If no mse_* columns remain after dropping requested columns.
    """
    columns_to_drop = columns_to_drop or []

    df = pd.read_csv(py_data_path)
    mse_cols = [
        col for col in df.columns
        if col.startswith("mse_") and col not in columns_to_drop
    ]
    if not mse_cols:
        raise ValueError("No MSE columns left after dropping requested columns.")

    df["avg_mse"] = df[mse_cols].mean(axis=1)
    df["median_mse"] = df[mse_cols].median(axis=1)
    df["worst_mse"] = df[mse_cols].max(axis=1)

    df["tf_key"] = df["num"].astype(str) + df["den"].astype(str)
    unique = df.drop_duplicates("tf_key").sort_values("avg_mse")

    rank_cols = ["test_no", "num", "den", "avg_mse", "median_mse", "worst_mse"]
    return df, unique, mse_cols, rank_cols


def print_ranking_summary(unique, mse_cols, columns_to_drop=None, total_models=None):
    """
    Print which validation columns were used and how many models were ranked.

    Parameters
    ----------
    unique : pandas.DataFrame
        Deduplicated models from prepare_ranked_models().
    mse_cols : list[str]
        Validation MSE columns included in ranking.
    columns_to_drop : list[str], optional
        Columns that were excluded from ranking.
    total_models : int, optional
        Total row count before deduplication. Defaults to len(unique).
    """
    columns_to_drop = columns_to_drop or []
    total_models = total_models if total_models is not None else len(unique)

    print(f"Using {len(mse_cols)} validation columns: {', '.join(mse_cols)}")
    if columns_to_drop:
        print(f"Dropped: {', '.join(columns_to_drop)}")
    print(f"{total_models} models -> {len(unique)} unique transfer functions\n")


def print_top_models(unique, rank_cols, top_n=5):
    """
    Print the best unique transfer functions (lowest avg_mse first).

    Parameters
    ----------
    unique : pandas.DataFrame
        Ranked unique models from prepare_ranked_models().
    rank_cols : list[str]
        Columns to display for each ranked model.
    top_n : int, optional
        Number of top models to print. Default is 5.

    Returns
    -------
    pandas.DataFrame
        Top N models with a 1-based rank index.
    """
    top_models = unique[rank_cols].head(top_n).reset_index(drop=True)
    top_models.index = top_models.index + 1
    top_models.index.name = "rank"

    print(f"=== Top {top_n} models (lowest avg_mse) ===")
    print(top_models.to_string())
    print()

    return top_models


def save_ranked_table(df):
    """
    Save the model table with computed MSE statistics back to CSV.

    Removes the internal tf_key column before saving.

    Parameters
    ----------
    df : pandas.DataFrame
        Table returned by prepare_ranked_models() (with tf_key column).

    Writes
    ------
    Model.csv at py_data_path (overwrites existing file).
    """
    df.drop(columns="tf_key").to_csv(py_data_path, index=False)


def make_new_table(columns_to_drop=None, top_n=5):
    """
    Rank grey-box models by validation MSE and print the top candidates.

    Main entry point. Loads Model.csv, ranks unique transfer functions by
    average validation MSE, prints a summary and the top N models, then
    saves the enriched table back to Model.csv.

    Parameters
    ----------
    columns_to_drop : list[str], optional
        mse_* columns to exclude from ranking.
    top_n : int, optional
        Number of best models to print. Default is 5.

    Returns
    -------
    pandas.DataFrame
        Top N ranked models (same table printed to stdout).
    """
    df, unique, mse_cols, rank_cols = prepare_ranked_models(columns_to_drop)
    print_ranking_summary(unique, mse_cols, columns_to_drop, total_models=len(df))
    top_models = print_top_models(unique, rank_cols, top_n=top_n)
    save_ranked_table(df)   # comment this out if you want to print the top N models only
    return top_models


if __name__ == "__main__":
    # workaround()
    # show_plot()
    make_new_table()

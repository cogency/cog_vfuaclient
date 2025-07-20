import argparse
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

def main(rawArgs=None):
    parser = argparse.ArgumentParser(description="OPC-UA live logger")

    parser.add_argument("--csv_file", type=str, required=True, help="CSV file")
    parser.add_argument("--cols", nargs="+", required=False, help="List of cols to plot")
    parser.add_argument("--figsize", nargs=2, type=int, default=[16,6], help="figure size")
    parser.add_argument("--resample", type=int, default=1, help="resample")
    parser.add_argument("--profile", type=str, default=None, help="volume,bed,flow")
    args = parser.parse_args(rawArgs)

    csv_file = Path(args.csv_file)

    df = pd.read_csv(csv_file, parse_dates=["Timestamp"])

    print(df.columns)

    if args.cols is None and args.profile is None:
        args.cols = ["vflow"]

    df2 = df[["Timestamp"]+args.cols]
    df2["TimeSeconds"] = (df2["Timestamp"] - df2["Timestamp"].iloc[0]).dt.total_seconds()
    df2 = df2.set_index("Timestamp").resample(f"{args.resample}s").mean().ffill()

    plt.figure(figsize=args.figsize)

    # Plot all variables (except timestamp)
    for col in args.cols:
        plt.plot(df2["TimeSeconds"], df2[col], label=col)

    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title(f"{csv_file.stem}")
    plt.legend()
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    main(['--csv_file',"voluflow_log_20250720_192623_223980.csv"])#,'--cols','mean_bed','mean_bed_left','mean_bed_right'])

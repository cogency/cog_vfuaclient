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
    parser.add_argument("--time_column", type=str, default='Timestamp', help="Name of time column")
    parser.add_argument("--time_format", type=str, default=None, help="Set time format profile")
    args = parser.parse_args(rawArgs)

    csv_file = Path(args.csv_file)

    timestampColumn = args.time_column

    def parse_unix_float(ts):
        return datetime.datetime.fromtimestamp(float(ts))

    if args.time_format=='unix_float':
        df = pd.read_csv(csv_file, parse_dates=[timestampColumn], date_parser=parse_unix_float)
    else:
        df = pd.read_csv(csv_file, parse_dates=[timestampColumn])

    print(df.columns)

    if args.cols is None and args.profile is None:
        args.cols = ["vflow"]

    df2 = df[[timestampColumn]+args.cols]
    df2["TimeSeconds"] = (df2[timestampColumn] - df2[timestampColumn].iloc[0]).dt.total_seconds()
    df2 = df2.set_index(timestampColumn).resample(f"{args.resample}s").mean().ffill()

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
    main(['--csv_file',"voluflow_log_20250720_195546_660427.csv", '--cols', 'vflow'])#,'--cols','mean_bed','mean_bed_left','mean_bed_right'])
    
    # f = r"C:\Cogency Dropbox\Project - DBM\DBM - Voluflow\phase7 - 2025 testfacility\results_20250617\results\20250617-141028-VoluflowMetric.csv"
    # f = r"C:\Cogency Dropbox\Project - DBM\DBM - Voluflow\phase7 - 2025 testfacility\results_20250617\results\20250617-143107-VoluflowMetric.csv"
    
    # main(['--csv_file', f, '--time_column', 'recorderTime', '--time_format', 'unix_float', '--resample', '10', '--cols', 'fields-mean_bed'])
    # main(['--csv_file', f, '--time_column', 'recorderTime', '--time_format', 'unix_float', '--resample', '1', '--cols', 'fields-vflow'])

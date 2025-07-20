import argparse
import datetime
import csv
import time

from pathlib import Path
from opcua import Client

def main(rawArgs=None):
    parser = argparse.ArgumentParser(description="OPC-UA live logger")

    parser.add_argument("--folder", type=str, default=None, help="Output CSV folder")
    #  parser.add_argument("--nodes", nargs="+", required=True, help="List of node IDs (e.g. ns=2;s=Temp)")
    parser.add_argument("--host", type=str, default="localhost", help="VoluFlow Camera IP")
    parser.add_argument("--port", type=int, default=4840, help="VoluFlow Camera Port")
    parser.add_argument("--poll_ms", type=int, default=1000, help="Polling interval in ms")
    parser.add_argument("--verbose", type=int, default=0, help="Print rows")

    args = parser.parse_args(rawArgs)

    url = f"opc.tcp://{args.host}:{args.port}"
    print(f"Connecting to {url}")

    client = Client(f"opc.tcp://{args.host}:{args.port}")
    client.connect()
    csv_file = None

    try:
        nodes = {}

        for nme in ["VoluflowMetric", "SensorMetric", "SystemMetric"]:
            root = client.get_node(f"ns=2;s={nme}")
            nodes.update({x.get_browse_name().Name: x for x in root.get_children()})

        recstamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        if args.folder is not None:
            outFile = Path(args.folder) / f"voluflow_log_{recstamp}.csv"
            outFile.parent.mkdir(parents=True, exist_ok=True)
        else:
            outFile = Path(f"voluflow_log_{recstamp}.csv")

        csv_file = open(outFile, "a", newline="")
        writer = csv.writer(csv_file)

        header = ["Timestamp"] + list(nodes.keys())
        writer.writerow(header)

        if args.verbose:
            print(header)
    
        print(f"recording to {outFile}...")

        while True:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            row = [ts]

            for node in nodes.values():
                try:
                    val = node.get_value()
                except:
                    val = None

                row.append(val)

            writer.writerow(row)
            csv_file.flush()  # ensure it’s written immediately

            if args.verbose:
                print(row)

            time.sleep(args.poll_ms//1000)

    except KeyboardInterrupt:
        print("\nLogging stopped.")

    finally:
        client.disconnect()

        if csv_file is not None:
            csv_file.close()

    print('exit')

if __name__=="__main__":
    main()


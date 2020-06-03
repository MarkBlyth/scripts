#!/usr/bin/env python3

import argparse
import pyabf
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(
        description="Visualise some neuron data from an abf file")
    parser.add_argument("filename", help="ABF file to open")
    parser.add_argument(
        "-s", "--sweep", help="Data sweep to visualise", default=0, type=int
    )
    parser.add_argument(
        "-c", "--channel", help="Channel to extract", default=0, type=int
    )
    parser.add_argument("-e", "--export", action="store_true")
    parser.add_argument(
        "-l", "--lower", help="Crop data to time interval [lower, upper]", type=float, default=0)
    parser.add_argument(
        "-u", "--upper", help="Crop data to time interval [lower, upper]", type=float, default=1)
    args = parser.parse_args()

    abf = pyabf.ABF(args.filename)
    abf.setSweep(args.sweep, args.channel)

    ts = abf.sweepX
    ys = abf.sweepY[np.logical_and(args.lower <= ts, ts <= args.upper)]
    ts = ts[np.logical_and(args.lower <= ts, ts <= args.upper)]

    if args.export:
        data_arr = np.array([ts, ys])
        infilename = args.filename.split(".")[0]
        outfilename = "{0}_channel_{1}_sweep_{2}.np".format(
            infilename, args.channel, args.sweep
        )
        with open(outfilename, "wb") as outfile:
            np.save(outfile, data_arr)
        return

    if args.sweep is None:
        print(abf)
    else:
        _, ax = plt.subplots()
        ax.plot(ts, ys)
        plt.show()


if __name__ == "__main__":
    main()

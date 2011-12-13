#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""rtk_helper.py: a tool to retrieve Kanji using Heisig ID ranges."""

import argparse, sys

def parse_args():
    ap = argparse.ArgumentParser(
        description="Finds Heisig kanji from a KANJIDIC database.  Outputs to "
        "stdout, sorted by Heisig index in ascending order.")
    ap.add_argument("kanjidic")
    ap.add_argument("from_index", type=int)
    ap.add_argument("to_index", type=int)
    return ap.parse_args()

def main():
    options = parse_args()
    if options.from_index > options.to_index:
        print >> sys.stderr, "from_index cannot be larger than to_index."
        sys.exit(1)
    with open(options.kanjidic) as infile:
        data = infile.read().decode("euc-jp")

    results = []
    for line in data.splitlines():
        # Skip comments.
        if line.startswith("#"):
            continue

        # Drop the glosses, if present.
        gloss_index = line.find("{")
        if gloss_index > -1:
            line = line[:gloss_index]

        # Grab the Heisig tag, if present.
        fields = line.split(" ")
        heisig = [f for f in fields if f.startswith("L")]
        if len(heisig) < 1:
            continue

        # Strip tag and convert to int.
        heisig_index = int(heisig[0][1:])

        if (options.from_index <= heisig_index) \
            and (heisig_index <= options.to_index):
            kanji = fields[0]
            results.append((heisig_index, kanji))

    results.sort(key=lambda x: x[0])
    for index, kanji in results:
        print kanji.encode("utf-8")

if __name__ == "__main__":
    main()

import argparse
from __init__ import *


# Handle command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="file to find itemsets on")
parser.add_argument("minsup", help="minimum support", type=int)
parser.add_argument("algorithm", help="frequent pattern mining algorithm", choices=["fpgrowth", "fpmax"])
parser.add_argument("--output", help="output file path (if not given, the output is printed to console)")
args = parser.parse_args()

# Read input data
itemsets = itemsets_from_file(args.filename) 

# Select algorithm
if args.algorithm == "fpgrowth":
    fis = frequent_itemsets(itemsets, args.minsup)
elif args.algorithm == "fpmax":
    fis = maximal_frequent_itemsets(itemsets, args.minsup)

# Generate output
if args.output:
    with open(args.output, "w") as fout:
        for itemset in fis:
            for i,item in enumerate(itemset):
                fout.write(str(item))
                if i < len(itemset)-1:
                    fout.write(" ")
            fout.write("\n")
else:
    for itemset in fis:
        print(" ".join(itemset))

# wdecoster
import numpy as np
import math
import sys


def getN50(readlengths):
    '''
    Get read N50.
    Based on https://github.com/PapenfussLab/Mungo/blob/master/bin/fasta_stats.py
    '''
    return readlengths[np.where(np.cumsum(readlengths) >= 0.5 * np.sum(readlengths))[0][0]]


def removeLengthOutliers(df, columnname):
    '''
    Remove records with length-outliers above 3 standard deviations from the median
    '''
    return df[df[columnname] < (np.median(df[columnname]) + 3 * np.std(df[columnname]))]


def aveQual(quals):
    '''
    Calculation function:
    Receive the integer quality scores of a read and return the average quality for that read
    First convert Phred scores to probabilities,
    calculate average error probability
    convert average back to Phred scale
    '''
    return -10 * math.log(sum([10**(q / -10) for q in quals]) / len(quals), 10)


def readstats(datadf):
    '''
    For an array of readlengths, return a dictionary containing:
    - the number of reads
    - the total number of bases sequenced
    - the median length
    - the mean length
    - the top 5 longest reads and their quality
    - the maximum average basecall quality
    - the fraction and number of reads above > Qx
    (use a set of cutoffs depending on the observed quality scores)
    - the number of active channels
    '''
    readlengths = np.array(datadf["lengths"])
    qualities = np.array(datadf["quals"])

    res = dict()
    if "runIDs" in datadf:
        res["runIDs"] = list(np.unique(datadf["runIDs"]))
    if "channelIDs" in datadf:
        res["ActiveChannels"] = np.unique(datadf["channelIDs"]).size
    res["NumberOfReads"] = readlengths.size
    if res["NumberOfReads"] < 10:
        return None
    res["TotalBases"] = np.sum(readlengths)
    res["MedianLength"] = np.median(readlengths)
    res["MeanLength"] = np.mean(readlengths)
    indices_top_L = np.argpartition(readlengths, -5)[-5:]
    res["MaxLengthsAndQ"] = [list(e)
                             for e in zip(
        list(readlengths[indices_top_L]),
        list(qualities[indices_top_L]))]
    indices_top_Q = np.argpartition(qualities, -5)[-5:]
    res["MaxQualsAndL"] = [list(e)
                           for e in zip(
        list(readlengths[indices_top_Q]),
        list(qualities[indices_top_Q]))]
    qualgroups = [q for q in range(5, 50, 5) if q < np.amax(qualities) + 5]
    res["QualGroups"] = dict()
    for q in qualgroups:
        numberAboveQ = np.sum(qualities > q)
        res["QualGroups"][q] = (numberAboveQ, numberAboveQ / res["NumberOfReads"])
    return res


def writeStats(datadf, outputfile):
    '''
    Call calculation function and write to file
    '''
    stat = readstats(datadf)
    if stat:
        if outputfile == 'stdout':
            output = sys.stdout
        else:
            output = open(outputfile, 'wt')
        print("Number of reads:\t{}\n".format(stat["NumberOfReads"]), file=output, end="")
        print("Total bases:\t{}\n".format(stat["TotalBases"]), file=output, end="")
        print("Median read length:\t{}\n".format(stat["MedianLength"]), file=output, end="")
        print("Mean read length:\t{}\n".format(round(stat["MeanLength"], 2)), file=output, end="")
        print("Readlength N50:\t{}\n".format(
            getN50(np.sort(datadf["lengths"]))), file=output, end="")
        print("\n", file=output, end="")
        print("Top 5 read lengths and their average basecall quality score:\n", file=output, end="")
        for length, qual in sorted(stat["MaxLengthsAndQ"], key=lambda x: x[0], reverse=True):
            print("Length: {}bp\tQ: {}\n".format(length, round(qual, 2)), file=output, end="")
        print("\n", file=output, end="")
        print("Top 5 average basecall quality scores and their read lengths:\n", file=output, end="")
        for length, qual in sorted(stat["MaxQualsAndL"], key=lambda x: x[1], reverse=True):
            print("Length: {}bp\tQ: {}\n".format(length, round(qual, 2)), file=output, end="")
        print("\n", file=output, end="")
        print("Number of reads and fraction above quality cutoffs:\n", file=output, end="")
        for q in sorted(stat["QualGroups"].keys()):
            print("Q{}:\t{}\t{}%\n".format(
                q, stat["QualGroups"][q][0], round(100 * stat["QualGroups"][q][1], 2)),
                file=output, end="")
        if "ActiveChannels" in stat:
            print("\nData produced using {} active channels.\n".format(
                stat["ActiveChannels"]), file=output, end="")
        if "runIDs" in stat:
            print("\nData was produced in run(s) with ID:\n{}".format(
                "\n".join(stat["runIDs"])), file=output, end="")
    else:
        sys.stderr.write("Number of reads too low for meaningful statistics.\n")

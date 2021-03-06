#!/usr/bin/env python

import os
import shutil
import re

from config import Dirs, Disks, Files
from utils import xdm, error, checkFilesEq


### Check functions

def checkRecordsByChecksum(infile):
    """check records by checksum"""
    with open(infile, "r") as f:
        for i, line in enumerate(f):
            l = line[:-1] if line[-1] == "\n" else line
            s = 0
            for c in l:
                s = (s + ord(c) - 48) % 80
            if s != 0:
                error("VAR Records",
                      "%s: Record %d checksum mismatch: %d != 0" % (
                          infile, i, s))


def checkRecordsByLen(infile, fixed=None):
    """check records by encoded length"""
    refline = "*".join(["".join([chr(c) for c in xrange(64, 127)])
                        for _ in xrange(4)])
    if fixed is None:
        with open(infile, "r") as f:
            records = f.readlines()
    else:
        with open(infile, "rb") as f:
            data = f.read()
            records = [data[i:i + fixed]
                       for i in xrange(0, len(data), fixed)]
    for i, line in enumerate(records):
        if fixed:
            l = line
            if len(l) != fixed:
                error("VAR Records",
                      "%s: Record %d length mismatch: %d != %d" % (
                          infile, i, len(l), fixed))
        else:
            l = line[:-1] if line[-1] == "\n" else line
        l = l.rstrip()
        s = "!" + refline[:len(l) - 2] + chr(i + 49) if len(l) > 1 else ""
        if l != s:
            error("VAR Records",
                  "%s: Record %i content mismatch" % (infile, i))


### Main test

def runtest():
    """extract VAR record files generated by DMWRVAR.xb"""

    # setup
    shutil.copyfile(Disks.recsdis, Disks.work)

    # read full-size records
    for reclen in [16, 127, 128, 129, 254, 255]:
        xdm(Disks.work, "-e", "F" + str(reclen), "-o", Files.output)
        checkRecordsByChecksum(Files.output)
    for reclen in [16, 126, 127, 128, 254, 255]:
        xdm(Disks.work, "-e", "V" + str(reclen), "-o", Files.output)
        checkRecordsByChecksum(Files.output)

    # read partially filled records
    for reclen in [64]:
        xdm(Disks.work, "-e", "F" + str(reclen) + "V", "-o", Files.output)
        checkRecordsByLen(Files.output, fixed=reclen)
    for recid in [
            "64V", "255V1", "255V2", "255V3", "255V4", "255V4", "255V5"
            ]:
        xdm(Disks.work, "-e", "V" + recid, "-o", Files.output)
        checkRecordsByLen(Files.output)

    # read special records
    xdm(Disks.work, "-e", "F10R", "-o", Files.output)
    checkFilesEq("VAR Records", Files.output,
                 os.path.join(Dirs.refs, "f10r.txt"), "DIS/FIX10")
    xdm(Disks.work, "-e", "V10R", "-o", Files.output)
    checkFilesEq("VAR Records", Files.output,
                 os.path.join(Dirs.refs, "v10r.txt"), "DIS/VAR10")

    # re-write extracted records and check
    for fn in [
            "V1", "V16", "V126", "V127", "V128", "V254", "V64V", "V255V1",
            "V255V2", "V255V3", "V255V4", "V255V5", "V10R", "F10R",
            "F1", "F16", "F127", "F128", "F129", "F254", "F255", "F64V"
            ]:
        rectype = "DIS/VAR" if fn[0] == "V" else "DIS/FIX"
        reclen = re.search("\d+", fn).group(0)
        fmt = rectype + reclen
        xdm(Disks.work, "-e", fn, "-o", Files.reference)
        xdm(Disks.work, "-a", Files.reference, "-n", "COPY", "-f", fmt)
        xdm(Disks.work, "-e", "COPY", "-o", Files.output)
        checkFilesEq("VAR Records", Files.output, Files.reference, fmt)

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Disks.work)


if __name__ == "__main__":
    runtest()

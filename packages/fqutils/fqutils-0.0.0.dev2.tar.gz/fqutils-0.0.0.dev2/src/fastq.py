#! /usr/bin/env python
#############################################################
#     File Name           :     fastq.py
#     Created By          :     Ye Chang
#     Creation Date       :     [2017-10-03 17:00]
#     Last Modified       :     [2017-10-05 20:19]
#     Description         :
#############################################################


class FASTQ:
    """read fastq file"""

    def __init__(self, filename):
        self.filename = filename

    def get_filetype(self):
        """detect file type"""
        if self.filename.endswith(".gz"):
            return "Gzip"
        elif self.filename.endswith("fq") or self.filename.endswith("fastq"):
            return "plain file"
        return "Noooo"

    def read(self):
        """generator for reading"""
        ids = set('@' + x for x in open(self.filename))
        print(ids)
        with open(self.filename, "r") as f:
            for l in f:
                yield l

import collections
import gzip
import os
import sys
import re
from eta import ETA


class FASTARead(collections.namedtuple('FASTARecord', 'name comment seq')):
    def __repr__(self):
        if self.comment:
            return '>%s %s\n%s\n' % (self.name, self.comment, self.seq)
        return '>%s\n%s\n' % (self.name, self.seq)

    def subseq(self, start, end, comment=None):
        if self.comment:
            comment = '%s %s' % (self.comment, comment)

        return FASTARead(self.name, comment, self.seq[start:end])

    def clone(self, name=None, comment=None, seq=None):
        n = name if name else self.name
        c = comment if comment else self.comment
        s = seq if seq else self.seq

        return FASTARead(n, c, s)

    def write(self, out):
        out.write(repr(self))



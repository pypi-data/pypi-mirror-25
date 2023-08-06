# from collections import namedtuple
from os.path import basename, splitext

import h5py
import numpy as np


class Group:
    def __init__(self, filename):
        self.filename = filename
        self.basename = basename(splitext(filename)[0])
        self.f = h5py.File(filename, 'a')


#    def fields_view(self, arr, fields):
#        dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
#        return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)

    @property
    def samples(self):
        try:
            return self.f["samples"][:]
        except KeyError:
            self.f["samples"] = np.empty([0], dtype='S7')
            return self.f["samples"][:]

    @samples.setter
    def samples(self, value):
        if "samples" in self.f:
            del self.f["samples"]
        self.f["samples"] = value

    def append(self, sample):
        if(type(sample) == str):
            sample = bytes(sample, "utf-8")
        if(type(sample) == list):
            sample = [bytes(s, "utf-8") for s in sample]
        new_samples = np.append(self.samples, sample)
        self.samples = new_samples

    def remove(self, sample):
        if(type(sample) == str):
            sample = bytes(sample, "utf-8")
        try:
            index = np.nonzero(self.samples == sample)[0][0]
            new_samples = np.delete(self.samples, index)
            self.samples = new_samples
            return True
        except IndexError:
            return False

    def chromosomes(self):
        return [c for c in self.f["snps"]]

    def variants(self, chrom):
        return self.f[chrom]["variants"][:]

    def __repr__(self):
        return self.basename

    def __lt__(self, other):
        return self.basename < other.basename

# from collections import namedtuple
from os.path import basename, splitext

import numpy as np
from numpy.lib.recfunctions import merge_arrays
import h5py


class Sample:
    def __init__(self, filename):
        self.filename = filename
        self.basename = basename(splitext(filename)[0])
        self.samplename = splitext(self.basename)[0]
        self.f = h5py.File(filename, 'r')

    def __meta__(self, path, name, default=b''):
        p = self.f
        if path:
            p = p[path]

        value = p.attrs.get(name, default)
        if type(value) == int:
            return value
        else:
            return value.decode()

    @property
    def disease(self):
        return self.__meta__("", "disease")

    @property
    def capturekit_coverage(self):
        return float(self.__meta__("", "exome_sequencing_capture_kit_coverage",
                                   0))

    @property
    def chromosomes(self):
        return list(self.f.keys())

    def readcount(self, chrom):
        return int(self.__meta__(chrom, "exome_sequencing_readcount", 0))

    def duplication_rate(self):
        return float(self.__meta__("",
                                   "exome_sequencing_duplication_percentage",
                                   0))

    def capturekit_coverage_greater(self, x):
        return float(self.__meta__("", "exome_coverage_greater_{x}".format(x=x), 0))

    def examined_pairs(self):
        return int(self.__meta__("", "exome_sequencing_examined_pairs", 0))

    def unmapped_reads(self):
        return int(self.__meta__("", "exome_sequencing_unmapped_reads", 0))

    def fields_view(self, arr, fields):
        dtype2 = np.dtype({name: arr.dtype.fields[name] for name in fields})
        return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)

    def position_to_key(self, pos):
        return (pos << 4)

    def encode_keys(self, chrom, variants):
        '''decode the key and append fields'''
        keys = variants["key"]
        positions = keys >> 4
        mask = (1 << 4) - 1
        types = np.bitwise_and(keys, mask) >> 1
        mask = 1
        het = np.bitwise_and(keys, mask)
        chroms = np.repeat(chrom, len(keys))
        m = merge_arrays((variants, chroms, positions, types, het),
                         flatten=True)
        m.dtype.names = list(variants.dtype.names) + ["chrom", "position",
                                                      "typ", "het"]
        return m
#        return append_fields(variants, ("chrom", "position", "typ", "het"),
#                             (chroms, positions, types, het))

    def structural(self,
                   chrom,
                   typ=None,
                   minlength=20,
                   maxlength=float('inf'),
                   fields=["start", "end", "typ", "qual", "length", "gene_id"],
                   ):

        filtered_values = []
        if chrom in self.f and "structural" in self.f[chrom]:
                values = self.f[chrom]["structural"][:]

                if typ:
                    filter_crit = True
                    bit_typ = 0
                    for t in typ:
                        bit_typ += 2**t
                    filter_crit &= (2**values["typ"] & bit_typ) > 0
                    filter_crit &= (values["length"]) > minlength
                    filter_crit &= (values["length"]) < maxlength
                    filtered_values = values[filter_crit]
                    filtered_values = self.fields_view(filtered_values, fields)
                    filtered_values = np.unique(filtered_values)

        return filtered_values, self.samplename

    def keys(self, chrom):
        if not (chrom in self.f and "variant_keys" in self.f[chrom]):
            return np.array([], dtype=np.int64)
        return self.f[chrom]["variant_keys"][:]

    def has_variants(self, chrom, start, stop):
        start_index, stop_index = np.searchsorted(self.f[chrom]
                                                  ["variant_keys"],
                                                  (self.position_to_key(start),
                                                   self.position_to_key(stop))
                                                  )
        return start_index < stop_index

    def transcripts(self, chrom, start, stop):
        return self.f[chrom]["variants_transcripts"][start:stop]

    def variants(self,
                 chrom,
                 min_qual=0,
                 effects=None,
                 het=None,
                 dbsnp="None",
                 unique=True,
                 genes=[],
                 fields=["key", "qual", "ref"],
                 start=-1,
                 stop=-1,
                 decodekey=False,
                 min_alt_mapping_qual=0,
                 ):

        if chrom not in self.f:
            return None

        values = self.f[chrom]["variants"][:]

        if start > -1 and stop > -1:
            start_index, stop_index = np.searchsorted(
                values["key"],
                (self.position_to_key(start), self.position_to_key(stop)))
            values = values[start_index:stop_index]

        # TODO: db option

        if values.shape[0] == 0:
            random_chr = list(self.f.keys())[0]
            dtype_1 = self.f[random_chr]["variants"][:].dtype
            empty_data = np.array([], dtype=dtype_1)
            if len(fields):
                return self.fields_view(empty_data, fields)
            return empty_data

        filter_crit = np.ones(len(values), dtype=np.bool)

        # filter criterias

        if dbsnp == "all":
            filter_crit &= values["rsid"] == 0

        if dbsnp == "all_without_precious":
            filter_crit &= np.logical_or(values["rsid"] == 0,
                                         values["precious"])

        if dbsnp == "common":
            filter_crit &= np.logical_or(values["rsid"] == 0,
                                         np.logical_not(values["common"]))

        if dbsnp == "common_without_precious":
            filter_crit &= np.logical_or(values["rsid"] == 0,
                                         np.logical_not(values["common"]),
                                         values["precious"])
            # select variants, that has no precious flag by dbsnp

        if min_qual:
            filter_crit &= values["qual"] > min_qual

        if min_alt_mapping_qual:
            filter_crit &= values["mq"] > min_alt_mapping_qual

        if effects:
            filter_crit &= (values["effect"] & effects) > 0

        if het is not None:
            filter_crit &= (values["key"] & 1) == het

        if len(genes):
            transcript_values = self.f[chrom]["variants_transcripts"][:]
            filter_transcripts = np.in1d(transcript_values["gene_id"],
                                         np.array(genes))
            valid_variants = \
                transcript_values[filter_transcripts]["variant_id"]
            valid_zeros = np.zeros(len(values), dtype=bool)
            valid_zeros[valid_variants] = True
            filter_crit &= valid_zeros

        if len(fields) > 0:
            filtered_values = self.fields_view(values[filter_crit], fields)
        else:
            filtered_values = values[filter_crit]

        if unique:
            filtered_values = np.unique(filtered_values)

        # if decodekeys is True, decode all keys and append chrom, position,
        # typ and het to the returned data, which is very expensive for huge
        # lists
        if decodekey:
            filtered_values = self.encode_keys(chrom, filtered_values)

        return filtered_values

    def __repr__(self):
        return self.basename

    def __lt__(self, other):
        return self.basename < other.basename

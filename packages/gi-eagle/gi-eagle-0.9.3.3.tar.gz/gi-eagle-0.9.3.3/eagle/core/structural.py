import argparse

import numpy as np

from eagle.core.wrap.sample import Sample


def main(args):
    case_name = args.case[0]
    run(case_name)
    # out(run(case_name))


def run(cases, chromosomes, insertion, inversion,
        deletion, minlength, maxlength):
    typs = []
    if deletion:
        typs.append(5)
    if insertion:
        typs.append(6)
    if inversion:
        typs.append(7)

    cases = [Sample(c) for c in cases]
    variants = []
    for case in cases:
        if not chromosomes:
            chromosomes = case.chromosomes
        for chrom in chromosomes:
            values, samplename = case.structural(chrom, typ=typs,
                                                 minlength=minlength,
                                                 maxlength=maxlength)
            variants += [dict([("chrom", chrom)] + [("sample", samplename)] +
                              list(zip(values.dtype.names, x)))
                         for x in values]
    variants = parse_types(variants)
    return variants


def parse_types(variants):
    for variant in variants:
        variant['typ'] = get_typ(variant['typ'])
        for key in variant:
            if isinstance(variant[key], np.float32):
                variant[key] = float(variant[key])
            elif issubclass(type(variant[key]), np.integer):
                variant[key] = int(variant[key])
            elif isinstance(variant[key], np.bool_):
                variant[key] = bool(variant[key])
            elif isinstance(variant[key], np.bytes_):
                variant[key] = variant[key].decode()
    return variants


def get_typ(typ):
    if typ == 5:
        return "DEL"
    elif typ == 6:
        return "INS"
    elif typ == 7:
        return "INV"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", nargs=1)
    args = parser.parse_args()
    main(args)

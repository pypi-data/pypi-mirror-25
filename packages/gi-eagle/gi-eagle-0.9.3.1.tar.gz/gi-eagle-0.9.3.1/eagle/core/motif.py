import argparse
from collections import Counter
from itertools import zip_longest
import os

import h5py
from matplotlib.font_manager import FontProperties
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main(cases, controls, output):
    c = Counter()
    for case, control in list(zip_longest(cases, controls)):
        f_case = h5py.File(case, 'r') if case else []
        f_control = h5py.File(control, 'r') if control else []
        for chrom in f_case:
            chrom_case = f_case[chrom]
            if chrom in f_control:
                chrom_control = f_control[chrom]
            else:
                chrom_control = None

            count_contexts(chrom_case, chrom_control, c)
    contexts, alterations, counts = sort_counts(c)
    sum_counts = sum(counts)
    if sum_counts != 0:
        normalized_counts = [count/sum_counts for count in counts]
    else:
        normalized_counts = counts
    plot_data(contexts, alterations, normalized_counts, output)


def plot_data(contexts, alterations, counts, output):
    font = FontProperties()
    font.set_family('monospace')
    font.set_size(5)
    sns.set_style("whitegrid")
    max_count = max(counts)
    plt.ylim([0, max_count*1.03])
    x_values = [i for i in range(len(counts))]
    color_palette = sns.color_palette("husl", 6)
    expanded_palette = list(zip(*([color_palette]*16)))
    colors = [item for sublist in expanded_palette for item in sublist]
    # barlist = sns.barplot(x=x_values, y=counts, palette=colors, linewidth=0)
    plt.xticks(x_values, contexts, rotation=90, fontproperties=font)
    for i in range(0, 96, 16):
        plt.gca().add_patch(patches.Rectangle((i-0.5, max_count+0.0005), 16,
                                              0.001, facecolor=colors[i],
                                              linewidth=0))
        alteration = contexts[i][1]+'>'+alterations[i]
        plt.text(i+6.5, max_count+0.00065, alteration, fontproperties=font)
    if not os.path.exists("/tmp/eagle"):
        os.mkdir("/tmp/eagle")
    plt.savefig('/tmp/eagle/'+str(output)+'.png', dpi=200)


def sort_counts(counts):
    base_to_index = {"A": 0, "C": 1, "G": 2, "T": 3}
    contexts = []
    alterations = []
    total_counts = []
    for i in ['C', 'T']:
        alt = ['A', 'C', 'G', 'T']
        alt.remove(i)
        for a in alt:
            for l in ['A', 'C', 'G', 'T']:
                for r in ['A', 'C', 'G', 'T']:
                    context = l + i + r
                    contexts.append(context)
                    alterations.append(a)
                    rev_context, rev_a = reverse_complement(context, a)
                    count = counts[(base_to_index[a], context.encode())] + \
                        counts[(base_to_index[rev_a], rev_context)]
                    total_counts.append(count)
    return contexts, alterations, total_counts


def count_contexts(chrom_case, chrom_control, counter):
    unique_variants = np.unique(chrom_case['variants']['key', 'context'])
    keys_case = unique_variants['key']
    context = np.core.defchararray.upper(unique_variants['context'])
    alt = keys_case.astype(np.int64) >> 1 & 7

    if chrom_control:
        keys_control = chrom_control['variants']['key']
        somatic = np.in1d(keys_case, keys_control, invert=True)
        context = context[somatic]
        alt = alt[somatic]

    counter += Counter(zip(alt, context))


def reverse_complement(context, mutation):
    base_complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    mutation = base_complements[mutation]
    complement = [base_complements[base] for base in context]
    reverse_complement = ''.join(complement)[::-1]
    return reverse_complement.encode(), mutation


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("case")
    parser.add_argument("control")
    args = parser.parse_args()
    main(args.case, args.control)

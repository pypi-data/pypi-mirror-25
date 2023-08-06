import glob
import os
import uuid

import h5py

from eagle.application import app
from eagle.core.wrap.sample import Sample

SNP_PATH = app.config["SNP_PATH"]
GROUP_PATH = app.config["GROUP_PATH"]
BAM_PATH = app.config["BAM_PATH"]


def __h5files__(path):
    '''return sorted h5 files in a path'''
    files = [f.rsplit("/", 1)[-1][:-3]
             for f in glob.iglob(os.path.join(path, "*.h5"))]
    return sorted(files)


def __txtfiles__(path):
    '''return sorted txt files in a path'''
    files = [f.rsplit("/", 1)[-1][:-4]
             for f in glob.iglob(os.path.join(path, "*.txt"))]
    return sorted(files)


def available_samples(project_filter=True):
    '''return all available sample names'''
    return __h5files__(SNP_PATH)


def available_sample_objects(project_filter=True):
    '''return all available samples as Sample objects'''
    return [Sample(sample_filename(s)) for s in available_samples()]


def available_group_samples(group):
    samples = open(group).readline().split()
    return samples


def available_groups(project_filter=True):
    '''return all available groups'''
    return __txtfiles__(GROUP_PATH)


def sample_filename(sample):
    '''return the filename to a given sample'''
    return os.path.join(SNP_PATH, sample + ".h5")


def group_filename(group):
    '''return the filename to a given sample'''
    return os.path.join(GROUP_PATH, group + ".txt")


def bam_filename(sample):
    '''return the bam filename to a given sample'''
    return os.path.join(BAM_PATH, sample + ".bam")


def available_chromosomes():
    '''return the chromosomes of all samples'''
    chromosomes = []
    for sample_name in available_samples():
        sample_path = sample_filename(sample_name)
        sample = h5py.File(sample_path, 'r')
        for chrom in sample:
            if chrom not in chromosomes:
                chromosomes.append(chrom)
    return chromosomes


class Query():
    pass


def parse_request(request):
    q = Query()
    q.case = request.form.getlist('case')
    q.chromosomes = request.form.getlist('chromosomes')
    q.control = request.form.getlist('control')
    q.effects = sum(request.form.getlist('effects', type=int))
    q.min_qual = request.form.get('minquality', type=int)
    q.min_mapping_qual = request.form.get('minmappingquality', type=int)
    q.min_samples_per_gene = request.form.get('samplespergene', type=int)
    q.min_samples_per_variant = request.form.get('samplespervariant', type=int)
    q.min_variants_per_gene = request.form.get('variantspergene', type=int)
    q.min_variant_length = request.form.get('minlength', type=int)
    q.max_variant_length = request.form.get('maxlength', type=float)
    q.search_all = request.form.get('searchall', type=bool)
    q.case_groups = request.form.getlist('case_group')
    q.control_groups = request.form.getlist('control_group')
    q.usehg19 = request.form.get('usehg19', type=bool) is True
    q.ignore_heterozygosity = \
        request.form.get('ignore_heterozygosity', type=bool) is True
    q.insertion = request.form.get('insertion', type=bool) is True
    q.inversion = request.form.get('invariant', type=bool) is True
    q.deletion = request.form.get('deletion', type=bool) is True
    q.dbsnp = request.form.get("dbsnp")
    q.uuid = uuid.uuid4()

    # genes
    genes = request.form.getlist('genes')
    if genes and not q.search_all:
        q.genes = map(lambda x: x.strip(),
                      request.form.getlist('genes')[0].split("\n"))
    else:
        q.genes = []

    q.index = request.form.get('sample')
    q.parent1 = request.form.get('parent1')
    q.parent2 = request.form.get('parent2')

    return q

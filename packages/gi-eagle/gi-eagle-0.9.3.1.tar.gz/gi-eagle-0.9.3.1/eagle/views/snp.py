"""
SNP query page
"""
from base64 import b64encode
from datetime import date

from flask import render_template, request

from eagle.application import app
from eagle.core import snps
from eagle.core.effectenum import EffectNames, exon_effects
from eagle.views.common import sample_filename, group_filename,\
    available_groups, available_sample_objects, parse_request,\
    available_group_samples


@app.template_filter()
def diseases(samples):
    '''return the disease of a sample'''
    return set([sample.disease for sample in samples])


def samples_by_diseases(diseases):
    '''return all samples affected by one of the given diseases'''
    samples = [sample_filename(s.basename) for s in available_sample_objects()
               if '@'+s.disease in diseases]
    for disease in diseases:
        if not disease.startswith('@'):
            file_path = group_filename(disease)
            group_samples = available_group_samples(file_path)
            samples += [sample_filename(sample) for sample in group_samples]
    return samples


def genvcf(results, q):
    vcf_string = """##fileformat=VCFv4.0
##fileDate=%s
##source=eagle
##reference=%s
##phasing=partial
##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=.,Type=Float,Description="Allele Frequency">
##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
##FILTER=<ID=q10,Description="Quality below 10">
##FILTER=<ID=s50,Description="Less than 50%% of samples have data">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t""" % \
        (date.today().strftime('%Y%m%d'), "hg19" if q.usehg19 else "hg38")
    vcf_string += "\t".join(q.case)
    vcf_string += "\n"
    rows = []
    for r in results:
        row = [str(s) for s in [r["chrom"][3:],
               r["position"],
               ".",
               r["ref"] if r["ref"] in "ACGT" else "N",
               "ACGT"[r["typ"]] if r["typ"] < 4 else ".",
               r["maxqual"],
               ".",
               ".",
               "GT:GQ"]]
        for sample in q.case:
            GT_string = "./."
            GQ_string = "."
            if sample in r['samples']:
                GT_string = "0/1" if r['heterozygot'][sample] \
                    else "1/1" if r["typ"] < 4 else "0/0"
                GQ_string = str(r['qual'][sample])
            row.append("%s:%s" % (GT_string, GQ_string))
        rows.append("\t".join(row))
    vcf_string += "\n".join(rows)
    # vcf_string += results[0]
    return vcf_string


@app.route('/snp', methods=['GET', 'POST'])
def snp():
    if request.method != 'POST':
        return render_template(
            "snp_query.html",
            available_samples=available_sample_objects(),
            available_groups=available_groups(),
            EffectNames=EffectNames,
            exon_effects=exon_effects,
        )

    # parse the request parameters
    q = parse_request(request)

    # building case filenames
    cases = [sample_filename(c) for c in q.case]
    cases.extend(samples_by_diseases(q.case_groups))
    cases = set(cases)

    # building control filenames
    controls = [sample_filename(c) for c in q.control]
    controls.extend(samples_by_diseases(q.control_groups))
    controls = set(controls)

    results = snps.run(
        cases,
        controls,
        q.effects,
        q.min_qual,
        q.min_samples_per_gene,
        q.min_samples_per_variant,
        q.min_variants_per_gene,
        q.genes,
        ignore_heterozygosity=q.ignore_heterozygosity,
        usehg19=q.usehg19,
        dbsnp=q.dbsnp,
        min_alt_mapping_qual=q.min_mapping_qual,
    )

    vcf = b64encode(genvcf(results, q).encode()).decode()

    return render_template('snp_results.html', results=results,
                           vcf=vcf, query=q)

from pyliftover import LiftOver

from eagle.application import app
from eagle.core.effectenum import EffectNames

lo = LiftOver("hg38", "hg19")


def liftover(chromosome, position, usehg19):
    if usehg19:
        l = lo.convert_coordinate("chr" + chromosome[3:], int(position))
        if not l:
            return ("", 0)
        return l[0][0:2]
    else:
        return (chromosome, position)


app.jinja_env.globals.update(liftover=liftover)


@app.template_filter()
def u2b(s):
    '''converts a unicode string to a byte array'''
    return bytes(s, "utf-8")


@app.template_filter()
def b2u(s):
    '''converts a byte array to a unicode string'''
    return str(s, "utf-8").strip()


@app.template_filter()
def effects(s):
    '''generate effects string from effect bitvector'''
    ret = [EffectNames[b] for b in EffectNames if b & s > 0]
    return ", ".join(ret)


_heterozygosity_strings = {1: "het", 2: "hom", 3: "both"}


@app.template_filter()
def heterozygosity(h):
    '''return the string for a heterozygosity "enum"'''
    return _heterozygosity_strings.get(h, "error")


@app.template_filter()
def single_element(s):
    '''return an element from an iteratable'''
    return next(iter(s))


@app.template_filter()
def remove_chr(s):
    '''return lowercase s'''
    if s.upper().startswith("CHR"):
        return s[3:]
    return s


@app.template_filter()
def rsid(x):
    if x:
        return "rs{x}".format(x=x)
    return ""

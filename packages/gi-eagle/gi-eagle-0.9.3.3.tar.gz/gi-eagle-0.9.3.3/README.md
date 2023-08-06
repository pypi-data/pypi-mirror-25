# Eagle #

The exome analysis graphical environment (Eagle) is a webbased user interface for exonic data analysis.

## Installation ##

### by pip ###

As long as no conda package is build, using pip is the easiest way to install Eagle

```
pip install gi-eagle
```

### by setup.py ###

You can install Eagle by running setup.py from a cloned repository

```
git clone git@bitbucket.org:christopherschroeder/eagle.git
cd eagle
python setup.py install
```

## Create the data-files ##

Instead of a central database Eagle stores the genetic information in structured h5 files. These files are created on [SnpEff and SnpSift](http://snpeff.sourceforge.net) annotated [vcfs](http://www.internationalgenome.org/wiki/Analysis/vcf4.0/) and created as follows. As an example we assume having a vcf files named *example.vcf*, based on hg38 and containing the two samples *sampleA* and *sampleB*. Furthermore we assume a [dbSNP](https://www.ncbi.nlm.nih.gov/projects/SNP/) vcf file stored as *150.vcf.gz* ([download](ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b150_GRCh38p7/VCF/All_20170710.vcf.gz)).


Step 1. Annotate the vcf file
```
snpeff -noStats -t hg38 example.vcf | snpsift annotate -tabix 150.vcf.gz - > example.annotated.vcf
```

Step 2. Use eagle to convert the vcf file
```
eagle convert --samples sampleA sampleB example.annotated.vcf data
```
This creates two sample specific data files *data/sampleA.h5* and *data/sampleB.h5*.



## Create the config ##
Eagle requires a configuration file to run, containing path information to the previously created data files and to corresponding bam files. The config syntax follows the python [supported INI file structure](https://docs.python.org/3.6/library/configparser.html#supported-ini-file-structure) with a *pathes* and a *reference* section.
Example config file *config.cfg*
```
[pathes]
snp: /vol/home/me/data/h5
bam: /vol/home/me/data/bam
group: /vol/home/me/data/groups

[reference]
version: hg38
```
The *snp* key contains the path to the data files, *bam* key the path to the corresponding bam files and *group* the path to a directory where Eagle stores custom sample groups. Please note that Eagle requires identical file basenames to match bam and h5, e.g. *sampleA.bam* and *sampleA.h5*.

## Running ##

The interface is launched by
```
eagle interface --config config.cfg
```
with a given previously created *cfg* file. Per default the local webserver is running on port 8000 and is accessed under *http://127.0.0.1:8000* or *http://localhost:8000*, if the system's defaults are not customized.

## Licence ##

Copyright (c) 2017 Christopher Schr�der <christopher.schroeder@tu-dortmund.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Who do I talk to? ##

For detailled information about my person please go to [https://christopherschroeder.bitbucket.io](https://christopherschroeder.bitbucket.io)

# janis-workshops
This repository contains workshops for the [Janis](https://github.com/PMCC-BioinformaticsCore/janis) pipeline framework.

1. Introduction to Janis
2. Building a basic bioinformatics workflow
3. [Wrapping a new CommandTool](https://github.com/PMCC-BioinformaticsCore/janis-workshops/tree/master/workshop3)
4. Advanced workflow concepts

You can find more documentation about Janis here: https://janis.readthedocs.io/en/latest/

## Quickstart

You can install Janis using pip:

```bash
pip3 install janis-pipelines[bioinformatics]
```

## Workshop material

These guides and notes are designed to assist a participant attending a workshop and can't be seen as a replacement to a physical session. The guides and data (where available) are published under GPL3.

Every piece of data should be referenced, please [raise an issue](https://github.com/PMCC-BioinformaticsCore/janis-workshops/issues/new) if that's not the case.


## Data

The BRCA1 samples are sourced from the [SAMN03492678 study](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SAMN03492678) of [NA12878](ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/) of the Genome in a Bottle project:

> - BRCA1_30X: gene BRCA1 from the WGS_30X:
> - Calcualted coverage: 33.6X
> - Location: 17:43044295-43125483 (from NCBI)
> - Extract reads in 17:43044045-43125733 (+- 250bp)

### Reference data

Processing and preprocessing of the NA12878 data used a modified HG38 reference genome with renamed contigs.

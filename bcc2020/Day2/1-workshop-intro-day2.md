# BCC2020 EAST - Janis Workshop (2.1)
## Produce a portable germline variant-calling pipeline in CWL and WDL using Janis and GATK

Welcome to BCC2020 East Janis workshop (Day 2). This workshop is split into 2 parts where we will go through an example of using Janis to build a genomic variant-calling pipeline. 

Workflows from this workshop are adopted from the following GATK (Broad Institute)'s WDL pipelines with modifications to simplify the tasks for the purpose of this workshop. 
- https://github.com/gatk-workflows/gatk4-data-processing
- https://github.com/gatk-workflows/gatk4-germline-snps-indels

The main goal of this workshop is to introduce Janis for building portable pipeline. We will be using small test datasets for demonstrations. Please note that some of the bioinformatics details, such as tools' parameters, genome references and databases, might not be complete. Please consider reviewing the pipeline details at the end of this workshop if you are planning to use this on other samples.  

## Important Links:

- Janis Documentation: https://janis.readthedocs.io/en/latest
- Janis GitHub: https://github.com/PMCC-BioinformaticsCore/janis
- This workshop GitHub: https://github.com/PMCC-BioinformaticsCore/janis-workshops

## Workshop Outline

### ~Day 1~
- ~Introduction to Janis~
    - ~Installing and setting up Janis environment~
    - ~Running a simple test workflow ~
- ~Building a workflow to align sample to reference genome~
    - ~Understanding logs and troubleshooting for errors~
- ~Exercise: Extend alignment workflow to complete the data processing workflow~
- ~Q&A~

### Day 2

- Recap of Day 1
- Adding new tools definition in Janis (GATK HaplotypeCaller)
- Exercise: Adding more tools (BQSR) to complete the germline variant calling pipeline
- Using translated CWL & WDL pipelines on other platform 
- Q&A 


## Requirements:

- Python 3.6+
- Docker

## Workshop environment:

- Single instance setup (local compute / single cloud VM) 


## Getting started

We will start with downloading all the test data required for this workshop. For consistency, we will use the same directory called `janis-bcc2020`.

```
mkdir janis-bcc2020 && cd janis-bcc2020
wget -q -O- "https://github.com/PMCC-BioinformaticsCore/janis-workshops/raw/master/janis-data.tar" | tar -xz
```

**If you have missed the first day of workshop yesterday**, you can download all the necessary workflows that we will be building up upon from the [solution](https://github.com/PMCC-BioinformaticsCore/janis-workshops/tree/bcc-2020/bcc2020/solution) page. 
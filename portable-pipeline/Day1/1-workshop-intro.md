# Janis Workshop (1.1)
## Produce a portable germline variant-calling pipeline in CWL and WDL using Janis and GATK

Welcome to Janis workshop. This is a 2-part workshop where we will use Janis to build a genomic variant-calling pipeline. 

Workflows from this workshop are adopted from the following GATK (Broad Institute)'s WDL pipelines with modifications to simplify the tasks for the purpose of this workshop. 

- https://github.com/gatk-workflows/gatk4-data-processing
- https://github.com/gatk-workflows/gatk4-germline-snps-indels

The goal of this workshop is to introduce Janis for building portable pipelines. We build a toy variant-caller that works for small data sets. **Please note that the pipeline produced by this workshop should only be used as a guide, and is NOT for production usage**. Please consider reviewing the pipeline details such as tools' parameters, genome references and databases at the end of this workshop if you are intend to use this for other samples.  

## Important Links:

- Janis Documentation: https://janis.readthedocs.io/en/latest
- Janis GitHub: https://github.com/PMCC-BioinformaticsCore/janis
- This workshop GitHub: https://github.com/PMCC-BioinformaticsCore/janis-workshops/portable-pipeline

## Workshop Outline

### Day 1

For the first session, we will get ourselves familiar with Janis.  

|            	| Description                                                                                                                                                      	|
|------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| 30 minutes 	| Introduction to Janis<br>- Installing and setting up Janis Environment<br>- _OR_ connecting to preconfigured environment<br>- Running a small workflow as a test 	|
| 30 minutes 	| Building a workflow to align a set of fastqs<br>- Learn about preconfigured tools<br>- Using BWA mem + samtools view<br>- Add Mark Duplicates<br>- Running a small test       	|
| 30 minutes 	| Exercise: Extend alignment to complete data processing<br>- Add SortSam + SetNmMdAndUqTags <br>- Test the pipeline                                                            	|
| 30 minutes 	| Wrap-up <br> - Going through exercise' solutions <br>- Q&A|



### Day 2

For the second session, we will complete our portable germline variant-calling pipeline

|            	| Description                                                                                                                                                      	|
|------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| 30 minutes 	| Recap of Day 1 |
| 30 minutes 	| Adding new tools definition in Janis <br> - Create Janis' GATK ApplyBQSR + GATK BaseRecalibrator <br> - Add new tools to workflow <br> - Test updated pipeline |
| 30 minutes 	| Exercise: Adding more tools to complete germline pipeline <br>- Add GATK HaplotypeCaller  <br> -  Add new tool to workflow <br> - Test updated pipeline 	|
| 30 minutes 	| Wrap-up <br> - Going through exercise' solutions <br>- Q&A|


## Workshop environment

Prerequisites to install Janis on your personal computer:

- A unix-based operating system (MacOS / Ubuntu / RHEL / CentOS / etc)
- Python 3.6+
- Docker
- Zip (archiver for zip files)
- Node.js

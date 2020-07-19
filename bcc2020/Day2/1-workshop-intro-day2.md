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

~For the first session, we will get ourselves familiar with Janis.~ 

|            	| Description                                                                                                                                                      	|
|------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| 30 minutes 	| ~Introduction to Janis<br>- Installing and setting up Janis Environment<br>- _OR_ connecting to preconfigured environment<br>- Running a small workflow as a test~ 	|
| 30 minutes 	| ~Building a workflow to align a set of fastqs<br>- Learn about preconfigured tools<br>- Using BWA mem + samtools view<br>- Add Mark Duplicates<br>- Running a small test~       	|
| 30 minutes 	| ~Exercise: Extend alignment to complete data processing<br>- Add SortSam + SetNmMdAndUqTags <br>- Test the pipeline~                                                            	|
| 30 minutes 	| ~Wrap-up <br> - Going through exercise' solutions <br>- Q&A~|



### Day 2

For the second session, we will complete our portable germline variant-calling pipeline

|            	| Description                                                                                                                                                      	|
|------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| 30 minutes 	| Recap of Day 1 |
| 30 minutes 	| Adding new tools definition in Janis <br> - Create Janis' GATK ApplyBQSR + GATK BaseRecalibrator <br> - Add new tools to workflow <br> - Test updated pipeline |
| 30 minutes 	| Exercise: Adding more tools to complete germline pipeline <br>- Add GATK HaplotypeCaller  <br> -  Add new tool to workflow <br> - Test updated pipeline 	|
| 30 minutes 	| Wrap-up <br> - Going through exercise' solutions <br>- Q&A|



## Requirements:

- Python 3.6+
- Docker

## Workshop environment:

- AWS VM (Pre-installed with solutions from Day1)
# Workshop 1.8 - Running a germline pipeline

We're going to run a germline variant-calling pipeline across our samples.

Documentation: https://janis.readthedocs.io/en/latest/pipelines/wgsgermlinemulticallers.html

Let's highlight the required inputs:

- `fastqs: Array<FastqGzPair>`
- `gatk_intervals: Array<bed>`
- `reference: FastaWithDict`
- `snps_dbsnp: CompressedIndexedVCF`
- `snps_1000gp: CompressedIndexedVCF`
- `known_indels: CompressedIndexedVCF`
- `mills_indels: CompressedIndexedVCF`

## Preparing our inputs

We'll prepare an inputs file for our sample_name, fastqs and gatk_intervals, as this pipeline can accept an array of fastq pairs.

**wgs-germline-inputs.yml**
```yaml
sample_name: NA12878
fastqs:
- - $HOME/workshop1/data/BRCA1-R1.fastq.gz
  - $HOME/workshop1/data/BRCA1-R2.fastq.gz
gatk_intervals: 
- $HOME/workshop1/data/BRCA1.bed
```

## Recipes

At Peter Mac, a number of prebuilt "recipes" are available at Peter Mac. For the HG38 reference genome, there is a recipe called `hg38` that will fill out the inputs:

- `reference: FastaWithDict`
- `snps_dbsnp: CompressedIndexedVCF`
- `snps_1000gp: CompressedIndexedVCF`
- `known_indels: CompressedIndexedVCF`
- `mills_indels: CompressedIndexedVCF`

Recipes can be specified with the `-r` workflow option (following by the recipes you want to use).

## Running the pipeline

Putting our inputs and the recipe together, we can run the pipeline using the following command:

```bash
janis run \
    -B -o part4 \
    -r hg38 \
    --inputs wgs-germline-inputs.yml \
    WGSGermlineGATK
````
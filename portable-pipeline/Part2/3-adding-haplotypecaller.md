# Janis Workshop (2.3)

## Exercise: add a variant-caller (GATK Haplotypecaller) to complete the germline variant-caller for this workshop

In this section, we will give you some hands-on time to add new tool (not previously in the registry) to a workflow. The task in this exercise is to create a CommandTool for `GATK HaplotypeCaller` using a `janis.CommandToolBuilder` (in our `part2/tools.py` file). After we create this tool, we'll add it to our `part2/variantcaller.py` workflow.


## Creating GATK HaplotypeCaller tool class

The commandline equivalent command that we are trying to add into our workflow is 

```bash
gatk HaplotypeCaller  \
   --input input.bam \
   --reference Homo_sapiens_assembly38.fasta \
   --output output.vcf.gz \
   --bam-output output.bam \
   --create-output-bam-index
```

Like all of previous steps, let's start with our template:

<details>
    <summary> Click to show solution </summary>

```python
Gatk4HaplotypeCaller_4_1_4 = CommandToolBuilder(
    tool="Gatk4HaplotypeCaller",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "HaplotypeCaller"],
    inputs=[],
    outputs=[]
)
```

    
</details>


<br> Let's wrap our individual inputs:

- `bam`: will be an indexed bam (remember to rewrite the secondary files):

- `reference`: Reference sequence file

- `outputFilename`: Where to write the indexed output VCF.gz. Note, HaplotypeCaller will output a GZIP compressed VCF with it's tabix index (.vcf.gz.tbi), the Janis type `VcfTabix` can represent this on the output:

- `bamOutputFilename`: File to which assembled haplotypes should be written

- `createBamOutputIndex`: We _want_ to create the index for the BAM.
    
<details>
    <summary> Click to show solution </summary>
    
```python
    ToolInput("bam", BamBai, prefix="--input"),

    ToolInput("reference", FastaWithIndexes, prefix="--reference"),

    ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), extension=".vcf.gz"), prefix="--output"),

    ToolInput("bamOutputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".HAP", extension=".bam"),prefix="--bam-output"),

    ToolInput("createBamOutputIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),   
```
    
</details>      

### Outputs

We have two outputs for this tool `out_vcf` and `out_bam`: 

<details>
    <summary> Click to show solution </summary>
    
```python
    ToolOutput("out_vcf", VcfTabix, selector=InputSelector("outputFilename")),

    ToolOutput("out_bam", BamBai, selector=InputSelector("bamOutputFilename"), secondaries_present_as={".bai": "^.bai"}),
```
    
</details>    


### Final HaplotypeCaller tool

You should have your final haplotypecaller tool that looks like the following: 
<details>
    <summary> Click to show solution </summary>
    
```python
   Gatk4HaplotypeCaller_4_1_4 = CommandToolBuilder(
    tool="Gatk4HaplotypeCaller",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "HaplotypeCaller"],
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), extension=".vcf.gz"), prefix="--output"),
        ToolInput("bamOutputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".HAP", extension=".bam"),prefix="--bam-output"),
        ToolInput("createBamOutputIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),
    ],
    outputs=[
        ToolOutput("out_vcf", VcfTabix, selector=InputSelector("outputFilename")),
        ToolOutput("out_bam", BamBai, selector=InputSelector("bamOutputFilename"), secondaries_present_as={".bai": "^.bai"}),
    ],
)
    
```
    
</details>    
    
    
    

<br>
Let's check the WDL conversion of the full tool:

```bash
    janis translate part2/tools.py --name Gatk4HaplotypeCaller_4_1_4 wdl
```

The command part of this WDL file should look quite similar to the command that we are targetting. 

```wdl
command <<<
    gatk HaplotypeCaller \
      --input '~{bam}' \
      --reference '~{reference}' \
      --output '~{select_first([outputFilename, "~{basename(bam, ".bam")}.vcf.gz"])}' \
      --bam-output '~{select_first([bamOutputFilename, "~{basename(bam, ".bam")}.HAP.bam"])}' \
      ~{if select_first([createBamOutputIndex, true]) then "--create-output-bam-index" else ""}
  }
}
```


## Adding variant-caller to workflow

This looks good! Let's jump over to our `part2/variantcaller.py` and add this as our final piece.

Import our newly created `Gatk4HaplotypeCaller_4_1_4` from `tools`:

```python
from tools import (
    Gatk4BaseRecalibrator_4_1_4,
    Gatk4ApplyBQSR_4_1_4,
    Gatk4HaplotypeCaller_4_1_4,
)
```


```python
# Use HaplotypeCaller as our variant caller
w.step(
    "haplotypecaller",
    Gatk4HaplotypeCaller_4_1_4(bam=w.applybqsr.out_bam, reference=w.reference),
)
```

Let's create 2 outputs for our new results:

```python
w.output("out_assembledbam", source=w.haplotypecaller.out_bam)
w.output("out_variants", source=w.haplotypecaller.out_vcf)
```

Let's check the translation of our full workflow just to check everything's looking okay. 

> You can also confirm your workflow with the solution: `part2/variantcaller_solution.py`.

```bash
janis translate part2/variantcaller.py wdl
```

## Run the final workflow!

Now that the final workflow is complete, you can run the final workflow with:

```bash
janis run -o part2 --development \
    part2/variantcaller.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --known_sites reference/brca1_hg38_dbsnp138.vcf.gz \
    --known_sites reference/brca1_hg38_known_indels.vcf.gz \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

Let's inspect the final output directory:

```bash
$ ls -lGh part2
-rw-r--r-- 2 ec2-user 541K Jul 19 03:32 out_assembledbam.bam
-rw-r--r-- 2 ec2-user  224 Jul 19 03:32 out_assembledbam.bam.bai
-rw-r--r-- 2 ec2-user 2.6M Jul 19 03:23 out_bam.bam
-rw-r--r-- 2 ec2-user  296 Jul 19 03:23 out_bam.bam.bai
-rw-r--r-- 2 ec2-user 1.1M Jul 19 03:23 out_recalibration_table.table
-rw-r--r-- 2 ec2-user  12K Jul 19 03:32 out_variants.vcf.gz
-rw-r--r-- 2 ec2-user  170 Jul 19 03:32 out_variants.vcf.gz.tbi
```

[Next >](4-closing.md)
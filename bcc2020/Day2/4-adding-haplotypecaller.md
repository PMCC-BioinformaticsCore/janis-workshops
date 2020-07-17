# BCC2020 EAST - Janis Workshop (2.4)

## Exercise: add a variant-caller (GATK Haplotypecaller) to complete the germline variant-caller for this workshop

In this section, we will give you some hands-on time to add new tool (not previously in the registry) to a workflow. The task in this exercise is to create a CommandTool for `GATK HaplotypeCaller` using a `janis.CommandToolBuilder` (in our `day2/tools.py` file). After we create this tool, we'll add it to our `day2/variantcaller.py` workflow.


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

Let's wrap our individual inputs:

- `bam`: will be an indexed bam (remember to rewrite the secondary files):

    ```python
    ToolInput(
        "bam", BamBai, prefix="--input", secondaries_present_as={".bai": "^.bai"}
    )
    ```

- `reference`: Reference sequence file

    ```python
    ToolInput("reference", FastaWithIndexes, prefix="--reference")
    ```

- `outputFilename`: Where to write the indexed output VCF.gz. Note, HaplotypeCaller will output a GZIP compressed VCF with it's tabix index (.vcf.gz.tbi), the Janis type `VcfTabix` can represent this on the output:

    ```python
    ToolInput(
        "outputFilename",
        Filename(prefix=InputSelector("bam"), extension=".vcf.gz"),
        prefix="--output",
    ),
    ```

- `bamOutputFilename`: File to which assembled haplotypes should be written

    ```python
    ToolInput(
        "bamOutputFilename",
        Filename(
            prefix=InputSelector("bam"), suffix=".assembled", extension=".bam"
        ),
        prefix="--bam-output",
    )
    ```

- `createBamOutputIndex`: We _want_ to create the index for the BAM.

    ```python
    ToolInput(
        "createBamOutputIndex",
        Boolean(optional=True),
        prefix="--create-output-bam-index",
        default=True,
    ),
    ```

### Outputs

We have two outputs for this tool:

- `out_vcf`: 

    ```python
    ToolOutput("out_vcf", VcfTabix, selector=InputSelector("outputFilename"))
    ```

- `out_bam`: 

    ```python
    ToolOutput(
        "out_bam",
        BamBai,
        selector=InputSelector("bamOutputFilename"),
        secondaries_present_as={".bai": "^.bai"},
    )
    ```

### Final HaplotypeCaller tool

```python
Gatk4HaplotypeCaller_4_1_4 = CommandToolBuilder(
    tool="Gatk4HaplotypeCaller",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "HaplotypeCaller"],
    inputs=[
        ToolInput(
            "bam", BamBai, prefix="--input", secondaries_present_as={".bai": "^.bai"}
        ),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput(
            "outputFilename",
            Filename(prefix=InputSelector("bam"), extension=".vcf.gz"),
            prefix="--output",
        ),
        ToolInput(
            "bamOutputFilename",
            Filename(
                prefix=InputSelector("bam"), suffix=".assembled", extension=".bam"
            ),
            prefix="--bam-output",
        ),
        ToolInput(
            "createBamOutputIndex",
            Boolean(optional=True),
            prefix="--create-output-bam-index",
            default=True,
        ),
    ],
    outputs=[
        ToolOutput("out_vcf", VcfTabix, selector=InputSelector("outputFilename")),
        ToolOutput(
            "out_bam",
            BamBai,
            selector=InputSelector("bamOutputFilename"),
            secondaries_present_as={".bai": "^.bai"},
        ),
    ],
)
```
Let's check the WDL conversion of the full tool:

```bash
    janis translate day2/tools_solution.py --name Gatk4HaplotypeCaller_4_1_4 wdl
```

```wdl
version development

task Gatk4HaplotypeCaller {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    File bam
    File bam_bai
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    String? outputFilename
    String? bamOutputFilename
    Boolean? createBamOutputIndex
  }
  command <<<
    gatk HaplotypeCaller \
      --input '~{bam}' \
      --reference '~{reference}' \
      --output '~{select_first([outputFilename, "~{basename(bam, ".bam")}.vcf.gz"])}' \
      --bam-output '~{select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"])}' \
      ~{if defined(select_first([createBamOutputIndex, true])) then "--create-output-bam-index" else ""}
    if [ -f $(echo '~{select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"])}' | sed 's/\.[^.]*$//').bai ]; then ln -f $(echo '~{select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"])}' | sed 's/\.[^.]*$//').bai $(echo '~{select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"])}' ).bai; fi
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "broadinstitute/gatk@sha256:cec850f20311f0686fcf88510bc44e529590d78bec7076a603132115943c09e6"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out_vcf = select_first([outputFilename, "~{basename(bam, ".bam")}.vcf.gz"])
    File out_vcf_tbi = select_first([outputFilename, "~{basename(bam, ".bam")}.vcf.gz"]) + ".tbi"
    File out_bam = select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"])
    File out_bam_bai = select_first([bamOutputFilename, "~{basename(bam, ".bam")}.assembled.bam"]) + ".bai"
  }
}
```

This looks good! Let's jump over to our `day2/variantcaller.py` and add this as our final piece.

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

> You can also confirm your workflow with the solution: `day2/variantcaller_solution.py`.

```bash
janis translate day2/variantcaller.py wdl
```

## Run the final workflow!

Now that the final workflow is complete, you can run the final workflow with:

```bash
janis run -o day2 --development \
    day2/variantcaller_solution.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --known_sites reference/knownsites.vcf.gz \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

Let's inspect the final output directory:

```bash
$ ls -lGh day2
# TODO: add output here
```


## Advanced task

If you are familiar with how python object oriented works, this tool definition can be created as a separate class. This can then be used via python import similar to how we setup our janis-bioinformatics toolbox in our previous examples on Day 1. 

You can take a look at our GATK HaplotypeCaller implementation in our tool registry: 

[Link](link)

If you wish, you can attempt to modify your implementation this way. You will be able to use this definition as an independent workflow. For example, if you already have a bam file and wish to only run a variant-caller on your sample. 

Step:
- As above, but in a separate class

Run as workflow:
```bash
    janis run GATK_Haplotypecaller <input>
```

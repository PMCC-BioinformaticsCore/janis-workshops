# Janis Workshop (1.4)

## Exercise: extend alignment workflow to complete the data processing workflow

In this section, we will give you some hands-on time to play  with Janis workflow. The task in this exercise is to extend alignment workflow from the previous section where we will add

- `GATK4 SortSam` to the output of Mark Duplicates. 
- `Gatk4 SetNmMdAndUqTags` to the result from Sort Sam.

We'll use the same file from the previous part (`part1/processing.py`) for our analysis. 

## Adding SortSam to workflow

The `Gatk4SortSam_4_1_4` has already been imported from the toolbox [Janis GATK4 SortSam documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/gatk4/gatk4sortsam.html) for you:

```python
# These imports should already be near the top of your file
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)
```

In addition to connecting the output of `markduplicates` to Gatk4 SortSam, we want to tell SortSam to use the following values:

- sortOrder: `"coordinate"`

Instead of connecting an input or a step, we can just provide the literal value.

 Try to write the step definition BEFORE checking the solution below: 
<details>
    <summary> Click to show solution </summary>
        
```python
w.step(
    "sortsam",
    Gatk4SortSam_4_1_4(
        bam=w.markduplicates.out,
        sortOrder="coordinate",
    )
)
```
</details>

### Adding SetNmMdAndUqTags

[GATK4 SetNmMdAndUqTags](https://janis.readthedocs.io/en/latest/tools/bioinformatics/gatk4/gatk4setnmmdanduqtags.html) 
is going to calculate the following tags by comparing our BAM to the reference genome:

- NM: Edit distance to the reference
- MD: String encoding mismatched and deleted reference bases
- UQ: Phred likelihood of the segment, conditional on the mapping being correct

> These are predefined standard tags from the [SAM specification](https://samtools.github.io/hts-specs/SAMtags.pdf).

Like SortSam, this tool has already been imported as `Gatk4SetNmMdAndUqTags_4_1_4`, and it requires two inputs:

- `bam`: we'll use the output of `sortsam`,
- `reference`: The reference genome

Try to write the step definition _BEFORE_ checking the solution below:

<details>
    <summary> Click to show solution </summary>

```python
w.step(
    "fix_tags",
    Gatk4SetNmMdAndUqTags_4_1_4(
        bam=w.sortsam.out,
        reference=w.reference,
    ),
)
```

</details>

### Collecting the output

Now that we've finished our analysis, lets add one output from `sortsam`:

```python
w.output("out_bam", source=w.fix_tags.out)
```

## Workflow + Translation

Hopefully you have a workflow that looks like the following!

> The final workflow is also available in `$JW/part1/preprocesing_solution.py`.

<details>
    <summary> Click to show solution </summary>


```python
    
from janis_core import WorkflowBuilder, String
  
# Import bioinformatics types
from janis_bioinformatics.data_types import FastqGzPairedEnd, FastaWithIndexes

# Import bioinformatics tools
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)

# Construct the workflow here
w = WorkflowBuilder("preprocessingWorkflow")

# inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPairedEnd)
w.input("reference", FastaWithIndexes)

# Use `bwa mem` to align our fastq paired ends to the reference genome

w.step(
    "bwamem",  # step identifier
    BwaMemLatest(
        reads=w.fastq,
        readGroupHeaderLine=w.read_group,
        reference=w.reference,
        markShorterSplits=True,  # required for MarkDuplicates
    ),
)

# Use `samtools view` to convert the aligned SAM to a BAM
#   - Use the output `out` of the bwamem step
w.step(
    "samtoolsview",
    SamToolsView_1_9(sam=w.bwamem.out),
)

# Use `gatk4 MarkDuplicates` on the output of samtoolsview
#   - The output of BWA is query-grouped, providing "queryname" is good enough
w.step(
    "markduplicates",
    Gatk4MarkDuplicates_4_1_4(
        bam=w.samtoolsview.out,
        assumeSortOrder="queryname"
    ),
)

w.step("sortsam",
    Gatk4SortSam_4_1_4(
        bam=w.markduplicates.out,
        sortOrder="coordinate",))

w.step(
    "fix_tags",
    Gatk4SetNmMdAndUqTags_4_1_4(
        bam=w.sortsam.out,
        reference=w.reference,
    ),
)

w.output("out_bam", source=w.fix_tags.out)
    
```

</details>    
<p>    
    
We can again translate the following file into Workflow Description Language using janis from the terminal:

```bash
janis translate part1/preprocessing.py wdl
```



## Running the alignment workflow

Now that we have a complete pipeline again, let's re-run the same command we did before.

```
janis run -o part1 --development --keep-intermediate-files \
    part1/preprocessing.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

This time we notice that CWLTool is using _cached output_ of the first two steps:

```
... [INFO]: cwltool: INFO [job bwamem] Using cached output ...
... [INFO]: cwltool: INFO [job samtoolsview] Using cached output ...
```

Inspecting out output directory, we two more entries: a bam and its index!

```bash
$ ls -lgh part1/

# -rw-r--r--  3 1677682026   2.7M Jul 16 17:15 out_bam.bam
# -rw-r--r--  3 1677682026   296B Jul 16 17:15 out_bam.bam.bai
```

#### Optional

Check to see if the `MD`, `NM` and `UQ` tags are in the output bam:

> Hint: you can run `samtools view` in a the docker container with:
> ```python
> docker run -v $JW/part1/:/data/ quay.io/biocontainers/samtools:1.9--h8571acd_11 samtools view /data/out_bam.bam | head
> ```

## Great work!!

Great work! You've built a completely portable pipeline that uses containers to align a set of fastqs to a reference genome, marked duplicates in the aligned BAM and sorted the result. You can run this pipeline in your current envionrment (local), on HPCs using Slurm, or even using Amazon or Google cloud services. 

If you're looking for a bigger challenge, try the advanced task in the next section!


## Advanced task

For those we are familiar with this GATK workflow, you might have noticed that there are other steps that we've omitted from this example. If you have finished the exercise above, you can attempt to complete the remaining steps of this data processing workflow. We might look at some of these steps in tomorrow's workshop too.

- Gatk4BaseRecalibrator_4_1_4
- Gatk4ApplyBqsr_4_1_4

[Next >](5-debugging.md)


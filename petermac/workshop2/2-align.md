# Workshop 2.2 - Alignment

In this stage, we're going to build a simple workflow to align short reads of DNA.

We start with a pair of compressed `FASTQ` files, we align these reads into an uncompressed `SAM` file (the _de facto_ standard for short read alignments) using `BWA MEM`, compress this into the binary equivalent `BAM` file using `samtools`, and finally sort the reads using `GATK4 SortSam`.


These tools already exist within the Janis Tool Registry, you can see their documentation online:

- [BWA MEM](https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html)
- [Samtols View](https://janis.readthedocs.io/en/latest/tools/bioinformatics/samtools/samtoolsview.html)
- [GATK4 SortSam](https://janis.readthedocs.io/en/latest/tools/bioinformatics/gatk4/gatk4sortsam.html)

## Creating our file

A Janis workflow file is a regular Python file, so we can start by creating a file called `alignment.py` and importing Janis.

```bash
mkdir part1
# your choice of editor, vim, emacs, sublime, vscode
vim part1/alignment.py
```

Then include the following python code to load Janis:

```python
import janis
```

## Importing our tools and datatypes

Python requires that you import the tools and types that you use, these import statements are available on the documentation. We'll have one import per tool, and one import for every data-types we use.

We have four inputs we want to expose on this workflow:

1. Sequencing Reads (`FastqGzPair` - paired end sequence)
2. Sample name (`String`)
3. Read group header (`String`)
4. Reference files (`Fasta` + index files)


We can use the `janis.String` datatype (imported with Janis) for the first, and we can import the remaining bioinformatics types:

```python
from janis_bioinformatics.tools.bwa.mem.latest import BwaMemLatest
from janis_bioinformatics.tools.samtools.view.view import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict
```

## Declaring our workflow and exposing inputs

We'll create an instance of the [`janis.WorkflowBuilder`](https://janis.readthedocs.io/en/latest/references/workflow.html#janis.Workflow) class, this requires a workflow identifier. We discussed which imports we want in the previous section which we can expose on this workflow with the `janis.Workflow.input` method:

```python
w = janis.WorkflowBuilder("alignmentWorkflow")

w.input("sample_name", janis.String)
w.input("read_group", janis.String)
w.input("fastq", FastqGzPair)
w.input("reference", FastaWithDict)
```

## Declaring our steps and connections

Steps are easy to create, however you may need to refer to the documentation when writing your own workflows to know which named parameters a tool takes (and their types). Similar to exposing inputs, we create steps with the `janis.Workflow.step` method.

We can refer to any node on the workflow graph (such as an input) by accessing the property of the same name (dot-notation). Eg, to access the `read_group` on our workflow, we can use `w.read_group`.

We instantiate our tool with the named parameters we want to provide and pass that as the second parameter to the `janis.Workflow.step` method:

### BWA MEM

```python
w.step(
    "bwamem",
    BwaMemLatest(
        reads=w.fastq,
        readGroupHeaderLine=w.read_group,
        reference=w.reference
    )
)
```

### Samtools view

When creating the connection between `bwamem` and `samtoolsview`, we'll access the `out` output of `BwaMemLatest`. This will create a dependency of `"bwamem"` for `samtoolsview`.

```python
w.step(
    "samtoolsview",
    SamToolsView_1_9(
        sam=w.bwamem.out
    )
)
```

### SortSam

SortSam requires a number of values we want to set 

```python
w.step(
    "sortsam",
    Gatk4SortSam_4_1_2(
        bam=w.samtoolsview.out,
        sortOrder="coordinate",
        createIndex=True,
        validationStringency="SILENT",
        maxRecordsInRam=5000000
    )
)
```

## Exposing outputs

Outputs have a very similar syntax to both inputs and steps, they take an `identifier` and a named `source` parameter. We only want to output the resulting bam file from `sortsam`, which we can do with the following line:

```python
w.output("out", source=w.sortsam.out)
```

## Workflow + Translation

Hopefully you have a workflow that looks like the following!

```python
import janis

from janis_bioinformatics.tools.bwa.mem.latest import BwaMemLatest
from janis_bioinformatics.tools.samtools.view.view import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict

w = janis.WorkflowBuilder("alignmentWorkflow")

# Inputs
w.input("sample_name", janis.String, value="NA12878")
w.input("read_group", janis.String, value="@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA")
w.input("fastq", FastqGzPair, value="/path/to/reads.fastq")
w.input("reference", FastaWithDict, value="/path/to/reference.fasta")

# Steps
w.step(
    "bwamem", 
    BwaMemLatest( 
        reads=w.fastq, 
        readGroupHeaderLine=w.readGroup, 
        reference=w.reference
    )
)
w.step(
    "samtoolsview", 
    SamToolsView_1_9(
        sam=w.bwamem.out
    )
)

w.step(
    "sortsam",
    Gatk4SortSam_4_1_2(
        bam=w.samtoolsview.out,
        sortOrder="coordinate",
        createIndex=True,
        validationStringency="SILENT",
        maxRecordsInRam=5000000
    )
)

# Outputs
w.output("out", source=w.sortsam.out)
```

We can translate the following file into Workflow Description Language using janis from the terminal:

```bash
janis translate alignment.py wdl
```


## Running the alignment workflow

```
janis run -o part1 part1/alignment.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --sample_name NA12878 \
    --read_group "'@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA'"
```
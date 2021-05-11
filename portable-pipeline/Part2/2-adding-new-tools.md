# Janis Workshop (2.2)

In the previous workshop, we used tools from the Janis Bioinformatics toolbox. But what happens if you want to use a new tool that is not on Janis Bioinformatics!?

In Part 2 of this workshop, we're going to use the `janis.CommandToolBuilder` to teach Janis how to interact with command line software. We sometimes refer to this as "Wrapping a new tool" or "Creating a tool wrapper".

> Importantly, every command line tool in Janis runs in a container. This means that all of our workflows are portable AND reproducible. Using containers means we also don't have to install the software on our computer.

In this section, we're going to add 3 new GATK tools to Janis:

1. [BaseRecalibrator](https://gatk.broadinstitute.org/hc/en-us/articles/360036898312-BaseRecalibrator) - Generates a recalibration table for ApplyBQSR.

2. [ApplyBQSR](https://gatk.broadinstitute.org/hc/en-us/articles/360037055712-ApplyBQSR) - Performs a base quality score recalibration using the table produced by BaseRecalibrator.

3. [HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller) - Our variant caller! Call germline SNPs and indels via local re-assembly of haplotypes.

We'll go through adding the first two, and then you can add HaplotypeCaller in the next exercise.

Note, we're going to use the official GATK docker container that the broad institute provides when building our tools: `broadinstitute/gatk:4.1.4.0`.

To get started, here are some of the basic concepts for wrapping tools in Janis. 

## Tool structure

We'll use the following template for our tools:

```python
ToolName = CommandToolBuilder(
    tool: str="toolname",
    base_command=["base", "command"],
    container="container/name:version",
    version="version",
    inputs=[],  # List[ToolInput]
    outputs=[], # List[ToolOutput]
)
```
- `tool` is a unique identifier of the tool.

- `base_command` is the command that you would use to call the container. For example `"echo"`, `["bwa", "mem"]`, `["gatk", "MarkDuplicates"]`, `["samtools", "flagstat"]`

    > It's important to separate part of the base command, eg: `["bwa", "mem"`], not ~`"bwa mem"`~.

- `inputs` - A list of named inputs that the tool can receive (we'll see how this is structured soon)

- `outputs` - A list of named outputs that the tool will provide (we'll see how a tool can collect outputs soon)

- `container` - A docker container of the tool - technically any OCI compliant container is perfect, so you can use containers from `quay.io`.
    > _Further information_: [Containerising your tools](https://janis.readthedocs.io/en/latest/tutorials/container.html)

- `version` - The version of the tool that we're using.

### Tool Input

We use a `janis.ToolInput` to represent inputs to a command line tool. The `ToolInput` also provides the mechanisms for constructing our command line (eg: prefix, position, separators, etc). See the documentation for more ways to [configure a ToolInput](https://janis.readthedocs.io/en/latest/references/commandtool.html#tool-input).

```python
janis.ToolInput(
	tag: str,
	input_type: DataType,
	position: Optional[int] = None,
	prefix: Optional[str] = None,
    # more configuration options
	prefix_applies_to_all_elements: bool = None,
	secondaries_present_as: Dict[str, str] = None,
	default: Any = None,
	doc: Optional[str] = None
)
```

### Tool outputs

We’ll use a `janis.ToolOutput` to collect and represent outputs. A ToolOutput has a type, and we can use a `selector` to get an output.
See the documentation for more ways to [configure a ToolOutput](https://janis.readthedocs.io/en/latest/references/commandtool.html#tool-output)

```python
janis.ToolOutput(
    tag: str,
    output_type: DataType,
    selector: Union[janis_core.types.selectors.Selector, str, None] = None,
    # more configuration options
    presents_as: str = None,
    secondaries_present_as: Dict[str, str] = None,
    doc: Optional[str] = None
)
```

A tool may output multiple files, we want to give each of the relevant output file a meaningful output name.
To do so, you will need to provide Janis with the instruction on which file to select for a given output name.

To do this in Janis, we can use different selectors to select the relevant outputs. For example:

- `InputSelector` - we can use the value of an input to construct an output filename
- `WildcardSelector` - use a `glob` format to find an output, for example get all the bams in the execution directory with `WildcardSelector("*.bams")`.

We will see how this works in our example.

## Setup

```bash
cat ~/.janis/janis.conf
```

should give you:
```yaml
engine: cwltool
notifications:
  email: null
template:
  id: local
```

And you should see the following files on `part2` directory

```bash
ls -lGh part2/
```

```
-rwxr-xr-x 1 ec2-user  268 Jul 16 16:37 tools.py
-rwxr-xr-x 1 ec2-user 3.3K Jul 17 02:12 tools_solution.py
-rwxr-xr-x 1 ec2-user 1.9K Jul 16 16:36 variantcaller.py
-rwxr-xr-x 1 ec2-user 3.3K Jul 17 01:55 variantcaller_solution.py
```

There are 4 files:

1. `variantcaller.py` - This is from our 'preprocessing.py' workflow in Part 1, and where we will put our complete variant calling workflow.
2. `tools.py` - We'll add our new tools in here, and then import them into the `variantcaller.py`.
3. `tools_solution.py` is one of the solutions to these exercises (don't peek)!
4. `variantcaller_solution.py` is one of the solutions to these exercises (don't peek)!


## Building our tools

## Creating GATK BaseRecalibrator Janis tool

BaseRecalibrator generates a recalibration table for Base Quality Score Recalibration (BQSR). On command line, you will usually call BaseRecalibrator as follow:

```bash
gatk BaseRecalibrator \
   --input my_reads.bam \
   --reference reference.fasta \
   --output recal_data.table \
   --known-sites dbsnp.vcf \
   --known-sites known_indels.vcf
```

### Adding tool to Janis python file

To add this tool, use your favourite text editor edit `part2/tools.py`.

We have pre-populated some of the janis imports to get you started. 

```python
from janis_core import (
    CommandToolBuilder,
    ToolInput,
    ToolOutput,
    InputSelector,
    Array,
    File,
    Filename,
    Boolean,
)

from janis_bioinformatics.data_types import Bam, BamBai, FastaWithIndexes, VcfTabix, Vcf
```

Add the following lines into `part2/tools.py`: 

```python
Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    tool="Gatk4BaseRecalibrator",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "BaseRecalibrator"],
    # we'll look at these next
    inputs=[],  # List[ToolInput]
    outputs=[], # List[ToolOutput]
)
```

### Adding Inputs

Alright, let's decode the different inputs we see to a corresponding ToolInput:

- `--input` - Our input bam. 

    ```python
     ToolInput("bam", BamBai, prefix="--input"),
    ```


- `--reference` - Reference sequence file (fasta with indexes):

    ```python
    ToolInput("reference", FastaWithIndexes, prefix="--reference"),
    ```


- `--output` - The filename of the output recalibration table. This is not an input file, but a generated filename. For this reason, we'll use the `janis.Filename` class to generate a filename:

    ```python
    ToolInput(
        "outputFilename", 
        Filename(extension=".table"), 
        prefix="--output"
    ),
    ```


- `--known-sites` - An array of known sites (gzipped compressed and tabix indexed VCF: `VcfTabix`). 
  Note that the tool requires us to apply prefix to each element in the array (e.g `--known-sites dbsnp.vcf --known-sites known_indels.vcf`).
  To provide this instruction to Janis, you will need to add this parameter `prefix_applies_to_all_elements=True`: 

    ```python
    ToolInput(
        "knownSites", 
        Array(VcfTabix), 
        prefix="--known-sites", 
        prefix_applies_to_all_elements=True
    ),
    ```

This gives definition as:

```python
Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    tool="Gatk4BaseRecalibrator",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "BaseRecalibrator"],

    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput(
	    "outputFilename", 
	    Filename(extension=".table"), 
	    prefix="--output"
	),
        ToolInput(
	    "knownSites", 
	    Array(VcfTabix), 
	    prefix="--known-sites", 
	    prefix_applies_to_all_elements=True
	),
    ],
    outputs=[],  # List[ToolOutput]
)
```


### Adding outputs

Our BaseRecalibrator has one output, the recalibration table specified by `--output` (fed by our input called `outputFilename` above).

In general the value of `selector=` in `ToolOutput` can be as simple as `selector="my_output_filename.table"`.
But, this definition makes your Janis tool less flexible. 
If you want the user of your Janis tool to be able to dynamically set the output filename,
you can use an `InputSelector` to construct a string to represent the output filename.

In this example, we want to select an output file that has the exact value the user passed to `outputFilename`:

```python
ToolOutput("out_recalibration_report", File, selector=InputSelector("outputFilename"))
```

### Final tool definition

Your complete tool definition should look like this:

```python
Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    tool="Gatk4BaseRecalibrator",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "BaseRecalibrator"],

    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("outputFilename", Filename(extension=".table"), prefix="--output"),
        ToolInput("knownSites", Array(VcfTabix), prefix="--known-sites", prefix_applies_to_all_elements=True),
    ],
    outputs=[
        ToolOutput("out_recalibration_report", File, selector=InputSelector("outputFilename"))
    ],
)
```

At this point, we will save this `tools.py` file. 

### Translate new tool definition to CWL/WDL 

When translating a file of multiple tool definitions, it's good practice to specify the `--name` of the tool, eg:

```bash
janis translate part2/tools.py --name Gatk4BaseRecalibrator_4_1_4 wdl
```

Look how closely our command section mirrors the command we're trying to replicate!

```wdl
command <<<
    gatk BaseRecalibrator \
      --input '~{bam}' \
      --reference '~{reference}' \
      --output '~{select_first([outputFilename, "generated.table"])}' \
      ~{if length(knownSites) > 0 then "--known-sites '" + sep("' --known-sites '", knownSites) + "'" else ""}
>>>

```

## Creating GATK ApplyBQSR Janis tool

We will apply similar steps for ApplyBQSR:

The following is the command that we will run on commandline if we are to run ApplyBQSR manually:

```bash
gatk ApplyBQSR \
   --input input.bam \
   --reference reference.fasta \
   --bqsr-recal-file recalibration.table \
   --output output.bam \
   --create-output-bam-index
```

### Adding tool to Janis python file

To start, we will add this tool into `part2/tools.py`.

You will add the following lines underneath `Gatk4BaseRecalibrator_4_1_4` tool definition that we created in the previous exercise. 

```python
Gatk4ApplyBQSR_4_1_4 = CommandToolBuilder(
    tool="Gatk4ApplyBqsr",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "ApplyBQSR"],
    # we'll look at these next
    inputs=[],
    outputs=[],
)
```

### Adding Inputs

Very similar arguments apply to each tool input here:

- `--output` is a generated filename,
- `--create-output-bam-index` is an optional Boolean, which we'll default to true

We will add the following inputs:

```python
ToolInput("bam", BamBai, prefix="--input"),

ToolInput("reference", FastaWithIndexes, prefix="--reference"),

ToolInput("recalFile", File, prefix="--bqsr-recal-file"),

ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".recal", extension=".bam"), prefix="--output"),

ToolInput("createBamIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),

```

### Adding Outputs

We have one indexed bam as an output. The filename was specified in `outputFilename` input value.
To instruct Janis that the Bam index file has a `.bai` extension instead of `.bam.bai`, add the parameter `secondaries_present_as={".bai": "^.bai"}`.

```python
ToolOutput("out_bam", BamBai, selector=InputSelector("outputFilename"),secondaries_present_as={".bai": "^.bai"},)
```

### Final tool

The full tool definition should look like:

```python
Gatk4ApplyBQSR_4_1_4 = CommandToolBuilder(
    tool="Gatk4ApplyBqsr",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "ApplyBQSR"],
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("recalFile", File, prefix="--bqsr-recal-file"),
        ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".recal", extension=".bam"), prefix="--output"),
        ToolInput("createBamIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),
    ],
    outputs=[
        ToolOutput("out_bam", BamBai, selector=InputSelector("outputFilename"),secondaries_present_as={".bai": "^.bai"},)
    ],
)
```

You can save the file `part2/tools.py` and check the WDL translation for this tool with the following command:

```bash
janis translate part2/tools.py --name Gatk4ApplyBQSR_4_1_4 wdl
```

In the standard output you should see the translated wdl code. This is what the WDL command section should look like:
```
command <<<
    gatk ApplyBQSR \
      --input '~{bam}' \
      --reference '~{reference}' \
      --bqsr-recal-file '~{recalFile}' \
      --output '~{select_first([outputFilename, "~{basename(bam, ".bam")}.recal.bam"])}' \
      ~{if select_first([createBamIndex, true]) then "--create-output-bam-index" else ""}

>>>
```

## Adding these tools to our workflow

Now that we've created two tools, let's add these tools to our workflow. 
We will need to edit `part2/variantcaller.py` file.

You will notice that this is very similar to the `processing.py` workflow that we were working on in Part 1. We have pre-populated them with the solution from Part 1. 

```python
from janis_core import WorkflowBuilder, String, Array
  
# Import bioinformatics types
from janis_bioinformatics.data_types import (
    FastqGzPairedEnd,
    FastaWithIndexes,
    VcfTabix,
)

# Import bioinformatics tools
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)

# Add tools import here


# Construct the workflow here
w = WorkflowBuilder("preprocessingWorkflow")

# inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPairedEnd)
w.input("reference", FastaWithIndexes)
# add known_sites input here

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
    "samtoolsview", SamToolsView_1_9(sam=w.bwamem.out),
)

# Use `gatk4 MarkDuplicates` on the output of samtoolsview
#   - The output of BWA is query-grouped, providing "queryname" is good enough
w.step(
    "markduplicates",
    Gatk4MarkDuplicates_4_1_4(bam=w.samtoolsview.out, assumeSortOrder="queryname"),
)
# Use `gatk4 SortSam` on the output of markduplicates
#   - Use the "coordinate" sortOrder
w.step("sortsam", Gatk4SortSam_4_1_4(bam=w.markduplicates.out, sortOrder="coordinate",))

# Use `gatk4 SetNmMdAndUqTags` to calculate standard tags for BAM
w.step(
    "fix_tags", Gatk4SetNmMdAndUqTags_4_1_4(bam=w.sortsam.out, reference=w.reference,),
)

# Add the Base Quality Score Recalibration steps here!


```

Now we can add the following statements (below the `# Add tools import here` comment) to import our recently created tools:

```python
from tools import Gatk4BaseRecalibrator_4_1_4, Gatk4ApplyBQSR_4_1_4
```

### Adding a new input to workflow

BaseRecalibrator requires an input for its known sites, let's mirror this input on our variant caller workflow ( under `# Add known_sites input here`):

```python
w.input("known_sites", Array(VcfTabix))
```

> We'll use these two files from the reference folder for our testing later:
> - `reference/brca1_hg38_dbsnp138.vcf.gz`
> - `reference/brca1_hg38_known_indels.vcf.gz`

To add two new steps `baserecalibrator` and `applybqsr` into our workflow, add the following lines below the comment `# Add the Base Quality Score Recalibration steps here!`:

```python
# Generate the recalibration table from the bam in fix_tags
w.step(
    "baserecalibration",
    Gatk4BaseRecalibrator_4_1_4(
        bam=w.fix_tags.out, reference=w.reference, knownSites=w.known_sites
    ),
)

# Use the recalibration table to fix the bam from fix_tags
w.step(
    "applybqsr",
    Gatk4ApplyBQSR_4_1_4(
        bam=w.fix_tags.out,
        reference=w.reference,
        recalFile=w.baserecalibration.out_recalibration_report,
    ),
)
```

### Add output to our new workflow

To instruct Janis to collect the output files of this workflow, add the following lines to the end of the file:

```python
w.output("out_recalibration_table", source=w.baserecalibration.out_recalibration_report)
w.output("out_bam", source=w.applybqsr.out_bam)
```

### Final workflow definition

Your final workflow definition should look like the following:

```python
from janis_core import WorkflowBuilder, Array, String

# Import bioinformatics types
from janis_bioinformatics.data_types import (
    FastqGzPairedEnd,
    FastaWithIndexes,
    VcfTabix,
)

# Import bioinformatics tools
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)

# Add tools import here
from tools import (
    Gatk4BaseRecalibrator_4_1_4,
    Gatk4ApplyBQSR_4_1_4,
)

# Construct the workflow here
w = WorkflowBuilder("variantcaller")

# inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPairedEnd)
w.input("reference", FastaWithIndexes)
# add known_sites input here
w.input("known_sites", Array(VcfTabix))

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
    "samtoolsview", SamToolsView_1_9(sam=w.bwamem.out),
)

# Use `gatk4 MarkDuplicates` on the output of samtoolsview
#   - The output of BWA is query-grouped, providing "queryname" is good enough
w.step(
    "markduplicates",
    Gatk4MarkDuplicates_4_1_4(bam=w.samtoolsview.out, assumeSortOrder="queryname"),
)
# Use `gatk4 SortSam` on the output of markduplicates
#   - Use the "coordinate" sortOrder
w.step("sortsam", Gatk4SortSam_4_1_4(bam=w.markduplicates.out, sortOrder="coordinate",))

# Use `gatk4 SetNmMdAndUqTags` to calculate standard tags for BAM
w.step(
    "fix_tags", Gatk4SetNmMdAndUqTags_4_1_4(bam=w.sortsam.out, reference=w.reference,),
)

# Add the Base Quality Score Recalibration steps here!

# Generate the recalibration table from the bam in fix_tags
w.step(
    "baserecalibration",
    Gatk4BaseRecalibrator_4_1_4(
        bam=w.fix_tags.out, reference=w.reference, knownSites=w.known_sites
    ),
)

# Use the recalibration table to fix the bam from fix_tags
w.step(
    "applybqsr",
    Gatk4ApplyBQSR_4_1_4(
        bam=w.fix_tags.out,
        reference=w.reference,
        recalFile=w.baserecalibration.out_recalibration_report,
    ),
)

w.output("out_recalibration_table", source=w.baserecalibration.out_recalibration_report)
w.output("out_bam", source=w.applybqsr.out_bam)

```

## Running the new workflow

You can now save the file `part2/variantcaller.py` and try running the pipeline. 

We will use similar command as Part 1 with additional inputs `--known_sites`:

```bash
janis run -o part2 --development --keep-intermediate-files \
    part2/variantcaller.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --known_sites reference/brca1_hg38_dbsnp138.vcf.gz \
    --known_sites reference/brca1_hg38_known_indels.vcf.gz \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

At the end of pipeline execution, if you check: 

```bash
ls -lGH part2
```

You should see some additional output files being created. 

```bash
-rw-r--r-- 2 ec2-user 2696706 Jul 19 02:32 out_bam.bam
-rw-r--r-- 2 ec2-user     296 Jul 19 02:32 out_bam.bam.bai
-rw-r--r-- 2 ec2-user 1104446 Jul 19 02:32 out_recalibration_table.table
```

[Next >](3-adding-haplotypecaller.md)
# BCC2020 EAST - Janis Workshop (2.3)

In the previous workshop, we used tools from the Janis Bioinformatics toolbox. But what happens if you find a new tool!?

Today we're going to use the `janis.CommandToolBuilder` to teach Janis how to interact with command line software. We sometimes refer to this as "Wrapping a new tool" or "Creating a tool wrapper".

Importantly, every command line tool in Janis runs in a container. This means that all of our workflows are portable AND reproducible. Using containers means we also don't have to install the software on our computer.

Today, we're going to add 4 new GATK tools to Janis:

1. [SetNmMdAndUqTags](https://gatk.broadinstitute.org/hc/en-us/articles/360037067472-SetNmMdAndUqTags-Picard-) - calculated the NM, MD and UQ tags of a coordinate-sorted BAM.

2. [BaseRecalibrator](https://gatk.broadinstitute.org/hc/en-us/articles/360036898312-BaseRecalibrator) - Generates a recalibration table for ApplyBQSR.

3. [ApplyBQSR](https://gatk.broadinstitute.org/hc/en-us/articles/360037055712-ApplyBQSR) - Performs a base quality score recalibration using the table produced by BaseRecalibrator.

4. [HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller) - Our variant caller! Call germline SNPs and indels via local re-assembly of haplotypes.

We'll go through adding the first three, and then you can add HaplotypeCaller in the next exercise.

Note, we're going to use the official GATK docker container that the broad institute provides when building our tools: `broadinstitute/gatk:4.1.4.0`.


### Command line structure

There is some terminology that we use in this section that you should be familliar with. We'll look at a call to `samtools flagstat` to see how you can specify inputs to a tool

```bash
samtools flagstat [--threads n] <in.bam>
```

- Base command - `samtools flagstat` - this is that you would use to call the program. For example `"echo"`, `["bwa", "mem"]`, `["gatk", "MarkDuplicates"]`

- Option input - `--threads n` - (sometimes called a configuration input) these are preceded by a hyphen (`-`) and usually contain a value afterwards.

- Positional input - `<in.bam>` - This argument has no prefix, and usually comes _after_ the option inputs.

## Setup

You've already downloaded everything you need yesterday, but just in case:

```bash
mkdir janis-bcc2020 && cd janis-bcc2020
wget -q -O- "https://github.com/PMCC-BioinformaticsCore/janis-workshops/raw/bcc-2020/bcc2020/resources/bcc-data.tar" | tar -xz
```

We'll work out of the `day2` folder, there are four files:

1. `variantcaller.py` - This is our workflow from yesterday, and where we'll put our complete variant calling workflow.
2. `tools.py` - We'll add our new tools in here, and then import them into the `variantcaller.py`.
3. `variantcaller-solution.py` and `tools-solution.py` are the solutions to these exercises (don't peek)!

## Tool structure

We'll use the following template for our tools:

```python
ToolName = CommandToolBuilder(
    tool: str="toolname",
    base_command=["base", "command"],
    inputs=[],  # List[ToolInput]
    outputs=[], # List[ToolOutput]
    container="container/name:version",
    version="version"
)
```
- `tool` is a unique identifier of the tool.

- `base_command` is the command that you would use to call the container. For example `"echo"`, `["bwa", "mem"]`, `["gatk", "MarkDuplicates"]`

    > It's important to separate part of the base command, eg: `["bwa", "mem"`], not ~`"bwa mem"`~.

- `inputs` - A list of named inputs that the tool can receive (we'll see how this is structured soon)

- `outputs` - A list of named outputs that the tool will provide (we'll see how a tool can collect outputs soon)

- `container` - A docker container of the tool - technically any OCI compliant container is perfect, so you can use containers from `quay.io`.

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
	separate_value_from_prefix: bool = None,
	prefix_applies_to_all_elements: bool = None,
	presents_as: str = None,
	secondaries_present_as: Dict[str, str] = None,
	separator: str = None,
	shell_quote: bool = None,
	localise_file: bool = None,
	default: Any = None,
	doc: Optional[str] = None
)
```

### Tool outputs

We’ll use a `janis.ToolOutput` to collect and represent outputs. A ToolOutput has a type, and we can use a `selector` to get an output.

```
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

We can use different selectors to find out outputs, for example

- `InputSelector` - we can use the value of an input to find out output
- `WildcardSelector` - use a `glob` format to find an output, for example get all the bams in the execution directory with `WildcardSelector("*.bams")`.

We'll see how this works in our example.


## Building our tools

### GATK SetNmMdAndUqTags

This call is going to calculate the following tags by comparing our BAM to the reference genome:

- NM: Edit distance to the reference
- MD: String encoding mismatched and deleted reference bases
- UQ: Phred likelihood of the segment, conditional on the mapping being correct

> These are predefined standard tags from the [SAM specification](https://samtools.github.io/hts-specs/SAMtags.pdf).

In our reference script, `SetNmMdAndUqTags` might get called like this:

```bash
gatk SetNmMdAndUqTags \
    --INPUT input.bam \
    --REFERENCE_SEQUENCE ~{ref_fasta}
    --OUTPUT ~{output_bam_basename}.bam \
    --CREATE_INDEX
```

Now although there are _MANY_ options that we could call SetNmMdAndUqTags, we'll just focus on the ones we'll use. 

Let's start by filling in our initial details:

```python
Gatk4SetNmMdAndUqTags_4_1_4 = CommandToolBuilder(
    tool="Gatk4SetNmMdAndUqTags",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "SetNmMdAndUqTags"],
    # let's look at these in a second
    inputs=[],  # List[ToolInput]
    outputs=[], # List[ToolOutput]
)
```


Let's break the inputs the individual components:

Here, we see 4 inputs, all of which have a prefix (no positional arguments):

- `--INPUT` - The BAM or SAM file to fix.
- `--REFERENCE_SEQUENCE` - Reference sequence file (with indexes).
- `--OUTPUT` - A filename of the output file.
- `--CREATE_INDEX` - Whether to create a BAM index when writing a coordinate-sorted BAM file. Note, this will use the format `outputfilename.bai`. We'll talk more about this soon.

For the `--OUTPUT` input, we're going to use the special `janis.Filename` type, which will generate a name for our input.

Let's see how we might translate these inputs to Janis:

```python
Gatk4SetNmMdAndUqTags_4_1_4 = CommandToolBuilder(
    # ...other fields
    inputs=[
        ToolInput("bam", Bam(), prefix="--INPUT"),
        ToolInput("reference", FastaWithIndexes, prefix="--REFERENCE_SEQUENCE"),
        ToolInput("outputFilename", Filename(suffix=".fixed", extension=".bam"), prefix="--OUTPUT"),
        ToolInput("createIndex", Boolean(), prefix="--CREATE_INDEX", default=True),
    ]
    outputs=[]
)
```

We know from the command line that this tool is going to write a file to the location of `--OUTPUT`, and we use `janis.Filename` class to generate a filename which gets used. We can use the value of the input `outputFilename` by using the `janis.InputSelector`. 

Additionally, Janis expects the BamIndex

```python
Gatk4SetNmMdAndUqTags_4_1_4 = CommandToolBuilder(
    # ...other fields
    inputs=[
        #...
        ToolInput(
            "outputFilename", 
            Filename(suffix=".fixed", extension=".bam"),
            prefix="--OUTPUT"
        ),
        #...
    ]
    outputs=[
        ToolOutput(
            "out_bam", 
            BamBai, 
            selector=InputSelector("outputFilename"),
            secondaries_present_as={".bai", "^.bai"}
        )
    ]
)
```

Woah. There were a lot of new concepts in there. But jumping in the deep-end is the best way to learn.  I promise the next tools are going to be easier.

```python
Gatk4SetNmMdAndUqTags_4_1_4 = CommandToolBuilder(
    tool="Gatk4SetNmMdAndUqTags",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "SetNmMdAndUqTags"],
    inputs=[
        ToolInput("bam", Bam(), prefix="--INPUT"),
        ToolInput("reference", FastaWithIndexes, prefix="--REFERENCE_SEQUENCE"),
        ToolInput(
            "outputFilename",
            Filename(suffix=".fixed", extension=".bam"),
            prefix="--OUTPUT",
        ),
        ToolInput("createIndex", Boolean(), prefix="--CREATE_INDEX", default=True),
    ],
    outputs=[
        ToolOutput(
            "out_bam", 
            BamBai, 
            selector=InputSelector("outputFilename"),
            secondaries_present_as={".bai", "^.bai"}
        )
    ],
)
```



## GATK BaseRecalibrator

```python

Gatk4BaseRecalibrator_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## GATK GatherBQSRReports

```python

Gatk4GatherBQSRReports_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## GATK ApplyBqsr

```python

Gatk4ApplyBqsr_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## Chaining tools to workflow

```python
    self.step("")
    self.step("")
    self.step("")
    self.step("")

```

## Run with the test data from yesterday

```bash
    janis run processing2.py
```

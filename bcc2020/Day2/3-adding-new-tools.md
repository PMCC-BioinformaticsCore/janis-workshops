# BCC2020 EAST - Janis Workshop (2.3)

In the previous workshop, we used tools from the Janis Bioinformatics toolbox. But what happens if you find a new tool!?

Today we're going to use the `janis.CommandToolBuilder` to teach Janis how to interact with command line software. We sometimes refer to this as "Wrapping a new tool" or "Creating a tool wrapper".

Importantly, every command line tool in Janis runs in a container. This means that all of our workflows are portable AND reproducible. Using containers means we also don't have to install the software on our computer.

Today, we're going to add 4 new GATK tools to Janis:

1. [BaseRecalibrator](https://gatk.broadinstitute.org/hc/en-us/articles/360036898312-BaseRecalibrator) - Generates a recalibration table for ApplyBQSR.

2. [ApplyBQSR](https://gatk.broadinstitute.org/hc/en-us/articles/360037055712-ApplyBQSR) - Performs a base quality score recalibration using the table produced by BaseRecalibrator.

3. [HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller) - Our variant caller! Call germline SNPs and indels via local re-assembly of haplotypes.

We'll go through adding the first two, and then you can add HaplotypeCaller in the next exercise.

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
wget -q -O- "https://github.com/PMCC-BioinformaticsCore/janis-workshops/raw/master/bcc2020/resources/bcc-data.tar" | tar -xz
```

We'll work out of the `day2` folder.


```bash
$ cd day2
$ ls -lGh
```

There are 4 files:

1. `variantcaller.py` - This is our workflow from yesterday, and where we'll put our complete variant calling workflow.
2. `tools.py` - We'll add our new tools in here, and then import them into the `variantcaller.py`.
3. `variantcaller_solution.py` and `tools_solution.py` are the solutions to these exercises (don't peek)!

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

## GATK BaseRecalibrator

BaseRecalibrator generates a recalibration table for Base Quality Score Recalibration (BQSR). You might call BaseReclibrator like the following:

```bash
gatk BaseRecalibrator \
   --input my_reads.bam \
   --reference reference.fasta \
   --output recal_data.table \
   --known-sites sites_of_variation.vcf \
   --known-sites another/optional/setOfSitesToMask.vcf
```

> We'll include `--known-sites` in our tool wrapper, but we don't provide example data for this workshop.

Let's fill in the basic details of the tool:

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

### Inputs

Alright, let's decode the different inputs we see to a corresponding ToolInput:

- `--input` - Our input bam. Note, Janis likes BamIndexes to look like `.bam.bai`, Janis supports rewriting this index with `secondaries_present_as`.

    ```python
    ToolInput("bam", BamBai, prefix="-I", secondaries_present_as={".bai": "^.bai"})
    ```

- `--reference` - Reference sequence file (fasta with indexes):

    ```python
    ToolInput("reference", FastaWithIndexes, prefix="-R")
    ```

- `--output` - The filename of the output recalibration table. This is not an input file, but a generated filename. For this reason, we'll use the `janis.Filename` class to generate a filename:

    ```python
    ToolInput("outputFilename", Filename(extension=".table"), prefix="--output"),
    ```

- `--known-sites` - An array of known sites (gzipped compressed and tabix indexed VCF: `VcfTabix`). Note that the prefix applies to each element in the array. We

    ```python
    ToolInput("knownSites", Array(VcfTabix), prefix="--known-sites", prefix_applies_to_all_elements=True)
    ```

This gives definition as:

```python
Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    # ... other params
    inputs=[
        ToolInput("bam", BamBai, prefix="-I", secondaries_present_as={".bai": "^.bai"}),
        ToolInput("reference", FastaWithIndexes, prefix="-R"),
        ToolInput("outputFilename", Filename(extension=".table"), prefix="--output"),
        ToolInput(
            "knownSites",
            Array(VcfTabix),
            prefix="--known-sites",
            prefix_applies_to_all_elements=True,
        ),
    ],
    outputs=[],  # List[ToolOutput]
)
```


### Outputs

Our BaseRecalibrator has one output, the recalibration table specified by `--output` (fed by our input called `outputFilename`).

We can use an `InputSelector` to get the `outputFilename` value to choose our output. This might look like the following:

```python
ToolOutput("out_recalibration_report", File, selector=InputSelector("outputFilename"))
```

### Final tool definition

This gives the following tool definition as:

```python
Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    tool="Gatk4BaseRecalibrator",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "BaseRecalibrator"],
    # we'll look at these next
    inputs=[
        ToolInput("bam", BamBai, prefix="-input", secondaries_present_as={".bai": "^.bai"}),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("outputFilename", Filename(extension=".table"), prefix="--output"),
        ToolInput(
            "knownSites",
            Array(VcfTabix),
            prefix="--known-sites",
            prefix_applies_to_all_elements=True,
        ),
    ],
    outputs=[
        ToolOutput(
            "out_recalibration_report", File, selector=InputSelector("outputFilename")
        )
    ],
)
```

### Translate

When translating a file of multiple tool definitions, it's good practice to specify the `--name` of the tool, eg:

```bash
janis translate day2/tools.py --name Gatk4BaseRecalibrator_4_1_4 wdl
```

Look how closely our command section mirrors the command we're trying to replicate!

```wdl
command <<<
    # you might have extra statements here
    gatk BaseRecalibrator \
        --input '~{bam}' \
        --reference '~{reference}' \
        --output '~{select_first([outputFilename, "generated.table"])}' \
        ~{"--known-sites '" + sep("' --known-sites  '", knownSites) + "'"}
>>>

```

## GATK ApplyBQSR

We'll apply a similar treatment for ApplyBQSR:

Command:

```bash
gatk ApplyBQSR \
   --input input.bam \
   --reference reference.fasta \
   --bqsr-recal-file recalibration.table \
   --output output.bam \
   --create-output-bam-index
```

### Inputs

Very similar arguments apply to each tool input here:

- `--output` is a generated filename,
- `--create-output-bam-index` is an optional Boolean, which we'll default to true

```python
Gatk4ApplyBQSR_4_1_4 = CommandToolBuilder(
    # other fields
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("recalFile", File, prefix="--bqsr-recal-file"),
        ToolInput(
            "outputFilename",
            Filename(
                prefix=InputSelector("bam"), suffix=".recalibrated", extension=".bam"
            ),
	    prefix="--output",
        ),
        ToolInput(
            "createBamIndex",
            Boolean(optional=True),
            prefix="--create-output-bam-index",
            default=True,
        ),
    ],
    outputs=[]
```

### Outputs

We have one indexed bam as an output, than is named through the `outputFilename` (we'll need to perform the same `present_secondaries_as` treatment):

```python
ToolOutput(
    "out_bam",
    BamBai,
    selector=InputSelector("outputFilename"),
    secondaries_present_as={".bai": "^.bai"},
)
```

### Final tool

This should leave you the final tool:

```python
Gatk4ApplyBQSR_4_1_4 = CommandToolBuilder(
    tool="Gatk4ApplyBQSR",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "ApplyBQSR"],
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("recalFile", File, prefix="--bqsr-recal-file"),
        ToolInput(
            "outputFilename",
            Filename(
                prefix=InputSelector("bam"), suffix=".recalibrated", extension=".bam"
            ),
	    prefix="--output",
        ),
        ToolInput(
            "createBamIndex",
            Boolean(optional=True),
            prefix="--create-output-bam-index",
            default=True,
        ),
    ],
    outputs=[
        ToolOutput(
            "out_bam",
            BamBai,
            selector=InputSelector("outputFilename"),
            secondaries_present_as={".bai": "^.bai"},
        )
    ],
)
```

You can now exit vim agin and check the translated tool with:

```bash
janis translate day2/tools.py --name Gatk4ApplyBQSR_4_1_4 wdl
```

Command:
```
command <<<
    gatk ApplyBQSR \
        --input '~{bam}' \
        --reference '~{reference}' \
        --bqsr-recal-file '~{recalFile}' \
        ~{if defined(select_first([createBamIndex, true])) then "--create-output-bam-index" else ""}
    # other statements here
>>>
```

## Adding these tools to our workflow

Now that we've created two tools, let's add them to our `variantcaller.py`, open up this file:

```bash
vim day2/variantcaller.py
```

Now we can add the following statments on L16 (below the `# Add tools import here` comment) to import our recently created tools:

```python
from tools import Gatk4BaseRecalibrator_4_1_4, Gatk4ApplyBQSR_4_1_4
```

### Adding a new input

BaseRecalibrator requires an input for its known sites, let's mirror this input on our variant caller workflow (on L36, under `# Add known_sites input here`):

```python
w.input("known_sites", Array(VcfTabix))
```

> We'll use the two files from the reference folder:
> - `reference/brca1_hg38_dbsnp138.vcf.gz`
> - `reference/brca1_hg38_known_indels.vcf.gz`

We can then add two new steps for `baserecalibrator` and `applybqsr` to the bottom of the same file`:

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

## Running the new workflow

Add a few outputs to our workflow to check that our workflow:

```python
w.output("out_recalibration_table", source=w.w.baserecalibration.out_recalibration_report)
w.output("out_bam", source=w.applybqsr.out_bam)
```

Then you can run the following command (adding a new `--known_sites` input):

```bash
janis run -o day2 --development \
    day2/variantcaller_solution.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --known_sites reference/brca1_hg38_dbsnp138.vcf.gz \
    --known_sites reference/brca1_hg38_known_indels.vcf.gz \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

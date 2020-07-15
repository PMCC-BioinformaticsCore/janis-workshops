# BCC2020 EAST - Janis Workshop (1.3)

## Building alignment workflow 
In this stage, we are going to build a simple workflow to align short reads of DNA. 

1. Start with a pair of compressed `FASTQ` files,
2. Align these reads using `BWA MEM` into an uncompressed `SAM` file (the _de facto_ standard for short read alignments),
3. Compress this into the binary equivalent `BAM` file using `samtools`, and finally
4. Sort the reads using `GATK4 SortSam`.

These tools already exist within the Janis Tool Registry, you can see their documentation online:

- [BWA MEM](https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html)
- [Samtols View](https://janis.readthedocs.io/en/latest/tools/bioinformatics/samtools/samtoolsview.html)
- [GATK4 Mark Duplicates](https://janis.readthedocs.io/en/latest/tools/bioinformatics/gatk4/gatk4markduplicates.html)

## Creating our file

A Janis workflow is a Python script, so we can start by creating a file called `alignment.py` and importing Janis.

```bash
mkdir part3 && mkdir tools
vim tools/alignment.py # or vim, emacs, sublime, vscode
```

From the `janis_core` library, we're going to import `WorkflowBuilder` and a `String`:

```python
from janis_core import WorkflowBuilder, String
```

## Imports

We have four inputs we want to expose on this workflow:

1. Sequencing Reads (`FastqGzPair` - paired end sequence)
2. Sample name (`String`)
3. Read group header (`String`)
4. Reference files (`Fasta` + index files (`FastaWithIndex`))

We've already imported the `String` type, and we can import `FastqGzPair` and `FastaWithIndex` from the `janis_bioinformatics` registry:

```python
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict
```

### Tools

We've discussed the tools we're going to use. The documentation for each tool has a row in the tbale caled "Python" that gives you the import statement. This is how we'll import how tools:


```python
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
```



## Declaring our workflow

We'll create an instance of the [`WorkflowBuilder`](https://janis.readthedocs.io/en/latest/references/workflow.html#janis.Workflow) class, this just requires a name for your workflow (can contain alphanumeric characters and underscores).

```python
w = WorkflowBuilder("alignmentWorkflow")
```

A workflow has 3 methods for building workflows:

- `workflow.input` - Used for creating inputs,
- `workflow.step` - Creates a step on a workflow,
- `workflow.output` - Exposes an output on a workflow.

We give each input / step / output a unique identifier, which then becomes a node in our workflow graph. We can refer to the created node using _dot-notation_ (eg: `w.input_name`). We'll see how this works in the later sections.

More information about each step will be linked from this page about the [`Workflow` and `WorkflowBuilder` class](https://janis.readthedocs.io/en/latest/references/workflow.html).


### Creating inputs on a workflow

> Further reading: [Creating an input](https://janis.readthedocs.io/en/latest/references/workflow.html#creating-an-input)

To create an input on a workflow, you can use the `Workflow.input` method, which has the following structure:

```python
Workflow.input(
    identifier: str, 
    datatype: DataType, 
    default: any = None, 
    doc: str = None
)
```

An input requires a unique identifier (string) and a DataType (String, FastqGzPair, etc). Let's prepare the inputs for our workflow:


```python
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPair)
w.input("reference", FastaWithDict)
```

### Declaring our steps and connections

> Further reading: [Creating a step](https://janis.readthedocs.io/en/latest/references/workflow.html#creating-a-step)

Similar to exposing inputs, we create steps with the `Workflow.step` method. It has the following structure:

```python
Workflow.step(
    identifier: str, 
    tool: janis_core.tool.tool.Tool, 
    scatter: Union[str, List[str], ScatterDescription] = None, 
)
```

We provide a identifier for the step (unique amongst the other nodes in the workflow), and intialise our tool, passing our inputs of the step as parameters.

We can refer to an input (or previous result) using the dot notation. For example, to refer to the `fastq` input, we can use `w.fastq`.

#### BWA MEM

We use [bwa mem's documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html) to determine that we need to provide the following inputs:

- `reads`: `FastqGzPair`            (connect to `w.fastq`)
- `readGroupHeaderLine`: `String`   (connect to `w.read_group`)
- `reference`: `FastaWithDict`      (connect to `w.reference`)

We can connect them to the relevant inputs to get the following step definition:

```python
w.step(
    "bwamem",   # identifier
    BwaMemLatest(
        reads=w.fastq,
        readGroupHeaderLine=w.read_group,
        reference=w.reference
    )
)
```

#### Samtools view

We'll use a very similar pattern for Samtools View, except this time we'll reference the output of `bwamem`. From bwa mem's documentation, there is one output called `out` with type `Sam`. We'll connect this to `SamtoolsView` only input, called `sam`.


```python
w.step(
    "samtoolsview",
    SamToolsView_1_9(
        sam=w.bwamem.out
    )
)
```

#### SortSam

In addition to connecting the output of `samtoolsview` to Gatk4 SortSam, we want to tell SortSam to use the following values:

- sortOrder: `"coordinate"`
- createIndex: `True`

Instead of connecting an input or a step, we just just provide the literal value.

```python
w.step(
    "sortsam",
    Gatk4SortSam_4_1_2(
        bam=w.samtoolsview.out,
        sortOrder="coordinate",
        createIndex=True
    )
)
```

### Exposing outputs

> Further reading: [Creating an output](https://janis.readthedocs.io/en/latest/references/workflow.html#creating-an-output)

Outputs have a very similar syntax to both inputs and steps, they take an `identifier` and a named `source` parameter. Here is the structure:

```python
Workflow.output(
    identifier: str,
    datatype: DataType = None,
    source: Node = None,
    output_folder: List[Union[String, Node]] = None,
    output_name: Union[String, Node] = None
)
```

Often, we don't want to specify the output data type, because we can let Janis do this for us. We'll talk about the `output_folder` and `output_name` in the next few sections. For now, we just have to specify an output identifier and a source.

```python
w.output("out", source=w.sortsam.out)
```

## Workflow + Translation

Hopefully you have a workflow that looks like the following!

```python
from janis_core import WorkflowBuilder, String

from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict

from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2

w = WorkflowBuilder("alignmentWorkflow")

# Inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPair)
w.input("reference", FastaWithDict)

# Steps
w.step(
    "bwamem", 
    BwaMemLatest( 
        reads=w.fastq, 
        readGroupHeaderLine=w.read_group, 
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
        createIndex=True
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
janis run -o part3 tools/alignment.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

## Debugging a run

Workflows do not always run smoothly, and for that it is useful to understand how workflows run, and how Janis can help you solve the problems. 

The Janis documentation contains some answers for:

- [Frequently asked questions](https://janis.readthedocs.io/en/latest/references/faq.html)
- [Common errors](https://janis.readthedocs.io/en/latest/references/errors.html)

In this section, we are going to investigate inside the `janis` folder, and look at how Cromwell structures the execution to give us a better idea how workflows are run.

### Execution folder notes

Usually when a workflow is a success, Janis automatically removes the intermediate input files. In the previous section, we ran an alignment workflow with `--keep-intermediate-files`, which means these files will persist even when the worklfow succeeded.

By default, the execution directory is under `$outputdir/janis/execution/`. Cromwell places the execution under two additional subfolders (workflow name, engine id). The exact task execution directory can be found from the progress screen as `executionDir`.

## Looking inside Janis directory

Our previous execution directory `part2` (`$HOME/janis-workshop1/part2`) contains a number of outputs, let's look at it using `ls`:

```
$ ls part2

drwxr-xr-x  franklinmichael  320B  janis
-rw-r--r--  franklinmichael  2.8M  out.bam
-rw-r--r--  franklinmichael  1.4M  out.bam.bai
```

We see our outputs `out.bam*`, let's look inside the `janis` directory:

```
$ ls part2/janis/
total 136
drwxr-xr-x  franklinmichael    96B  configuration
drwxr-xr-x  franklinmichael    64B  database
drwxr-xr-x  franklinmichael   128B  execution
drwxr-xr-x  franklinmichael   320B  logs
drwxr-xr-x  franklinmichael    96B  metadata
-rw-r--r--  franklinmichael    68K  task.db
drwxr-xr-x  franklinmichael   300B  workflow
```

There are a couple we'll highlight:

- `execution/`: Cromwell will place intermediate execution in this folder 
- `logs/`: Contains logs and stdout / stderr
- `workflow/` Contains the WDL (/ CWL) translation of the workflow + tools and the inputs
- `task.db`: An SQLite database that Janis uses to store metadata about the workflow run.

And a brief explanation fo the other folders
- `configuration/`: Any files required to configure Cromwell or a database
- `database/`: Contains database files for an engine (if relevant)
- `metadata/`: Contains raw metadata from the engine (if relevant)

### Inside the execution directory

Cromwell additionally scopes the execution directory inside two additional directories (WorkflowName/internal EngineID). The `executionDir` field in the progress screen gives you the direct link, let's look inside:

```
$ ls part2/janis/execution/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb

drwxr-xrwx  mfranklin 4.3K  call-bwamem
drwxr-xrwx  mfranklin 2.2M  call-cutadapt
drwxr-xrwx  mfranklin 2.2M  call-sortsam
```

Each `call-*` folder has two subdirectories:

- `execution` - The CWD for a task's execution.
- `inputs` - Where the inputs are localised within each task.


 The `execution` subdirectory which has the following structure:

- `rc`: Return code
- `script`: The script that runs inside the singularity container
- `script.submit`: The script that Cromwell executes to submit the job (contains the sbatch)
- `std*` - Stdout and stderr
- Often there will be a `std(err | out).submit`, which is the `std*` for the submit script, in our case it will usually just contain the job id.

Let's look at the `script` for `sortsam`:

```
$ less $HOME/janis-workshop1/part2/janis/execution/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb/call-sortsam/execution/script

[... other details]
gatk SortSam \
  -I /cromwell-executions/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb/call-sortsam/inputs/1281140437/generated.bam \
  -O generated.bam \
  -SO coordinate \
  --CREATE_INDEX \
  --MAX_RECORDS_IN_RAM 5000000 \
  --TMP_DIR . \
  --VALIDATION_STRINGENCY SILENT \
[... other details]
```

You'll notice that the input starts with `/cromwell-executions/BwaAligner` instead of the full path. This is because task execution get's placed inside a container.

## What happens when something goes wrong?

Workflows can fail for a variety of reasons, such as:

- A task may fail because:
    - Inputs are invalid (missing, incorrect format, invalid per spec)
    - Resources error (network, filesystem problems, unable to access resources)
    - Host problems (memory problems, cpu issues, time limits)
    - Doesn't write the outputs correctly
- and a myriad more problems.

Janis + Cromwell do their best to catch these problems and report them back to a user. Here's an example of a failed workflow, and how Janis may present it.

```
WID:        cee9f0
EngId:      f54e4868-2005-4f1f-a630-6e2b90b289e6
Name:       BwaAligner
Engine:     cromwell (localhost:53668) [PID=57172]

Task Dir:   $HOME/workshop1/failed
Exec Dir:   $HOME/workshop1/failed/janis/execution/BwaAligner/f54e4868-2005-4f1f-a630-6e2b90b289e6

Status:     Failed
Duration:   58s
Start:      2020-02-07T05:00:27.682668+00:00
Finish:     2020-02-07T05:01:26.110000+00:00
Updated:    Just now (2020-02-07T05:01:32+00:00)

Jobs: 
    [✓] cutadapt (7s)
    [!] bwamem (13s)
            stdout: $HOME/workshop1/failed/janis/execution/BwaAligner/f54e4868-2005-4f1f-a630-6e2b90b289e6/call-bwamem/execution/stdout
            stderr: $HOME/workshop1/failed/janis/execution/BwaAligner/f54e4868-2005-4f1f-a630-6e2b90b289e6/call-bwamem/execution/stderr       

Error: Job BwaAligner.bwamem:NA:1 exited with return code -1 which has not been declared as a valid return code. See 'continueOnReturnCode' runtime attribute for more details.:
```

This indicates to us that `bwamem` failed, and it tries to prompt us with the locations of `stdout` / `stderr`. Note that depending on the failure, these might not exist. But the execution folder is a good start: `$HOME/workshop1/failed/janis/execution/BwaAligner/f54e4868-2005-4f1f-a630-6e2b90b289e6/call-bwamem/execution/`.
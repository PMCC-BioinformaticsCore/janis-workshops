# Introduction to Janis at Peter Mac

Janis is workflow framework that uses Python to construct a declarative workflow. It has a simple workflow API within Python that you use to build your workflow. Janis converts your pipeline to the Common Workflow Language (CWL) and Workflow Description Language (WDL) for execution, and it’s also great for publishing and archiving.

Janis can run pipelines at Peter Mac, as it knows how to interact with Slurm.

This tutorial has a bioinformatics focus, although Janis is generic as a workflow assistant and can be used outside of the computational genomics.

## Learning outcomes

In this workshop, we'll learn:

- What is Janis, 
    - How Janis is different from seqliner
- How to load a Janis environment,
- How to run a simple workflow,
- How to align some samples.
- How to debug if something goes wrong (check logs)
- How to override amount of resources
- How to run same pipeline on cohort of samples,


## Foundations

- A workflow is a collection of tools are run in an organised manner.

- A workflow specification is a format that exactly describes the relatinoship between your tools. Popular workflow specification types include:

    - Common Workflow Language (CWL)
    - Workflow Description Language (WDL)
    - [_Unsupported_] Nextflow
    - [_Unsupported_] Snakemake

- Janis uses an _abstracted execution environment_ which removes the shared file system you're used to.

    - For a file or directory to be available to your tool, you need to EXPLICITLY include it. 
        - This includes associated files, if you want an indexed bam, you must use the BamBai type.

    - Outputs of tools must be EXPLICITLY collected, else they will be removed.
        - This is equivalent to a _SAVE_ stage in seqliner.

    - A step's requirements (its inputs) can be an input to a workflow, or the output of a previous step (hence creating a dependency).

    _Diagram_

- In Janis, all tasks are executed inside a isolated virtual environment called a [_Container_](https://www.docker.com/resources/what-container). Docker and Singularity are two common container types. (Docker containers can be executed by Singularity.)


## Getting started

Create a folder called `janis-workshop1` in a location where you have plenty of storage (we'd recommend you researcher folder).

> Copy this `<path to data>` to your local 

## Loading and configuring Janis

1. Load Janis through the module system

```
module load janis/0.9.0
```

2. [First run only] Initialize Peter Mac template

```
janis init pmac
```

By default, your configuration is placed at `~/.janis/janis.conf`. You can see and edit some of these details with `vim ~/.janis/janis.conf`:


```yaml
engine: cromwell
notifications:
    email: null
template:
    id: pmac
    catch_slurm_errors: false
    send_job_emails: false
```

This configuration tells Janis (and Cromwell) how to interact with Slurm and Singularity.

## Running workflows with Janis

Let's run the following command to see how to configure Janis when running a workflow:

```
janis run -h
```

```
usage: janis run [-h] [-i INPUTS] [-o OUTPUT_DIR] [-B] 
                 [--keep-intermediate-files] [...OTHER OPTIONS]
                 workflow [...WORKFLOW INPUTS]
```

> It's important that these configuration options come AFTER the `run`, but before the `$workflowname`. Any inputs after the `$workflowname` are passed as inputs to the workflow.

We'll highlight a few options:

- `-o OUTPUT_DIR, --output-dir OUTPUT_DIR` - [REQUIRED] This directory to copy outputs to. By default intermediate results are within a janis/execution subfolder (unless overriden by a template)

- `-i INPUTS, --inputs INPUTS` - YAML or JSON inputs file to provide values for the workflow (can specify multiple times)

- `-B, --background` - Run the workflow engine in the background (or submit to a cluster if your template supports it)

- `--keep-intermediate-files` - Do not remove execution directory on successful complete


## Running a test workflow

We'll run a simple workflow called ([`Hello`](https://janis.readthedocs.io/en/latest/tools/unix/hello.html)) to make sure that Janis is configured properly. This workflow prints "Hello, World" to the console. This tests that Janis is installed and that you can submit to the cluster correctly.

> We must specify an output directory (`-o`) to contain the execution and outputs, we'll ask Janis to create a subdirectory called `part1`:

```
janis run -o part1 hello
```

This command will:

- Create an output directory called `part1` (relative to the current directory),
- start Cromwell,
- submit to the cluster and run a task that calls "echo",
- collect the results.


You'll see logs from Cromwell in the terminal. There's a number of statements that are worth highlighting:

```
# 1. Your Workflow ID
[INFO]: Starting task with id = 'c83484'

# 2. The process ID of cromwell (in case of an intermittent failure)
Cromwell is starting with pid=14497

# 3. Cromwell started successfully running the job.
2020-01-31T12:58:46 [INFO]: Status changed to: Running

# 4. The task has completed successfully 
2020-01-31T12:59:05 [INFO]: View the task outputs: file://$HOME/janis-workshop1/part1
```

In our output folder, there are two items (`ll part1`):
```
drwxr-sr-x 8 mfranklin punim0755 133K Jan 31 12:59 janis
-rw-r--r-- 1 mfranklin punim0755   14 Jan 31 12:58 out
```

The output to the task is called `out`, as this is the name of the output that the `hello` tool specifies. The `janis` folder contains information about the execution, including logs.


### Running in the background

We've run the workflow within our terminal session. But often our workflow is too long to run in one session and it would be useful to submit the workflow to the cluster.

The Peter Mac configuration can submit to the janis partition on the cluster when the `--background` (`-B`) parameter is provided.

Let's run the same workflow with a new output directory (`part2`), except now providing the background parameter. Janis quickly returns with our workflow ID, which we can capture by running:

```
wid=$(janis run --background -o part2 hello)
```

We can track the progress of our workflow with:

```
janis watch $wid
```

You will see a progress screen like the following 

```
WID:        d12763
EngId:      291b6f91-6246-4ded-934b-98773e265ead
Name:       hello
Engine:     cromwell (localhost:53489) [PID=43580]

Task Dir:   /Users/franklinmichael/source/CWLab/test2
Exec Dir:   /Users/franklinmichael/source/CWLab/test2/janis/execution/hello/291b6f91-6246-4ded-934b-98773e265ead

Status:     Completed
Duration:   44s
Start:      2020-01-31T02:49:35.968005+00:00
Finish:     2020-01-31T02:50:20.305000+00:00
Updated:    Just now (2020-01-31T02:50:28+00:00)

Jobs: 
    [✓] hello (11s)       

Outputs:
    - out: /Users/franklinmichael/source/CWLab/test2/out
```

## Aligning a set of samples

Janis comes with a number of prebuilt pipelines. We're going to use the [BWAAligner](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html) (Cutadapt + BwaMem + Samtools + SortSam) to turn out a fastq pair into an indexed Bam.

By looking at the documentation for this tool: https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html

We see that the tool requires:

- `sample_name` - String
- `reference` - FastaWithDict
- `fastq` - FastqGzPair

and will return an indexed bam (`.bam` + `.bam.bai`) called `out`.

We're also going to add `--keep-intermediate-files` as it will be useful for the next section.

> The order of arugments is important here

Let's run the workflow!

```
janis run -B --keep-intermediate-files BwaAligner --sample_name NA12878 --fastq data/align/BRCA1_R*.fastq.gz
```

```
WID:        ed6702
EngId:      a07054bd-aa50-417e-a3e6-af3e62dd98cb
Name:       BwaAligner
Engine:     cromwell (localhost:49681) [PID=31868]

Task Dir:   $HOME/janis-workshop1/test2
Exec Dir:   $HOME/janis-workshop1/test2/janis/execution/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb

Status:     Completed
Duration:   3m:08s
Start:      2020-01-31T03:50:27.112017+00:00
Finish:     2020-01-31T03:53:35.184000+00:00
Updated:    10s ago (2020-01-31T03:53:40+00:00)

Jobs: 
    [✓] cutadapt (43s)
    [✓] bwamem (1m:14s)
    [✓] sortsam (31s)       

Outputs:
    - out: $HOME/janis-workshop1/test2/out.bam
```

At `test2/out.bam`, we have our aligned sample.



## Debug if something goes wrong

Workflows don't always run smoothly, and there are a few things that Janis does that can help. Here are two guides that are worth checking out:

- [Frequently asked questions](https://janis.readthedocs.io/en/latest/references/faq.html)
- [Common errors](https://janis.readthedocs.io/en/latest/references/errors.html)


In this section, we're going to investigate inside an execution to get an appreciation for how Cromwell runs a workflow, and to determine some common errors.

Usually when a workflow is a success, Janis automatically removes the intermediate input files. In the previous section, we ran an alignment workflow with `--keep-intermediate-files`, which means these files will persist even if the worklfow succeded.

By default, the execution directory is under `$outputdir/janis/execution/`. Cromwell places the execution under two additional subfolders (workflow name, engine id). The direct task execution directory can be found from the progress screen.

Inside this directory, there will be a `call-$taskname` for each task in the workflow

```
drwxr-xrwx 4 mfranklin punim0755 4.3K Jan 31 15:55 call-bwamem
drwxr-xrwx 5 mfranklin punim0755 2.2M Jan 31 15:55 call-cutadapt
drwxr-xrwx 5 mfranklin punim0755 2.2M Jan 31 15:56 call-sortsam
```

Each `call-*` folder has an `execution` subdirectory which has the following structure:

- `rc`: Return code
- `script`: The script that runs inside the singularity container
- `script.submit`: The script that Cromwell executes to submit the job (contains the sbatch)
- `std*` - Stdout and stderr
- Often there will be a `std(err | out).submit`, which is the `std*` for the submit script, in our case it will usually just contain the job id.

## Janis multirun

_TBA_










## Advanced functionality

Here's some advanced functionality of Janis:

- Scattering by multiple fields (dot + cross product)
- Output naming
- Python Tool for arbitrary code execution
- Cloud execution of workflows


# Workshop 1.3 - Running workflows with Janis

Let's run the following command to see how to configure Janis when running a workflow:

```
$ janis run -h

usage: janis run [-h] [-i INPUTS] [-o OUTPUT_DIR] [-B] 
                 [--keep-intermediate-files] [...OTHER OPTIONS]
                 workflow [...WORKFLOW INPUTS]
```

> It's important that these configuration options come AFTER the `run`, but before the `<workflow>` argument. Any parameters after the `<workflow>` are passed as inputs to the workflow.

We'll highlight a few options:

- `-o OUTPUT_DIR, --output-dir OUTPUT_DIR` - [REQUIRED] This directory to copy outputs to. By default intermediate results are within a janis/execution subfolder (unless overriden by your configuration)

- `-i INPUTS, --inputs INPUTS` - YAML or JSON inputs file to provide values for the workflow (can specify multiple times)

- `-B, --background` - Run the workflow engine in the background (or submit to a cluster if your template supports it)

- `--keep-intermediate-files` - Do not remove execution directory on successful complete


## How does Janis run a workflow?

As discussed in the introduction, the janis-assistant leverages community driven engines to run workflows. For our workflows at Peter Mac, we use the [Cromwell](https://github.com/broadinstitute/cromwell) execution engine, configured to work with [Slurm + Singularity](https://cromwell.readthedocs.io/en/stable/tutorials/Containers/). 

For our tests, Janis will:

- Start up a Cromwell instance,
- Convert the workflow to WDL (which Cromwell supports),
- Submits this WDL workflow to Cromwell,
- Watches the progress of the workflow,
- Performs a number of tasks after the workflow is completed.

The limitations with this include:

- Increased complexity to run a workflow
- Issues with running may become harder to find.

It's important to note that building workflows in Janis does NOT limit you to running with Janis. You are free to take the exported CWL and WDL specifications to run your workflow.


## Running a test workflow

To test that Janis is configured properly, We'll run a simple workflow called [`Hello`](https://janis.readthedocs.io/en/latest/tools/unix/hello.html) [click the link to see the dcoumentation]. This workflow prints `"Hello, World"` by default to stdout, and this stdout is captured as an output. This will test that Janis can submit to the cluster correctly. 

The Peter Mac configuration can submit to the janis partition on the cluster when the `--background` (`-B`) parameter is provided.

> You should ALWAYS use the `-B` argument at Peter Mac. 

We must specify an output directory (`-o`) to contain the execution and outputs, we'll ask Janis to create a subdirectory called `part1` within our `workshop1` directory.

Summary:

- Run in background with `-B`
- Specify an output directory with `-o part1`

```bash
janis run -B -o part1 hello
```

This command will:

- Create an output directory called `part1` (relative to the current directory),
- Start Cromwell,
- Submit to the cluster and run a task that calls "echo",
- Collect the results.


You'll see logs from Cromwell in the terminal. There's a number of statements that are worth highlighting:

```
[INFO]: Starting Janis in the background with: <sbatch command>
[INFO]: Submitted batch job 4830620
[INFO]: Exiting
```

We can track the progress of our workflow with:

```
janis watch part1/
```

You will see a progress screen like the following 

```
WID:        d12763
EngId:      291b6f91-6246-4ded-934b-98773e265ead
Name:       hello
Engine:     cromwell (localhost:53489) [PID=43580]

Task Dir:   $HOME/janis-workshop1/part1
Exec Dir:   $HOME/janis-workshop1/part1/janis/execution/hello/291b6f91-6246-4ded-934b-98773e265ead

Status:     Completed
Duration:   44s
Start:      2020-01-31T02:49:35.968005+00:00
Finish:     2020-01-31T02:50:20.305000+00:00
Updated:    Just now (2020-01-31T02:50:28+00:00)

Jobs: 
    [✓] hello (11s)       

Outputs:
    - out: $HOME/part1/out
```


In our output folder, there are two items (`ls part1`):
```
drwxr-sr-x 8 mfranklin punim0755 133K Jan 31 12:59 janis
-rw-r--r-- 1 mfranklin punim0755   14 Jan 31 12:58 out
```

The output to the task is called `out`, as this is the name of the output that the `hello` tool specifies.

```bash
cat part1/out
# Hello, mfranklin
```

The `janis` folder contains information about the execution, including logs, we'll see more about that in the next section.


## Aborting a workflow

As Janis manages other software to run your workflow, it's important to not directly kill the Janis instance, but rather ask to safely abort.

```
janis abort part1/
```

If this isn't completed:

- Internal databases may be corrupted,
- Instances of Cromwell may be let running in the background,
- Jobs submitted for execution may still run, including on cloud infrastructure.
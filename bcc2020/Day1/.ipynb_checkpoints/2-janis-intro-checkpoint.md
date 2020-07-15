# BCC2020 EAST - Janis Workshop (1.2)

## Introduction to Janis

Janis is workflow framework that uses Python to construct a declarative workflow. It has a simple workflow API within Python that you use to build your workflow. Janis converts your pipeline to the Common Workflow Language (CWL) or Workflow Description Language (WDL) for execution, which can then be published, shared or archived. 

This workshop uses a bioinformatics focus example, but Janis is a generic workflow assistant and can be used outside of the computational genomics.

- Janis GitHub: https://github.com/PMCC-BioinformaticsCore/janis
- Janis Documentation: https://janis.readthedocs.io/en/latest

## Foundations

- A workflow is a collection of tools are run in an organised manner.

- A workflow specification is a format that exactly describes the relationship between your tools. Popular workflow specification types include:

    - Common Workflow Language (CWL)
    - Workflow Description Language (WDL)
    - [_Unsupported_] Nextflow
    - [_Unsupported_] Snakemake

- YAML (.yml) is a file-format for specifying key-value pairs (like a dictionary). YAML is very similar to, and is in fact a superset of JSON.

### What is Janis

Janis is a project that aims to address two questions:

- How do we build pipelines that can run everywhere?
- How can we make running pipelines easier?

In fact, Janis is actually split into two components that addresses these questions separately:

- `janis-core` - Helps users **build** portable pipelines using existing workflow **specifications**.
- `janis-assistant` - Helps users **run** pipelines using existing workflow **engines**.

### Installations

#### Installing Janis through PIP
```bash
    pip install janis-pipelines
```


#### Installing Janis into a virtual env

A virtual environment is the best way to install Janis. It contains all the dependencies separately, and avoid polluting your local Python installation. It also preserves the version of Janis in a reproducible way.

1. Create an activate a virtualenv:

    ```bash
    # create virtual env
    virtualenv -p python3 janis/env

    # source the virtual env
    source janis/env/bin/activate
    ```


2. Install Janis through PIP:

    ```bash
    pip install janis-pipelines
    ```

#### Test that Janis (and associated modules) were installed

```bash
    janis -v
    # --------------------  ------
    # janis-core            v0.9.4
    # janis-assistant       v0.9.7
    # janis-pipelines       v0.9.1
    # janis-unix            v0.9.0
    # janis-bioinformatics  v0.9.3
    # janis-templates       v0.9.2
    # --------------------  ------
```

### Fundamental features

- Janis uses an _abstracted execution environment_ which removes the shared file system you may be used to in other pipelineing systems.

    - For a file or directory to be available to your tool, you need to EXPLICITLY include it. 
        - This includes associated files, if you want an indexed bam, you must use the BamBai type.

    - Outputs of a _tool_ must be EXPLICITLY collected to be used by future steps, else they will be removed.

    - Outputs of a workflow must be EXPLICITLY collected.

    - A step's requirements (its inputs) can be an input to a workflow, or the output of a previous step (hence creating a dependency).

        ![Diagram of alignment workflow showing connections](graphics/align-light.png)

- In Janis, all tasks are executed inside a isolated virtual environment called a [_Container_](https://www.docker.com/resources/what-container). Docker and Singularity are two common container types. (Docker containers can be executed by Singularity.)

### Setting up Janis 

Once installation is complete, we will start by initialising Janis environment. This step is only required on the first time we setup Janis. 

```bash
    janis init local 
```

Running this command will create a file in `~/.janis/janis.conf` that should look like as follow:

```yaml
engine: cromwell
notifications:
    email: null
template:
    id: pmac
    container_dir: /config/binaries/singularity/containers_devel/janis/
    catch_slurm_errors: true
    send_job_emails: false
    max_cores: 1 #40
    max_ram: 256
    max_workflow_time: 20100
    queues: debug #prod_måed,prod
    singularity_version: 3.4.0
```

We will leave this config file as default for the purpose of this workshop. This config file will be useful for advanced configuration, especially when used in High Performance Computing (HPC) environment. 

### How does Janis run a workflow?

Janis leverages community driven engines to run workflows. For this workshop, we will use the [cwltool](https://github.com/common-workflow-language/cwltool) execution engine to run translated Janis workflow (in Common Workflow Language [CWL](https://www.commonwl.org/)) using Dockerised tools. 

For our tests, Janis will:

- Convert the workflow to CWL
- Run the CWL workflow with cwltool
- Watch the progress of the workflow
- Perform a number of tasks after the workflow is completed

It's important to note that building workflows in Janis does NOT limit you to running with Janis. You are free to take the exported CWL and WDL specifications to run your workflow.


### Running a simple test workflow 

To test that Janis is configured properly, we will run a simple workflow called [`Hello`](https://janis.readthedocs.io/en/latest/tools/unix/hello.html) [click the link to see the documentation]. This workflow prints `"Hello, World"` by default to stdout, and this stdout is captured as an output. This will test that Janis can run in your environment correctly. 

We must specify an output directory (`-o`) to contain the execution and outputs, we'll ask Janis to create a subdirectory called `part1`. 

```bash
janis run -o part1 hello
```

This command will:

- Create an output directory called `part1` (relative to the current directory)
- Convert `hello` Janis workflow to `hello` CWL workflow
- Submit workflow to the cwltool and run a task that calls "echo"
- Collect the results

You will see logs from cwltool in the terminal. There is a number of statements that are worth highlighting:

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

## Tools Registry 

Janis contains a registry of prebuilt tools and workflows. This information is available in the documentation:

- Tools: https://janis.readthedocs.io/en/latest/tools/index.html
- Pipelines: https://janis.readthedocs.io/en/latest/pipelines/index.html

In fact, we have been using prebuilt tools to run our analysis, and these exist on the Registry.

These tools exist in separate modules to Janis, which means they can be updated independent of other janis functionality. It also means that you could create your own registry of tools independent of what Janis provides.

Let's look at the whole-genome variant calling pipeline that uses GATK to call variants: [`WGSGermlineGATK`](https://janis.readthedocs.io/en/latest/pipelines/wgsgermlinegatk.html).

We see the following table from the documentation:

|   |   |
|-- |-- |
|ID         | `WGSGermlineGATK` |
|Python:	| `janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK` |
|Versions:	| 1.2.0 |
|Authors:	| Michael Franklin |
|Citations: | 	 |
|Created:	| None |
|Updated:	| 2019-10-16 |
|Required inputs: | fastqs: Array<FastqGzPair> <br />reference: FastaWithDict <br />\<other inputs>: \<Type>|




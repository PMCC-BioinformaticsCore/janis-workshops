# Workshop 1.5 - Debugging a run

Workflows don't always run smoothly, and for that it's useful to understand how workflows run, and how Janis can help you solve the problems. 

The Janis documentation contains some answers for:

- [Frequently asked questions](https://janis.readthedocs.io/en/latest/references/faq.html)
- [Common errors](https://janis.readthedocs.io/en/latest/references/errors.html)


## Introduction

In this section, we're going to investigate inside the `janis` folder, and look at how Cromwell structures the execution to give us a better idea how workflows are run.

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

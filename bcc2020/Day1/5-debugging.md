# BCC2020 EAST - Janis Workshop (1.5)
# Debugging a run

Workflows do not always run smoothly, and for that it is useful to understand how workflows run, and how Janis can help you solve runtime problems. 

The Janis documentation contains some answers for:

- [Frequently asked questions](https://janis.readthedocs.io/en/latest/references/faq.html)
- [Common errors](https://janis.readthedocs.io/en/latest/references/errors.html)

In this section, we are going to investigate inside the `janis` folder, as this will be important for debugging!

### Tl;dr logs

Logs are stored in `<output-dir>/janis/logs`. In particular, it's worth checking out the `engine.log`:

```
less part2/janis/logs/engine.log
```


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

### Execution folder notes

Usually when a workflow is a success, Janis automatically removes the intermediate input files. In the previous section, we ran our preprocessing  workflow with `--development`, which means these files will persist even when the workflow succeededs.

By default, the execution directory is under `$outputdir/janis/execution/`. CWLTool and Cromwell have their own format for how this directory is structured.


## What happens when something goes wrong?

Workflows can fail for a variety of reasons, such as:

- A task may fail because:
    - Inputs are invalid (missing, incorrect format, invalid per spec)
    - Resources error (network, filesystem problems, unable to access resources)
    - Host problems (memory problems, cpu issues, time limits)
    - Doesn't write the outputs correctly
- and a myriad more problems.

Janis + CWLTool / Cromwell do their best to catch these problems and report them back to a user. Here's an example of a failed workflow, and how Janis may present it.

```
SID:        d92536
EngId:      d92536
Engine:     cwltool

Task Dir:   /Users/franklinmichael/source/janis-workshops/bcc2020/resources/part2

Status:     failed
Duration:   7s
Start:      2020-07-16T07:24:04.499003+00:00
Finish:     2020-07-16T07:24:11.463972+00:00
Updated:    3s ago (2020-07-16T07:24:11+00:00)

Jobs: 
        [✓] bwamem (0s)
        [!] samtoolsview (8s)
            stderr: /Users/franklinmichael/source/janis-workshops/bcc2020/resources/part2/janis/logs/engine.log       


Error: 
ERROR [job samtoolsview] Job error:
("Error collecting output for parameter 'out':\n../workflow/tools/SamToolsView_1_9_0.cwl:286:5: Did not find output file with glob pattern: '['generated.bam']'", {})
ERROR [step samtoolsview] Output is missing expected field file:///Users/franklinmichael/source/janis-workshops/bcc2020/resources/part2/janis/workflow/preprocessingWorkflow.cwl#preprocessingWorkflow/samtoolsview/out
```

This indicates to us that `bwamem` failed, and it tries to prompt us with the locations of `stderr`. Have a look through the engine log for more information.




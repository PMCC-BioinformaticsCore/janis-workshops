# Workshop 1.5 - Debugging a run

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
# Workshop 1.2 - Loading and configuring Janis

## Installing Janis into a virtual env

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

3. Test that Janis was installed:

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


## Configuring Janis

Janis can be configured to submit jobs to HPCs, this is done with a configuration file. By default, your configuration is placed at `~/.janis/janis.conf` (this file is created with a Janis init). Janis has a number of preconfigured environments, you can see these by running:

```
$ janis init -h

usage: janis init [-h] [-r RECIPES [RECIPES ...]] [--stdout] [-f] [-o OUTPUT]
                  {pmac,spartan,local,singularity,wehi,pawsey,slurm_singularity,pbs_singularity}
                  ...
```

If we're a local user, we don't need to configure Janis, it will automatically use Docker.


### [Spartan user only]

> This step only needs to occur on the first time you load Janis.

We need to configure Janis to be aware of the Slurm Cluster. Janis has an inbuilt [template for Spartan](https://janis.readthedocs.io/en/latest/templates/spartan.html) called `spartan` which takes care of the heavy lifting.

We need to provide a value for `container_dir`, a place where you can place Singularity containers. 

Running this command will create a config for Spartan at `~/.janis/janis.conf`

```
janis init spartan --container_dir /path/to/containerdir
```

You can see and edit some of these details with `vim ~/.janis/janis.conf`:

- Update the `notifications.email` field so Janis can send you notifications about the status of a workflow
- Janis can send you slurm notifications by settings `template.send_job_emails` to `true`
- Add a `template.max_cores` to 1

> Remember to reset `max_cores` and `queues` to their original setting at the end of this workshop.

```yaml
engine: cromwell
notifications:
  email: "youremail@unimelb.edu.au"
template:
  id: spartan
  max_cores: 1
    
  catch_slurm_errors: true
  container_dir: /path/to/containerdir
  max_workflow_time: 20100
  queues: cloud
  send_job_emails: true
  submission_queue: cloud
```

This configuration tells Janis (and Cromwell) how to interact with Slurm and Singularity.
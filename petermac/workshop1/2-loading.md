# Workshop 1.2 - Loading and configuring Janis

## Load Janis through the module system:

```
module load janis/dev
```

> Alternatively, Janis can be installed in a virtual env, instructions are [available in the documentation](https://janis.readthedocs.io/en/latest/tutorials/tutorial0.html).

## Configuring Janis

Janis can be configured to submit jobs to HPCs, this is done with a configuration file. By default, your configuration is placed at `~/.janis/janis.conf` (this file is created with a Janis init). Janis has a number of preconfigured environments, you can see these by running:

```
$ janis init -h

usage: janis init [-h] [-r RECIPES [RECIPES ...]] [--stdout] [-f] [-o OUTPUT]
                  {pmac,spartan,local,singularity,wehi,pawsey,slurm_singularity,pbs_singularity}
                  ...
```

We need to configure Janis to be aware of the Peter Mac Cluster. Janis has an inbuilt [template for Peter Mac](https://janis.readthedocs.io/en/latest/templates/pmac.html) called `pmac` which takes care of the heavy lifting.  In the next step we'll initialise a template for `pmac`. 


### [First time only]

> This step only needs to occur on the first time you load Janis.

[First run only] 

Running this command will create a config for Peter Mac at `~/.janis/janis.conf`

```
janis init pmac
```

 You can see and edit some of these details with `vim ~/.janis/janis.conf`:

- Update the `notifications.email` field so Janis can send you notifications about the status of a workflow
- Janis can send you slurm notifications by settings `template.send_job_emails` to `true`

```yaml
engine: cromwell
notifications:
email: null
template:
catch_slurm_errors: true
container_dir: /config/binaries/singularity/containers_devel/janis/
id: pmac
max_cores: 40
max_ram: 256
max_workflow_time: 20100
queues: prod_med,prod
send_job_emails: false
singularity_version: 3.4.0
```

This configuration tells Janis (and Cromwell) how to interact with Slurm and Singularity.
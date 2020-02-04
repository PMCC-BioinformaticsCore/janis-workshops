# Workshop 1.2 - Loading and configuring Janis

1. Load Janis through the module system

```
module load janis/0.9.0
```

> Alternatively, Janis can be installed in a virtual env, instructions are [available in the documentation](https://janis.readthedocs.io/en/latest/tutorials/tutorial0.html).

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
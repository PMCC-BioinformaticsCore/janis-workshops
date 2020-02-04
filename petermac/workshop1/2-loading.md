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
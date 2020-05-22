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

As we're a local user, we don't need to configure Janis, defaulting to use Docker.


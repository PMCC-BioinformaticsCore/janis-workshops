# Janis at Peter Mac - Workshop 2

Janis is workflow framework that uses Python to construct a declarative workflow. This workshop is the second part

## Learning outcomes

In this workshop, we'll learn:

- How to build an alignment workflow,
- Building a command tool (wrapper),
    - And how to integrate this tool into our workflow,
- Organise and rename our outputs
- Scattering (loops)
- How to add tools to the registry


## Foundations

It's recommended that you've participated in Workshop 1 as it gives you the foundations for:

- What is Janis,
- How to run workflows with Janis,
- How to do basic debugging of a pipeline.

This workshops uses biological and bioinformatics examples to describe workflows. Although the steps are explained, knowledge of this process will be useful.

### Bioinformatics in Janis

Janis provides a registry of tools and data types for bioinformatics analysis, called `janis-bioinformatics`. These tools are installed on the cluster, and are available to import, or use directly on the command line. You can see a list of bioinformatics tools that Janis provides [on the documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/index.html).


## Loading Janis

Janis is available through the module system with:

```
module load janis/dev
```

> Alternatively, Janis can be installed in a virtual env, instructions are [available in the documentation](https://janis.readthedocs.io/en/latest/tutorials/tutorial0.html).


In addition, within our config, we'll set:

- `max_cores` to `1`,
- `queues` to `"debug"`.

eg:

```bash
vim ~/.janis/janis.conf
```

```yaml
# ...other configuration options
template:
  id: pmac
  queues: debug # prod_med,prod
  max_cores: 1
```

## Getting started

Create a folder called `janis-workshop2` in a location where you have plenty of storage (we'd recommend your researcher folder).

```bash
mkdir janis-workshop2 && cd janis-workshop2
cp -r /data/janis/workshops/2020/workshop2/* .
```


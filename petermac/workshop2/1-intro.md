# Janis at Peter Mac - Workshop 2

Janis is workflow framework that uses Python to construct a declarative workflow. This workshop is the second part

## Learning outcomes

In this workshop, we'll learn:

- How to build an alignment workflow,
- Building a command tool (wrapper),
- Scattering (loops)
- Output naming


## Foundations

It's recommended that you've participated in Workshop 1 as it gives you the foundations for:

- What is Janis,
- How to run workflows with Janis,
- How to do basic debugging of a pipeline.

This workshops uses biological and bioinformatics examples to describe workflows. Although the steps are explained, knowledge of this process will be useful.


## Getting started

> Data is available at `<path to data>` for this workshop.


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

```yaml
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


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

> Instructions are available for installing Janis: https://janis.readthedocs.io/en/latest/tutorials/tutorial0.html


## Getting started

Let's start in a directory where we have plenty of space, then we'll download a tar file to `janis-workshop2`.

```
mkdir janis-workshop2 && cd janis-workshop2
wget -q -O- "https://github.com/PMCC-BioinformaticsCore/janis-workshops/raw/master/janis-data.tar" | tar -xz
```


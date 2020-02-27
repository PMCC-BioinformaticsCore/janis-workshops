# Workshop 1 - Conclusion

## Resetting your config

At the start of the workshop, we set the `max_cpu` of 1. Let's reset that with:

```bash
vim ~/.janis/janis.conf
```

## Summary

Thanks for taking part of the Introduction to Janis workshop!

To summarise, in this workflow you've learnt:

- What is Janis, 
    - How Janis is different from seqliner
- How to load a Janis environment,
- How to run a simple workflow,
- How to align some samples.
- How to debug if something goes wrong (check logs)
- How to override amount of resources
- How to batch run same pipeline on cohort of samples.


## Advanced functionality

Here's some additional functionality that Janis supports:

#### Scattering by multiple fields (dot + cross product)

> This is a component in Workshop 2.

Workflow's support looping through specific inputs through the `scatter` syntax.

#### Naming output files.

> This is a component in Workshop 2.

Usually, outputs are named by the tag of the output. However, it may be useful to organise your outputs in specific ways, especially when Janis might need to interact with other specific systems. On a workflow output, you can set an `output_name` and `output_folder` to determine these outputs.

#### Python Tool for arbitrary code execution

To avoid building a container for simple scripts, Janis provides a [PythonTool](https://janis.readthedocs.io/en/latest/references/tools/pythontool.html). This allows you to write a self-contained method that will get executed in a container.

We'd recommend this for short processing scripts, eg:

```python
from janis_core import PythonTool, TOutput, File
from typing import Dict, Optional, List, Any

class MyPythonTool(PythonTool):
    @staticmethod
    def code_block(in_string: str, in_integer: int) -> Dict[str, Any]:
        
        if len(in_string) > 10:
        suffix = "long string" 

            suffix = "short string"
        output_string = "The input was a " + suffix
        return {
            "myout": output_string,
            "myinteger": in_integer + 1
        }

    def outputs(self) -> List[TOutput]:
        return [
            TOutput("myout", str),
            TOutput("myinteger", int)
        ]

    def id(self) -> str:
        return "MyPythonTool"

    def version(self):
        return "v0.1.0"
```

#### Cloud execution of workflows

As every tool in Janis runs inside a container, moving to the cloud should be effortless. The Janis-assistant doesn't allow you to easily configure for Cromwell for the cloud (let's have a conversation though!), you can take your workflow and run it on pre-configured Cromwell instance (or another engine).

No changes to your workflow should have to be made, just update your input files to the paths of your data from your cloud storage, for example:

```yaml
sample_name: NA12878
fastq: 
- gs://my-bucket/path/to/BRCA1-R1.fastq.gz
- gs://my-bucket/path/to/BRCA1-R2.fastq.gz
reference: gs://my-bucket/reference.fasta
```


#### Cursory support for conditionals workflow

> This feature is still in testing, and is not currently widely available.

If you have steps that should only run in certain cirumstances, you're looking for _conditional_ support.

Janis has VERY cursory support for conditional workflows: https://github.com/PMCC-BioinformaticsCore/janis-core/pull/5


```python
w = WorkflowBuilder("conditionalTest")

w.input("inp", int, value=1)
w.input("name", str, value="Michael")

# I only want to run "echo" if the input called 'inp' has value greater than 1
w.step("echo", Echo(inp=w.name), when=w.inp > 1)

w.output("out", source=w.echo.out)
```
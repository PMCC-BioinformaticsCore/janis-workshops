# Workshop 2.4 - Scattering and loops

Loops are a foundational part of programming, and workflow specifications allow you to distribute an input over a task multiple times. This is called "scattering" in workflow specifications.

## Scattering by a single field

We might want to analyse a task across a single a number of genomic intervals. In this example, we'll just aim to print out each element in a list of strings. 

We're going to roughly replicate the following Python code:

```python
list_of_strings = []
for value in list_of_strings:
    print(value)
```

In our workflow, we'll use an inputs called `list_of_strings` that has an input type of `Array(String)`). We'll use the Janis tool [`Echo`](https://janis.readthedocs.io/en/latest/tools/unix/echo.html) which takes an input called `inp`. 

The key to this process, is within the [`workflow.step` method](https://janis.readthedocs.io/en/latest/references/workflow.html#creating-a-step), there an argument called `scatter` which we pass the input of the tool we want to scatter across; in this case it's `inp`.


**singlescatter.py**
```
from janis import WorkflowBuilder, String, Array
from janis_unix.tools.echo import Echo

w = WorkflowBuilder("print_list_of_strings")
w.input("list_of_strings", Array(String))

w.step(
    "print",
    Echo(
        inp=w.list_of_strings
    ),
    scatter="inp"
)

w.output("out", source=w.print)
```

We can see what this might look like in WDL with the following:

```bash
janis translate singlescatter.py wdl
```

```wdl
version development

import "tools/echo.wdl" as E

workflow print_list_of_strings {
  input {
    Array[String] list_of_strings
  }
  scatter (l in list_of_strings) {
     call E.echo as print {
      input:
        inp=l
    }
  }
  output {
    Array[File] out = print.out
  }
}
```


## Scattering by multiple fields

There are two different methods when scattering by multiple fields:

- Dot product (default)
- Cross product

### Dot product

The dot product groups all the first elements, then second, then third etc of the corresponding lists. For example, for 3 lists `[1A, 1B, 1C]`, `[2A, 2B, 2C]`, `[2A, 3B, 3C]`, the dot product would produce the following combinations: `[1A, 2A, 3A]`, `[1B, 2B, 3B]`, `[1C, 2C, 3C]`.

The lengths of the lists must be all equal.

> This is equivalent to the `zip` functionality in Python.

This is the default behaviour when you specify an array of fields to scatter across:

```python
from janis import WorkflowBuilder, String, Array
from janis_bioinformatics.tools.common.bwaaligner import BwaAligner
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict


w = WorkflowBuilder("multiple_align")
w.input("sample_names", Array(String))
w.input("fastqs", Array(FastqGzPair))
w.input("reference", FastaWithDict)

w.step(
    "align",
    BwaAligner(
        sample_name=w.sample_names,
        reference=w.reference,
        fastq=w.fastqs,
    ),
    scatter=["sample_name", "fastq"]
)

# Array of IndexedBams
w.output("out", source=w.align.out)
```

### Cross product

The cross product is similar to the cartestian product of two arrays (from maths). For 3 lists `[1A, 1B, 1C]`, `[2A, 2B, 2C]`, the cross product would produce the following combinations: `[1A, 2A]`, `[1A, 2B]`, `[1A, 2C]`, `[1B, 2A]`, `[1B, 2B]`, `[1B, 2C]`, `[1C, 2A]`, `[1C, 2B]`, `[1C, 2C]`.

As this isn't the default behaviour, you'll have to perform two additional imports `ScatterDescription` and `ScatterMethods`.

```python
from janis_core import WorkflowBuilder, String, Array, ScatterDescription, ScatterMethods


w = WorkflowBuilder("multiple_align")
w.input("field1", Array(String))
w.input("field2", Array(String))

w.step(
    "cross_test",
    MyTool(
        input1=w.field1,
        input2=w.field2
    ),
    scatter=ScatterDescription(
        ["sample_name", "fastq"],
        ScatterMethods.cross
    )
)

# Array of IndexedBams
w.output("out", source=w.align.out)
```
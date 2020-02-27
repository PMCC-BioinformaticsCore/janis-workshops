# Workshop 2.4 - Scattering and loops

Loops are a foundational part of programming, and workflow specifications allow you to distribute an input over a task multiple times. This is called "scattering" in workflow specifications.

```bash
mkdir scatter
```

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


```bash
vim scatter/single.py
```

```python
from janis_core import WorkflowBuilder, String, Array
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
janis translate scatter/single.py wdl
janis run -o scatter-single scatter/single.py \
    --list_of_strings String1 String2 String3
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

We haven't given Janis any good way to name these, so we'll end up with the following outputs:

```bash
$ ll scatter-single/
    drwxr-xr-x  franklinmichael  256B janis
    -rw-r--r--  franklinmichael    8B out_shard-0
    -rw-r--r--  franklinmichael    8B out_shard-1
    -rw-r--r--  franklinmichael    8B out_shard-2

$ cat scatter-single/out_shard-*
    String1
    String2
    String3
```

## Scattering by multiple fields

There are two different methods when scattering by multiple fields:

- Dot product (default)
- Cross product

### Dot product

The dot product groups all the first elements, then second, then third etc of the corresponding lists. For example, for 3 lists 
- `[1A, 1B, 1C]`, 
- `[2A, 2B, 2C]`, 
- `[3A, 3B, 3C]`, 

the dot product would produce the following combinations: 
- `[1A, 2A, 3A]`, 
- `[1B, 2B, 3B]`, 
- `[1C, 2C, 3C]`.

In the dot product, all of the lists must be the same length. 
s
> This is equivalent to the `zip` functionality in Python.

This is the default behaviour when you specify an array of fields to scatter across:

```bash
vim scatter/dot.py
```

> We'll include an `output_name` to show how this field may be useful.

```python
from janis_core import WorkflowBuilder, String, Array
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
        fastq=w.fastqs,
        reference=w.reference,
    ),
    scatter=["sample_name", "fastq"]
)

# Array of IndexedBams
w.output("out", source=w.align.out, output_name=w.sample_names)
```

```bash
janis translate scatter/dot.py wdl
janis run -o scatter-dot scatter/dot.py \
    --sample_names Sample1 \
    --fastqs data/BRCA1_R*.fastq.gz \
    --sample_names Sample2 \
    --fastqs data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta
```

### Cross product

The cross product is similar to the cartestian product of two arrays (from maths). For 2 lists 

1. `[1A, 1B, 1C]`, 
2. `[2A, 2B, 2C]`,

The cross product would produce the following combinations: : 
- `[1A, 2A]`, `[1A, 2B]`, `[1A, 2C]`, `[1B, 2A]`, `[1B, 2B]`, `[1B, 2C]`, `[1C, 2A]`, `[1C, 2B]`, `[1C, 2C]`.

As this isn't the default behaviour, you'll have to perform two additional imports `ScatterDescription` and `ScatterMethods`.

```
vim scatter/cross.py
```

```python
from janis_core import WorkflowBuilder, String, Array, ScatterDescription, ScatterMethods, CommandToolBuilder, ToolInput, ToolOutput, Stdout

# An example tool
PrintTwoInputsTool = CommandToolBuilder(
    "PrintTwoInputsTool",
    base_command=["echo"],
    inputs=[
        ToolInput("input1", String, position=1),
        ToolInput("input2", String, position=2)
    ],
    outputs=[
        ToolOutput("out", Stdout)
    ],
    container="ubuntu:latest",
    version="v0.1.0"
)

w = WorkflowBuilder("multiple_align")
w.input("field1", Array(String))
w.input("field2", Array(String))

w.step(
    "cross_test",
    PrintTwoInputsTool(
        input1=w.field1,
        input2=w.field2
    ),
    scatter=ScatterDescription(
        ["input1", "input2"],
        ScatterMethods.cross
    )
)

# Array of IndexedBams
w.output("out", source=w.cross_test.out)
```


```bash
janis translate scatter/cross.py wdl
janis run -o scatter-cross scatter/cross.py \
    --field1 1A 1B 1C \
    --field2 2A 2B 2C
```
Outputs:

```bash
$ ll scatter-cross/
    drwxr-xr-x  franklinmichael  256B janis
    -rw-r--r--  franklinmichael    6B out_shard-0
    -rw-r--r--  franklinmichael    6B out_shard-1
    -rw-r--r--  franklinmichael    6B out_shard-2
    -rw-r--r--  franklinmichael    6B out_shard-3
    -rw-r--r--  franklinmichael    6B out_shard-4
    -rw-r--r--  franklinmichael    6B out_shard-5
    -rw-r--r--  franklinmichael    6B out_shard-6
    -rw-r--r--  franklinmichael    6B out_shard-7
    -rw-r--r--  franklinmichael    6B out_shard-8

$ cat scatter-cross/out_shard-*
    1A 2A
    1A 2B
    1A 2C
    1B 2A
    1B 2B
    1B 2C
    1C 2A
    1C 2B
    1C 2C
```
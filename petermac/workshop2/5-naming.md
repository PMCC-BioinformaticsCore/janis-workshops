# Workshop 2.5 - Naming output files

Sometimes it's useful to organise your outputs in specific ways, especially when Janis might need to interact with other specific systems. By default, outputs are named by the tag of the output. The extension is derived from the type of the output (the [Bam](https://janis.readthedocs.io/en/latest/datatypes/bam.html) filetype knows it uses a `.bam` extension).

For example, if you had an output called `out` which had type `BamBai`, your output files by default would have the name `out.bam` and `out.bam.bai`.

When exposing an output on a workflow, there are two arguments you can provide to override this behaviour:

- `output_name: Union[str, InputSelector, InputNode] = None`
- `output_folder: Union[str, Tuple[Node, str], List[Union[str, InputSelector, Tuple[Node, str]]]] = None`

## Output name

Simply put, `output_name` is the dervied filename of the output without the extension. By default, this is the `tag` of the output.

You can specify a new output name in 2 ways:

1. A static string: `output_name="new name for output"`
2. Selecting an input value (given "sample_name" is the name of an input):
    1. `output_name=workflow.sample_name`
    2. `output_name=InputSelector("sample_name")`

You should make the following considerations:

- The input you select should be a string, or

- If the output you're naming is an array, the input you select should either be:
    - singular
    - have the same number of elements in it.

    Janis will either fall back to the first element if it's a list, or default to the output tag. This may cause outputs to override each other.


## Output folder

Similar to the output name, the `output_folder` is folder, or group of nested folders into which your output will be written. By default, this field has no value and outputs are linked directly into the output directory.

If the output_folder field is an array, a nested folder is created for each element in ascending order (eg: `["parent", "child", "child_of_child"]`).

There are multiple ways to specify output directories:

1. A static string: `output_folder="my_outputs"`
2. Selecting an input value (given "sample_name" is the name of an input):
    1. `output_folder=workflow.sample_name`
    2. `output_folder=InputSelector("sample_name")`
3. An array of a combination of values:
    - `output_folder=["variants", "unmerged"]`
    - `output_folder=["variants", w.sample_name]`
    - `output_folder=[w.other_field, w.sample_name]`

## Example applied

In our alignment example (`alignment.py`), we output the bam file with:

```python
w.output("out", source=w.sortsam.out)
```

We want to name the output in the following way:

- Grouped into the folder: `bams`,
- Named: `sample_name` (Janis will automatically add the `.bam` extension).

```python
w.output(
    "out", 
    source=w.sortsam.out,
    output_name=w.sample_name,
    output_folder=["bams"]
)
```




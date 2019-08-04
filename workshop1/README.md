# Workshop 1 - Introduction to Janis

Welcome to the first workshop for Janis! 

> This guide is designed as an aid to a presented workshop.

Welcome to Janis! Janis is a Python framework to assist in building computational workflows that can be exported to [CWL](https://www.commonwl.org/) and [WDL](http://www.openwdl.org/).

## Requirements

You must have Python 3.6 or later installed.

## Installing Janis

Janis can be easily installed by running the following pip command:

```bash
pip3 install janis-pipelines[bioinformatics,runner]
```

This will install the core Janis API, the unix and bioinformatics tools and a workflow running assistant that makes running workflows a lot easier.

> If you're getting permission issues, you might need to include the `--user` flag. It's also a good idea to include the `--no-cache` flag

### Testing the installation

We can easily test the installation by jumping into a Python terminal:

```bash
# Inside Python terminal
>>> import janis as j
>>> j.__version__ 
'v0.4.0`
```
We can also confirm this through a regular terminal:
```bash
janis --version
#v0.4.0
```

> These versions might be slightly different, `janis.__version__` returns the version of `janis.core`, while `janis --version` returns the version of `janis.runner`, however both test that we have a correct installation of Janis.

## Simple example

Let's build the simple `echo` workflow from the README. This just connects a string input to the `Echo` tool and collects the output.

> DIAGRAM

> The next steps can be achieved in a Python terminal or a saved file (and running the result), we'll do it in a file for isolation.

#### Selecting our tools

We know we want to use the `Echo` tool. Janis' documentation contains automatically generated tool descriptions we can consult to learn more about the tool. 

By visiting `documentation > tools (sidebar) > unix > Echo`, we get the following page:

![Screenshot of [Echo](https://janis.readthedocs.io/en/latest/tools/unix/echo.html) documentation](/resources/echo-docs.png)

It also gives us the import location which we can use to import the file:

```python
import janis as j
from janis_unix.tools.echo import Echo
```

#### Assembling our workflow components

Let's build the workflow, an input of type `string` called `name`, a step called `echoStep` and an output called `out`.

> Our Python variable names can be different from the identifier. 

```python
# After our imports

myWorkflow = j.Workflow("echoWf")
inp = j.Workflow("name", data_type=j.String(), value="Michael")
stp = j.Step("echoStep", tool=Echo())
out = j.Output("out")	# Will automatically determine the output type
```

#### Making our connections

We'll use the [`Workflow.add_edge`](https://janis.readthedocs.io/en/latest/references/workflow.html#janis.Workflow.add_edge) method on our workflow to build our connections, first between our input (`inp`) and the input of our Echo step (`stp.inp`), and secondly between the output of our step (`stp.out`) and our output (`out`).

```python
myWorkflow.add_edge(inp, stp.inp)
myWorkflow.add_edge(stp.out, out)
```

#### Translating our output

We can use the [`Workflow.translate`](https://janis.readthedocs.io/en/latest/references/workflow.html#janis.Workflow.translate) method to convert our workflow to a [`"cwl"`](https://janis.readthedocs.io/en/latest/references/cwl.html) or [`"wdl"`](https://janis.readthedocs.io/en/latest/references/wdl.html) representation. By default this method will print the workflow, tools and input-job to the console. However it can be configured to write to disk (with the `to_disk` param).

```python
myWorkflow.translate("cwl", to_disk=False)  # or "wdl"
```


### Final result

Congratulations, you've built a workflow! You can run this file to see your `cwl` or `wdl` in the console.

```python
import janis as j  
from janis_unix.tools.echo import Echo  
    
myWorkflow = j.Workflow("echoWf")
inp = j.Input("name", data_type=j.String(), value="Michael")
stp = j.Step("echoStep", tool=Echo())
out = j.Output("out")	# Will automatically determine the output type
  
myWorkflow.add_edge(inp, stp.inp)
myWorkflow.add_edge(stp.out, out)
  
# Will print the CWL, input file and relevant tools to the console  
myWorkflow.translate("cwl", to_disk=False)  # or "wdl"
```

## Running our workflow with `janis-runner`

You've built a workflow and translated it to CWL or WDL which you can run on your preferred engine. Janis-runner is designed to streamline that process of running workflows.

> We installed `janis-runner` when we included the `runner` install extra in `pip3 install janis-pipelines[bioinformatics, runner]`. 

We'll run our workflow with CWLTool, the reference runner for CWL.

```bash
janis run simple.py --engine cwltool
```


## Summary

In this workshop, you've learnt to:

- Install Janis
- Understand how to import Janis into a Python file
- Learn and apply basic workflow concepts:
	- Inputs / steps / outputs
- Build simple workflow
- Translate a workflow to CWL and WDL
- Run translated workflow with `janis-runner`
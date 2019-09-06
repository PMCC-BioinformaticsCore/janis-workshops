# Workshop 1 - Introduction to Janis

Welcome to the first workshop for Janis! 

> This guide is designed as an aid to a presented workshop.

Welcome to Janis! Janis is a Python framework to assist in building computational workflows that can be exported to [CWL](https://www.commonwl.org/) and [WDL](http://www.openwdl.org/).

## Requirements

You must have Python 3.6 or later installed.

## Installing Janis

Janis can be easily installed by running the following pip command:

```bash
pip3 install janis-pipelines
```

This will install the core Janis API, the unix and bioinformatics tools and a workflow running assistant that makes running workflows simpler.

> If you're getting permission issues, you might need to include the `--user` flag. If you're getting an older version of Janis, include the `--no-cache` flag

### Installing a workflow engine

Janis requires the use of a workflow engine to run your pipelines and a container assistant. For this tutorial, we require you to have Docker installed, but each engine can be configured to use Singularity.

#### Installing CWLTool

> More instructions on GitHub: [common-workflow-language/cwltool#install](https://github.com/common-workflow-language/cwltool#install)

CWLTool must be installed and be available on your `$PATH`. The simplest method is through:

```bash
pip3 install cwltool
```

#### Installing Cromwell

Cromwell requires java to be installed. Janis will automatically download Cromwell to `~/.janis/cromwell-xx.jar`, so this option should work without extra effort.


## Simple example

Let's build the simple `echo` workflow from the README. This just connects a string input to the `Echo` tool and collects the output.

> DIAGRAM

### Selecting our tools

We know we want to use the `Echo` tool. Janis' documentation contains tool descriptions we can consult to learn more about the tool. 

By visiting [`documentation > tools (sidebar) > unix > Echo`](https://janis.readthedocs.io/en/latest/tools/unix/echo.html), we get the following page:

![Screenshot of Echo's documentation](/resources/echo-docs.png)

We need to `import` the Echo tool into our file. The documentation gives us the import statement we can use to import the appropriate tool wrapper.

```python
import janis as j
from janis_unix.tools.echo import Echo
```

#### Assembling our workflow components

Let's declare the workflow and expose an input of type `String` called `name` with a default of `"Douglas"`. Our input will be available as a property on the workflow, and accessible through dot-notation.

```python
# After our imports

w = j.Workflow("echoWf")
w.input("name", j.String, default="Douglas")
# accessible with `w.name`
```

#### Tools and Connections

When we create out step, we provide an `identifier`, a tool and our connections. Our parameter names for our `Workflow.step` function mirror the inputs that the tool requires.

We want to connect our input (accessible through `w.name`) to the `inp` connection on the tool Echo. We can do that with the following code.

```python
# After our input declaration
w.step("echo", Echo, inp=w.name)
```

#### Exposing the tool output

We can finish off our workflow by adding a output, this has an identifier and a `source`.

```python
w.output("out", source=w.echo)
```

#### Final workflow

If all has gone well, you should end up with the workflow:

```python
w = j.Workflow("echoWf")
w.input("name", j.String, default="Douglas")
w.step("echo", Echo, inp=w.name)
w.output("out", source=w.echo)
```

#### Translating our output

There are two ways we can see a "CWL" / "WDL", 

1. Include a  [`Workflow.translate`](https://janis.readthedocs.io/en/latest/references/workflow.html#janis.Workflow.translate) method to convert our workflow to a [`"cwl"`](https://janis.readthedocs.io/en/latest/references/cwl.html) or [`"wdl"`](https://janis.readthedocs.io/en/latest/references/wdl.html) representation. 

2. Run `janis translate myworkflow.py wdl` from the shell.


## Running our workflow with `janis-runner`

You've built a workflow and translated it to CWL or WDL which you can run on your preferred engine. Janis-runner is designed to streamline that process of running workflows.

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
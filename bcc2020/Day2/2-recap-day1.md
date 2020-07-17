# BCC2020 EAST - Janis Workshop (2.2)

## Recap of day 1

Janis is workflow framework that uses Python to construct a declarative workflow. It has a simple workflow API within Python that you use to build your workflow. Janis converts your pipeline to the Common Workflow Language (CWL) or Workflow Description Language (WDL) for execution, which can then be published, shared or archived. 

### Translating workflow

``` bash
    janis translate processing.py cwl
```

``` bash
    janis translate processing.py wdl
```

### Running workflow

```bash
    janis run processing.py <input>
```


### Output & logs

Output will be located in `<path>/partX/<out>`


### Adding new tools to workflow

We will start by importing the tool class. 

``` python
    from janis.bioinformatics.tools import GATK 
```

```python
    self.input()
```

```python
    self.step()
```

```python
    self.output()
```



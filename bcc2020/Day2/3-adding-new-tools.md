# BCC2020 EAST - Janis Workshop (2.3)

## Adding new tool (BQSR)

In this section, we are going to add more tools into our data processing workflows that we started yesterday. Assuming none of these tools are available on our existing tool-registry, we will show you how to wrap new tools into Janis. 

We will create the following new tools:

- GATK SetNmMdAndUqTags
- GATK BaseRecalibrator
- GATK GatherBQSRReports
- GATK ApplyBqsr

## Creating our file

Similar to previous section, we can start by creating a file called `processing.py`. In the interest of time, we will duplicate previous `processing.py` instead of starting from scratch. 

```bash
    mkdir part5 && mkdir tools
    cp tools/processing.py tools/processing2.py
```

## GATK SetNmMdAndUqTags

```python

Gatk4SetNmMdAndUqTags_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## GATK BaseRecalibrator

```python

Gatk4BaseRecalibrator_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## GATK GatherBQSRReports

```python

Gatk4GatherBQSRReports_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## GATK ApplyBqsr

```python

Gatk4ApplyBqsr_4_1_4 = ToolBuilder(
    basecommand=[]

)

```

## Chaining tools to workflow

```python
    self.step("")
    self.step("")
    self.step("")
    self.step("")

```

## Run with the test data from yesterday

```bash
    janis run processing2.py
```

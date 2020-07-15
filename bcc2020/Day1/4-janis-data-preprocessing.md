# BCC2020 EAST - Janis Workshop (1.4)

## Exercise: extend alignment workflow to complete the data processing workflow

In this section, we will give you some hands-on time to play  with Janis workflow. The task in this exercise is to extend alignment workflow from the previous section where we will add `Sort` step to the bam file post mark duplicates. 

This tool already exists within Janis Tool Registry, you can see its documentation here:

- [GATK4 SortSam] (https://janis.readthedocs.io/en/latest/tools/bioinformatics/gatk4/gatk4sortsam.html)


## Creating our file

Similar to previous section, we can start by creating a file called `processing.py`. In the interest of time, we will duplicate previous `alignment.py` instead of starting from scratch. 

```bash
    mkdir part4 && mkdir tools
    cp tools/alignment.py tools/processing.py
```

## Adding SortSam to workflow

The commandline equivalent command that we are trying to add into our workflow is 

```bash
    GATK SortSam .... 
```

Step
- Import tool from tool registry
- Add input a new input called 'compression_level' 
- Add step to the workflow, connecting the output of mark_duplicates step to the input of SortSam's input (bam)
- We will use sortOrder="coordinate"
- Gather output from SortSam as the final workflow output

Once you have completed the task, you can test by translating your workflow to cwl. 

```bash
    janis translate tools/processing.py cwl
```

If the translations looks ok, please go ahead and run this updated workflow using the same test data. 

```bash
    janis run ....
```

The solution to this task is also available at ...


## Advanced task

For those we are familiar with this GATK workflow, you might have noticed that there are other steps that we purposedly omit from this example. If you have finished with the exercise above, you can attempt to complete the remaining steps of this data processing workflow. Some of these steps will be used as a different task for our day-2 topics. 

- Gatk4SetNmMdAndUqTags_4_1_4
- Gatk4BaseRecalibrator_4_1_4
- Gatk4GatherBQSRReports_4_1_4
- Gatk4ApplyBqsr_4_1_4
- Gatk4GatherBamFiles_4_1_4
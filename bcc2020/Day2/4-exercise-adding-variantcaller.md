# BCC2020 EAST - Janis Workshop (2.4)

## Exercise: add a variant-caller (GATK Haplotypecaller) to complete the germline variant-caller for this workshop

In this section, we will give you some hands-on time to add new tool (not previously in the registry) to a workflow. The task in this exercise is to create a new python class for `GATK HaplotypeCaller` using Janis' `ToolBuilder`. After the variant-caller class has been created, this tool will be added to our previous data processing workflow. 


## Creating our file

Similar to previous section, we can start by creating a file called `germline.py`. In the interest of time, we will duplicate previous `processing.py` instead of starting from scratch. 

```bash
    mkdir part6 && mkdir tools
    cp tools/processing2.py tools/germline.py
```

## Creating GATK HaplotypeCaller tool class

The commandline equivalent command that we are trying to add into our workflow is 

```bash
    GATK -Xmx${memory}g HaplotypeCaller .... 
```

Step
- Create a new class called GATKHaplotypeCaller_Version
- Create ToolBuilder
- Add containers version
- Add required input
- Add required output
- Add additional optional input, output and arguements
- Add docs and metadata (Optional)
- Please note that datatype for the output is Vcf (link to janis-type)

Once you have completed the task, you can test this by translating your tool class to cwl. 

```bash
    janis translate tools/germline.py GATKHaplotypeCaller_Version cwl
```

If the translations looks ok, we will add this tool to our workflow

Step: 
- Open `germline.py`
- Add new input
- Add new step
- Add new output

Once you have completed the task, you can test this by translating your updated workflow to cwl. 

```bash
    janis translate tools/germline.py cwl
```

followed by running this with the provided test data. 

```bash
    janis run tools/germline.py
```

The solution to this task is also available at ...


## Advanced task

If you are familiar with how python object oriented works, this tool definition can be created as a separate class. This can then be used via python import similar to how we setup our janis-bioinformatics toolbox in our previous examples on Day 1. 

You can take a look at our GATK HaplotypeCaller implementation in our tool registry: 

[Link](link)

If you wish, you can attempt to modify your implementation this way. You will be able to use this definition as an independent workflow. For example, if you already have a bam file and wish to only run a variant-caller on your sample. 

Step:
- As above, but in a separate class

Run as workflow:
```bash
    janis run GATK_Haplotypecaller <input>
```

# Workshop 1.4 - Aligning a set of samples

Janis comes with a number of prebuilt pipelines. We're going to use the [BWAAligner](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html) (Cutadapt + BwaMem + Samtools + SortSam) to turn out a fastq pair into an indexed Bam.

By looking at the documentation for this tool: https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html

We see that the tool requires:

- `sample_name` - String
- `reference` - FastaWithDict
- `fastq` - FastqGzPair

and will return an indexed bam (`.bam` + `.bam.bai`) called `out`.

We're also going to add `--keep-intermediate-files` as it will be useful for the next section.

> The order of arugments is important here

Let's run the workflow!

```
janis run -B --keep-intermediate-files BwaAligner --sample_name NA12878 --fastq data/align/BRCA1_R*.fastq.gz
```

```
WID:        ed6702
EngId:      a07054bd-aa50-417e-a3e6-af3e62dd98cb
Name:       BwaAligner
Engine:     cromwell (localhost:49681) [PID=31868]

Task Dir:   $HOME/janis-workshop1/test2
Exec Dir:   $HOME/janis-workshop1/test2/janis/execution/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb

Status:     Completed
Duration:   3m:08s
Start:      2020-01-31T03:50:27.112017+00:00
Finish:     2020-01-31T03:53:35.184000+00:00
Updated:    10s ago (2020-01-31T03:53:40+00:00)

Jobs: 
    [✓] cutadapt (43s)
    [✓] bwamem (1m:14s)
    [✓] sortsam (31s)       

Outputs:
    - out: $HOME/janis-workshop1/test2/out.bam
```

At `test2/out.bam`, we have our aligned sample.
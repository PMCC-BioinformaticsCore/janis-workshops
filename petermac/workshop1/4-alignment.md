# Workshop 1.4 - Aligning a set of samples

Janis comes with a number of prebuilt pipelines. We're going to use the [BWAAligner](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html) (Cutadapt + BwaMem + Samtools + SortSam) to turn out a fastq pair into an indexed Bam.

By looking at the documentation for this tool: https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html we see that the tool requires:

- `sample_name` - String
- `reference` - FastaWithDict
- `fastq` - FastqGzPair

and will return an indexed bam (`.bam` + `.bam.bai`) called `out`.

Janis can also generate an input file for a workflow:

```bash
janis inputs BwaAligner # > align-inputs.yml
```

We're also going to add `--keep-intermediate-files` as it will be useful for the next section.

It's important to keep the following argument format when running your workflow. Providing parameters after the `$workflowname` will result in that parameter passed to the workflow as an input.

```
janis run <run options> worklowname <workflow inputs>
```


Let's run the workflow in the directory `part2`!

```
janis run \
    -B --keep-intermediate-files \
    -o part2 \
    BwaAligner \
    --sample_name NA12878 \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference /bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta
```

Once the workflow completes, you will receive something similar to the following progress screen from `janis watch $wid`:

```
WID:        ed6702
EngId:      a07054bd-aa50-417e-a3e6-af3e62dd98cb
Name:       BwaAligner
Engine:     cromwell (localhost:49681) [PID=31868]

Task Dir:   $HOME/janis-workshop1/part2
Exec Dir:   $HOME/janis-workshop1/part2/janis/execution/BwaAligner/a07054bd-aa50-417e-a3e6-af3e62dd98cb

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
    - out: $HOME/janis-workshop1/part2/out.bam
```

Our aligned BamPair is copied to `part2/out.bam` (you'll also see the index at `part2/out.bam.bai`)
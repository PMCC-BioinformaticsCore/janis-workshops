# Workshop 1.6 - Running multiple samples

When running multiple samples, Janis provides functionality to easily submit a `batch` workflow.

Within the `janis run -h` help guide, there's the following argument group:

```
batchrun arguments:
  --batchrun            Enable the batchrun Pipeline Modifier
  --batchrun-fields BATCHRUN_FIELDS [BATCHRUN_FIELDS ...]
  --batchrun-groupby BATCHRUN_GROUPBY
                        Which field should we use to group the samples by,
                        this field should be UNIQUE in the run.
```

Let's explain the arguments:

- `--batchrun` is a flag to tell Janis that we're going to do a `batch` run.
- `--batchrun-fields`: A list of fields unique to each batch run. This saves us from specifying reference files multiple times.
- `--batchrun-groupby`: The field name that we're going to group our runs by. This might be a `sample_name`. Note, this must be unique within your inputs.

## Example - Aligning samples

We're going to use the same tool [`BwaAligner`](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html) to align two samples. Instead of setting Janis up twice, we can use `batch` run the workflow across two samples.

Looking at [`BwaAligner`'s documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html), we have the following inputs:

- `fastq: FastqGzPair`
- `sample_name: String`
- `reference: FastaWithDict`

The input `reference` is going to be the same for each of the alignments, where `sample_name` and `fastq` will change, and we can use the `sample_name` as a key.

Let's see this in action and we can investigate the output:

```
janis run \
    -o part3 \
    --batchrun \
    --batchrun-groupby sample_name \
    --batchrun-fields sample_name fastq \
    BwaAligner \
    --reference /path/to/reference.fasta \
    --sample_name NA12878 \
    --sample_name NA12879 \
    --fastq BRCA1_R*.fastq.gz \
    --fastq BRCA2_R*.fastq.gz
```

Let's have a look at the watch screen:

```
WID:        ac24fd
EngId:      e5d08985-2111-445c-a41b-aa397c803afe
Name:       BwaAligner
Engine:     cromwell (localhost:49276) [PID=22920]

Task Dir:   $HOME/part3
Exec Dir:   $HOME/part3/janis/execution/BwaAligner/e5d08985-2111-445c-a41b-aa397c803afe

Status:     Completed
Duration:   2m:55s
Start:      2020-02-06T11:20:41.086595+00:00
Finish:     2020-02-06T11:23:35.871000+00:00
Updated:    3m:58s ago (2020-02-06T11:23:41+00:00)

Jobs: 
    [✓] Sample2_BwaAligner (2m:21s)
        [✓] cutadapt (6s)
        [✓] bwamem (1m:59s)
        [✓] sortsam (9s)
    [✓] NA12878_BwaAligner (1m:51s)
        [✓] cutadapt (6s)
        [✓] bwamem (1m:18s)
        [✓] sortsam (19s)       

Outputs:
    - NA12878_out: $HOME/part3/NA12878/NA12878_out.bam
    - Sample2_out: $HOME/part3/Sample2/Sample2_out.bam
```

A few points to note:

- The step name is scoped by our `sample_name` (as we asked by providing the `groupby` field)
- The outputs are separated into a folder called `sample_name`.
    - If you run a workflow that already groups it's outputs, they are placed in a subdirectory of the groupby field (in this case `sample_name`). 






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

> Specify the batchrun-fields BEFORE the groupby, as BASH may get confused and include your following parameters as a field to batch on. (eg: `[...] --batchrun-fields field1 field2 WorkflowName`).

## Example - Aligning samples

We're going to use the same tool [`BwaAligner`](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html) to align two samples. Instead of setting Janis up twice, we can use `batch` run the workflow across two samples.

Looking at [`BwaAligner`'s documentation](https://janis.readthedocs.io/en/latest/tools/bioinformatics/common/bwaaligner.html), we have the following inputs:

- `fastq: FastqGzPair`
- `sample_name: String`
- `reference: FastaWithDict`

The input `reference` is going to be the same for each of the alignments, where `sample_name` and `fastq` will change, and we can use the `sample_name` as a key.

Let's see this in action and we can investigate the output:

```bash
wid=$(janis run \
    --background \
    -o part3 \
    --batchrun \
    --batchrun-fields sample_name fastq \
    --batchrun-groupby sample_name \
    BwaAligner \
    --reference /bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta \
    --sample_name Sample1 \
    --fastq data/BRCA1_R*.fastq.gz \
    --sample_name Sample2 \
    --fastq data/BRCA1_R*.fastq.gz) # We'll use the same files to keep it simple
```

Let's have a look at the watch screen:

```
WID:        ac24fd
EngId:      e5d08985-2111-445c-a41b-aa397c803afe
Name:       BwaAligner
Engine:     cromwell (localhost:49276) [PID=22920]

Task Dir:   $HOME/janis-workshop1/part3
Exec Dir:   $HOME/janis-workshop1/part3/janis/execution/BwaAligner/e5d08985-2111-445c-a41b-aa397c803afe

Status:     Completed
Duration:   2m:55s
Start:      2020-02-06T11:20:41.086595+00:00
Finish:     2020-02-06T11:23:35.871000+00:00
Updated:    Just now (2020-02-06T11:23:35+00:00)

Jobs: 
    [✓] Sample1_BwaAligner (2m:21s)
        [✓] cutadapt (6s)
        [✓] bwamem (1m:59s)
        [✓] sortsam (9s)
    [✓] Sample2_BwaAligner (1m:51s)
        [✓] cutadapt (6s)
        [✓] bwamem (1m:18s)
        [✓] sortsam (19s)       

Outputs:
    - NA12878_out: $HOME/janis-workshop1/part3/Sample1/Sample1_out.bam
    - Sample2_out: $HOME/janis-workshop1/part3/Sample2/Sample2_out.bam
```

A few points to note:

- The step name is scoped by our `sample_name` (as we asked by providing the `groupby` field)
- The outputs are separated into a folder called `sample_name`.
    - If you run a workflow that already groups it's outputs, they are placed in a subdirectory of the groupby field (in this case `sample_name`). 

## Cascading input files

It's possible to prepare a number of files for individual samples, and then Janis will stack these together during a batch run. To represent the previous example:

> The paths in the YAML file need to be already fully qualified (`$HOME` is workshop placeholder).

**`inputs1.yml`**
```yaml
sample_name: Sample1
fastq:
- $HOME/data/BRCA1_R1.fastq.gz
- $HOME/data/BRCA1_R2.fastq.gz
reference: /bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta
```

**`inputs2.yml`**
```yaml
sample_name: Sample2
fastq:
- $HOME/data/BRCA1_R1.fastq.gz
- $HOME/data/BRCA1_R2.fastq.gz

# Janis will correctly realise it doesn't need to stack the reference file
# and will instead override the previously defined value
reference: /bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta
```

Run statement:

> - This time the inputs need to go BEFORE the workflow name
> - specifying the reference in the CLI will override the two values inside the input yamls

```bash
wid=$(janis run \
    --background \
    -o part3-inputfiles \
    --batchrun \
    --batchrun-fields sample_name fastq \
    --batchrun-groupby sample_name \
    --inputs inputs1.yml \
    --inputs inputs2.yml \
    BwaAligner \
    --reference /bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta)
```

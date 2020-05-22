# Workshop 2.4 - Integrating Samtools Flagstat

In the previous sections, we built a workflow to align a set of reads to an indexed bam, and added SamtoosFlagstat into Janis. In this section, we're going to add this tool to the end of our workflow.

## Imports

We're not going to go into great details about Python imports, but we've put both our `alignment.py` and `samtoolsflagstat.py` into the same directory.

Within the alignment workflow, we can add the following [relative import](https://realpython.com/absolute-vs-relative-python-imports/) to the top of **`alignment.py`**.

```python
from samtoolsflagstat import SamtoolsFlagstat
```

## Step definition

Now that we have our tool inside our `alignment.py`, we can use it similar to how we've used other tools. Althought the output of `sortsam` is an `IndexedBam`, where the input of `SamToolsFlagstat` is a regular Bam, we're able to connect these 

```python
w.step(
    "flagstat",
    SamToolsFlagstat(
        bam=w.sortsam.out
    )
)
```

## Output

We'll output the statistics file we get with the following call:

```python
w.output("stats", source=w.flagstat.stats)
```


## Final result

```python
from janis_core import WorkflowBuilder, String

from typing import List, Optional, Union

from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict, Bam
from janis_unix.data_types import TextFile

# import SamToolsFlagStat from relative path
from samtoolsflagstat import SamToolsFlagstat


w = WorkflowBuilder("alignmentWorkflow")

# Inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPair)
w.input("reference", FastaWithDict)

# Steps
w.step(
    "bwamem", 
    BwaMemLatest( 
        reads=w.fastq, 
        readGroupHeaderLine=w.read_group, 
        reference=w.reference
    )
)
w.step(
    "samtoolsview", 
    SamToolsView_1_9(
        sam=w.bwamem.out
    )
)

w.step(
    "sortsam",
    Gatk4SortSam_4_1_2(
        bam=w.samtoolsview.out,
        sortOrder="coordinate",
        createIndex=True,
        validationStringency="SILENT",
        maxRecordsInRam=5000000
    )
)

w.step(
    "flagstat",
    SamToolsFlagstat(
        bam=w.sortsam.out
    )
)

# Outputs
w.output("out", source=w.sortsam.out)
w.output("stats", source=w.flagstat.stats)
```

```bash
janis translate tools/alignment.py
janis run -o part3 tools/alignment.py \
    --fastq data/BRCA1_R*.fastq.gz \
    --reference reference/hg38-brca1.fasta \
    --sample_name NA12878 \
    --read_group "@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA"
```

See the results of this workflow with:

```
$ ls part3

drwxr-xr-x  franklinmichael  256B janis
-rw-r--r--  franklinmichael  2.7M out.bam
-rw-r--r--  franklinmichael  296B out.bam.bai
-rw-r--r--  franklinmichael  408B stats.txt
```


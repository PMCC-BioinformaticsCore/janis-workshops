from janis_core import WorkflowBuilder, String

from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict

from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4SortSam_4_1_2,
    Gatk4MarkDuplicates_4_1_4,
)

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
        reads=w.fastq, readGroupHeaderLine=w.read_group, reference=w.reference
    ),
)
w.step("samtoolsview", SamToolsView_1_9(sam=w.bwamem.out))

w.step(
    "sortsam",
    Gatk4SortSam_4_1_2(
        bam=w.samtoolsview.out, sortOrder="coordinate", createIndex=True
    ),
)

w.step("markduplicates", Gatk4MarkDuplicates_4_1_4(bam=w.sortsam.out))

# Outputs
w.output("out", source=w.markduplicates.out)

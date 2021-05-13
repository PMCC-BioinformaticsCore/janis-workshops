from janis_core import WorkflowBuilder, String, Array

# Import bioinformatics types
from janis_bioinformatics.data_types import (
    FastqGzPairedEnd,
    FastaWithIndexes,
    VcfTabix,
)

# Import bioinformatics tools
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)

# Add tools import here


# Construct the workflow here
w = WorkflowBuilder("preprocessingWorkflow")

# inputs
w.input("sample_name", String)
w.input("read_group", String)
w.input("fastq", FastqGzPairedEnd)
w.input("reference", FastaWithIndexes)
# add known_sites input here

# Use `bwa mem` to align our fastq paired ends to the reference genome
w.step(
    "bwamem",  # step identifier
    BwaMemLatest(
        reads=w.fastq,
        readGroupHeaderLine=w.read_group,
        reference=w.reference,
        markShorterSplits=True,  # required for MarkDuplicates
    ),
)

# Use `samtools view` to convert the aligned SAM to a BAM
#   - Use the output `out` of the bwamem step
w.step(
    "samtoolsview", SamToolsView_1_9(sam=w.bwamem.out),
)

# Use `gatk4 MarkDuplicates` on the output of samtoolsview
#   - The output of BWA is query-grouped, providing "queryname" is good enough
w.step(
    "markduplicates",
    Gatk4MarkDuplicates_4_1_4(bam=w.samtoolsview.out, assumeSortOrder="queryname"),
)
# Use `gatk4 SortSam` on the output of markduplicates
#   - Use the "coordinate" sortOrder
w.step("sortsam", Gatk4SortSam_4_1_4(bam=w.markduplicates.out, sortOrder="coordinate",))

# Use `gatk4 SetNmMdAndUqTags` to calculate standard tags for BAM
w.step(
    "fix_tags", Gatk4SetNmMdAndUqTags_4_1_4(bam=w.sortsam.out, reference=w.reference,),
)

# Add the Base Quality Score Recalibration steps here!

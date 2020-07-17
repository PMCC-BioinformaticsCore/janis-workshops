from janis_core import WorkflowBuilder, String

# Import bioinformatics types
from janis_bioinformatics.data_types import FastqGzPairedEnd, FastaWithIndexes

# Import bioinformatics tools
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.samtools import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
)

# Construct the workflow here

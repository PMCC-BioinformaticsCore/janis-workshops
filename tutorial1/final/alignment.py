import janis

from janis_bioinformatics.tools.bwa.mem.latest import BwaMemLatest
from janis_bioinformatics.tools.samtools.view.view import SamToolsView_1_9
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_3
from janis_bioinformatics.data_types import Fastq, FastaWithDict

w = janis.Workflow("alignmentWorkflow")

# Inputs
w.input("readGroup", janis.String, value="'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")
w.input("fastq", Fastq, value=[
    "/Users/franklinmichael/source/janis-workshops/workshop2/data/BRCA1_R1.fastq.gz",
    "/Users/franklinmichael/source/janis-workshops/workshop2/data/BRCA1_R2.fastq.gz",
])
w.input("reference", FastaWithDict, 
value="/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta")

# Steps
w.step(
    "bwamem", 
    BwaMemLatest, 
    reads=w.fastq, 
    readGroupHeaderLine=w.readGroup, 
    reference=w.reference
)
w.step("samtoolsview", SamToolsView_1_9, sam=w.bwamem.out)
w.step(
    "sortsam",
    Gatk4SortSam_4_1_3,
    bam=w.samtoolsview.out,
    sortOrder="coordinate",
    createIndex=True,
    validationStringency="SILENT",
    maxRecordsInRam=5000000,
)

# Outputs
w.output("out", source=w.sortsam.out)
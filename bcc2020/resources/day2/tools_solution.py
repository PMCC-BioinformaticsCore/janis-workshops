from janis_core import (
    CommandToolBuilder,
    ToolInput,
    ToolOutput,
    InputSelector,
    Array,
    File,
    Filename,
    Boolean,
)

from janis_bioinformatics.data_types import Bam, BamBai, FastaWithIndexes, VcfTabix, Vcf

# Add tool definitions here

Gatk4BaseRecalibrator_4_1_4 = CommandToolBuilder(
    tool="Gatk4BaseRecalibrator",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "BaseRecalibrator"],
    
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("outputFilename", Filename(extension=".table"), prefix="--output"),
        ToolInput("knownSites", Array(VcfTabix), prefix="--known-sites", prefix_applies_to_all_elements=True),
    ],
    outputs=[
        ToolOutput("out_recalibration_report", File, selector=InputSelector("outputFilename"))
    ],
)

Gatk4ApplyBQSR_4_1_4 = CommandToolBuilder(
    tool="Gatk4ApplyBqsr",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "ApplyBQSR"],
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("recalFile", File, prefix="--bqsr-recal-file"),
        ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".recal", extension=".bam"), prefix="--output"),
        ToolInput("createBamIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),
    ],
    outputs=[
        ToolOutput("out_bam", BamBai, selector=InputSelector("outputFilename"), secondaries_present_as={".bai": "^.bai"},)
    ],
)

Gatk4HaplotypeCaller_4_1_4 = CommandToolBuilder(
    tool="Gatk4HaplotypeCaller",
    container="broadinstitute/gatk:4.1.4.0",
    version="v4.1.4.0",
    base_command=["gatk", "HaplotypeCaller"],
    inputs=[
        ToolInput("bam", BamBai, prefix="--input"),
        ToolInput("reference", FastaWithIndexes, prefix="--reference"),
        ToolInput("outputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), extension=".vcf.gz"), prefix="--output"),
        ToolInput("bamOutputFilename", Filename(prefix=InputSelector("bam", remove_file_extension=True), suffix=".HAP", extension=".bam"), prefix="--bam-output"),
        ToolInput("createBamOutputIndex", Boolean(optional=True), prefix="--create-output-bam-index", default=True),
    ],
    outputs=[
        ToolOutput("out_vcf", VcfTabix, selector=InputSelector("outputFilename")),
        ToolOutput("out_bam", BamBai, selector=InputSelector("bamOutputFilename"), secondaries_present_as={".bai": "^.bai"}),
    ],
)

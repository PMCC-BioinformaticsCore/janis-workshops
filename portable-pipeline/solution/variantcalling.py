from typing import Dict, Any, List, Union

from janis_core import (
    Workflow,
    WorkflowBuilder,
    PythonTool,
    Array,
    String,
    Int,
    TOutput,
    ToolMetadata,
    Boolean,
    # Command tool tthings
    CommandToolBuilder,
    ToolInput,
    ToolOutput,
    Filename,
    InputSelector,
)

from janis_core.operators.logical import If
from janis_core.operators.standard import FilterNullOperator

from janis_bioinformatics.data_types import (
    FastaWithIndexes,
    VcfIdx,
    FastqGzPair,
    FastaDict,
    VcfTabix,
)

from janis_bioinformatics.data_types import Bam, BamBai, FastaWithIndexes, Bed

from janis_bioinformatics.tools.gatk4 import Gatk4HaplotypeCaller_4_1_4


class Gatk4GermlineSnpsIndels(Workflow):
    """
    Based on: https://github.com/gatk-workflows/gatk4-germline-snps-indels/blob/6d70cd35c31165703da77d005ed8c43ec9f46003/haplotypecaller-gvcf-gatk4.wdl
    """

    def id(self):
        return "Gatk4GermlineSnpsIndels"

    def friendly_name(self):
        return "BCC: Workshop (variant calling)"

    def version(self):
        return "v0.1.0"

    def bind_metadata(self):
        return ToolMetadata(contributors=["Michael Franklin"],)

    def constructor(self):

        self.input("input_bam", BamBai)
        self.input("ref_fasta", FastaWithIndexes)
        self.input("intervals", Array(Bed))

        self.step(
            "haplotype_caller",
            Gatk4HaplotypeCaller_4_1_4(
                inputRead=self.input_bam,
                reference=self.ref_fasta,
                intervals=self.intervals,
                gvcfGqBands=[10, 20, 30, 40, 50, 60, 70, 80, 90],
                contaminationFractionToFilter=0.0,
                annotationGroup=[
                    "StandardAnnotation",
                    "StandardHCAnnotation",
                    # "AS_StandardAnnotation",
                ],
            ),
            scatter="intervals",
        )

        self.step("merge", Gatk4MergeVcfs_4_1_4(vcfs=self.haplotype_caller.out))

        self.output("output_vcf", source=self.merge.output_vcf)


Gatk4MergeVcfs_4_1_4 = CommandToolBuilder(
    tool="Gatk4MergeVcfs",
    base_command=["gatk", "MergeVcfs"],
    inputs=[
        ToolInput(
            "vcfs",
            Array(VcfTabix),
            prefix="--INPUT",
            prefix_applies_to_all_elements=True,
        ),
        ToolInput(
            "output_filename",
            Filename(suffix=".merged", extension=".vcf.gz"),
            prefix="--OUTPUT",
        ),
    ],
    outputs=[ToolOutput("output_vcf", VcfTabix, glob=InputSelector("output_filename"))],
    version="4.1.4.0",
    container="broadinstitute/gatk:4.1.4.0",
)


if __name__ == "__main__":
    Gatk4GermlineSnpsIndels().translate("wdl")
    # Gatk4MergeVcfs_4_1_4().translate("wdl")


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
)
from janis_bioinformatics.data_types import (
    FastaWithIndexes,
    VcfIdx,
    FastqGzPair,
    FastaDict,
    VcfTabix,
)

from janis_bioinformatics.tools.common import BwaMem_SamToolsView
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MarkDuplicates_4_1_4,
    Gatk4SortSam_4_1_4,
    Gatk4SetNmMdAndUqTags_4_1_4,
    Gatk4BaseRecalibrator_4_1_4,
    Gatk4GatherBQSRReports_4_1_4,
    Gatk4ApplyBqsr_4_1_4,
    Gatk4GatherBamFiles_4_1_4,
)


class Gatk4DataPreprocessing(Workflow):
    """
    Based on: https://github.com/gatk-workflows/gatk4-data-processing/blob/master/processing-for-variant-discovery-gatk4.wdl
    """

    def id(self):
        return "Gatk4DataPreprocessing"

    def friendly_name(self):
        return "BCC: Workshop"

    def version(self):
        return "v0.1.0"

    def bind_metadata(self):
        return ToolMetadata(contributors=["Michael Franklin"],)

    def constructor(self):

        self.input("sample_name", String)
        self.input("reads_list", Array(FastqGzPair))

        self.input("ref_name", String)
        self.input("ref_fasta", FastaWithIndexes)

        # self.input("dbSNP", VcfTabix)
        self.input("known_indels_sites", Array(VcfTabix))

        self.input("compression_level", Int, default=5)

        self.step(
            "align",
            BwaMem_SamToolsView(
                sampleName=self.sample_name,
                reads=self.reads_list,
                reference=self.ref_fasta,
                assumeInterleavedFirstInput=True,  # -p
                verboseLevel=3,  # -v
                batchSize=100000000,  # -k
                useSoftClippingForSupplementaryAlignments=True,  # -Y
            ),
            scatter="reads",
        )

        self.step(
            "mark_duplicates",
            Gatk4MarkDuplicates_4_1_4(
                bam=self.align.out,
                validationStringency="SILENT",
                opticalDuplicatePixelDistance=2500,
                # createMd5File=True,
                assumeSortOrder="queryname",
            ),
        )

        self.step(
            "sort",
            Gatk4SortSam_4_1_4(
                bam=self.mark_duplicates.out,
                # reference=self.ref_fasta,
                sortOrder="coordinate",
                compression_level=self.compression_level,
            ),
        )

        self.output("analysis_ready_bam", source=self.sort.out)


class CreateSequenceGroupings(PythonTool):
    """
    Based on: https://github.com/gatk-workflows/gatk4-data-processing/blob/3d0faa426d43098003050a445e17127cee025389/processing-for-variant-discovery-gatk4.wdl#L491-L548
    
    """

    def id(self):
        return "CreateSequenceGroupings"

    def version(self):
        return "v0.1.0"

    @staticmethod
    def code_block(ref_fasta: FastaDict) -> Dict[str, Any]:

        ref_dict = ".".join(ref_fasta.split(".")[:-1]) + ".dict"
        sequence_tuples = []
        with open(ref_dict, "r") as ref_dict_file:
            longest_sequence = 0
            for line in ref_dict_file:
                if line.startswith("@SQ"):
                    line_split = line.split("\t")
                    # (Sequence_Name, Sequence_Length)
                    sequence_tuples.append(
                        [
                            line_split[1].split("SN:")[1],
                            int(line_split[2].split("LN:")[1]),
                        ]
                    )
            longest_sequence = sorted(
                sequence_tuples, key=lambda x: x[1], reverse=True
            )[0][1]

        # We are adding this to the intervals because hg38 has contigs named with embedded colons (:) and a bug in
        # some versions of GATK strips off the last element after a colon, so we add this as a sacrificial element.
        hg38_protection_tag = ":1+"

        temp_size = sequence_tuples[0][1]
        processed_sequences = [[sequence_tuples[0][0] + hg38_protection_tag]]

        for sequence_tuple in sequence_tuples[1:]:
            if temp_size + sequence_tuple[1] <= longest_sequence:
                temp_size += sequence_tuple[1]
                processed_sequences[-1].append(sequence_tuple[0] + hg38_protection_tag)
            else:
                processed_sequences.append([sequence_tuple[0] + hg38_protection_tag])
                temp_size = sequence_tuple[1]

        return {
            "sequence_groupings": processed_sequences,
            "sequence_groupings_with_unmapped": [*processed_sequences, ["unmapped"]],
        }

    def outputs(self):
        return [
            TOutput("sequence_groupings", Array(Array(String))),
            TOutput("sequence_groupings_with_unmapped", Array(Array(String))),
        ]


if __name__ == "__main__":
    Gatk4DataPreprocessing().translate("cwl")

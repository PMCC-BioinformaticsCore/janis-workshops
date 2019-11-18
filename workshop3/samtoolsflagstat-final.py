from typing import List, Optional, Union
import janis as j
from janis.data_types import Bam

class SamtoolsFlagstat(j.CommandTool):
    @staticmethod
    def tool() -> str:
        return "samtoolsflagstat"

    @staticmethod
    def base_command() -> Optional[Union[str, List[str]]]:
        return ["samtools", "flagstat"]

    @staticmethod
    def container() -> str:
        return "quay.io/biocontainers/samtools:1.9--h8571acd_11"

    @staticmethod
    def version() -> str:
        return "1.9.0"

    def inputs(self) -> List[j.ToolInput]:
        return [
        j.ToolInput(
             "bam", 
             Bam, 
             position=1, 
             doc="Input bam to generate statistics for"
        ),
        # 2. `threads` inputs
        j.ToolInput(
            "threads", 
            j.Int(optional=True), 
            prefix="--threads", 
            doc="(-@)  Number of additional threads to use [0] "
        )
    ]

    def outputs(self) -> List[j.ToolOutput]:
        return [j.ToolOutput("out", j.Stdout)]
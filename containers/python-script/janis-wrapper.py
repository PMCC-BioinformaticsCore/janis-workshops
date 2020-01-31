"""
    This file is the template for a CommandTool, specifically for the 
    Samtools Flagstat tutorial but it's applicable for all tools.

    Author: Michael Franklin (November, 2019)
"""

from typing import List, Optional, Union
import janis as j

class ToolName(j.CommandTool):
    @staticmethod
    def tool() -> str:
        return "helloscript"
        
    @staticmethod
    def base_command() -> Optional[Union[str, List[str]]]:
        return ["hello.py"]
        
    @staticmethod
    def container() -> str:
        return "michaelfranklin/py:latest"

    @staticmethod
    def version() -> str:
        return "v0.1.0"

    def inputs(self) -> List[j.ToolInput]:
        return []

    def outputs(self) -> List[j.ToolOutput]:
        return [j.ToolOutput("out", j.Stderr)]
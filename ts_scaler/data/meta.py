from dataclasses import dataclass
from typing import Dict


@dataclass
class Metadata:
    column_mappings: Dict[str, str]

    @staticmethod
    def nyiso():
        return Metadata(
            column_mappings={
                "Time Stamp": "time_stamp",
                "Time Zone": "time_zone",
                "Integrated Load": "integrated_load",
            }
        )

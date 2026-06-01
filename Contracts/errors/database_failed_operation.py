from typing import Literal
from dataclasses import dataclass

@dataclass
class DataBaseFailedOpertaion(Exception):
    
    operation_type : Literal["CREATE","READ","UPDATE","DELETE"]
    databse_name: str
    database_collection: str
    description: str|None

    def __str__(self)->str:
        return f"On databse '{self.databse_name}', collection '{self.database_collection}' error tryng to {self.operation_type.lower()}, {self.description or ''} "

from dataclasses import dataclass
@dataclass
class Config:
    min_score:float = 0.2
    top_k:int = 30
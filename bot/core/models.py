from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class BotState(str, Enum):
    STOPPED="stopped"; CONNECTING="connecting"; HOME="home"; ARMY="army"; SEARCHING="searching"; BATTLE="battle"; RESULT="result"; RECOVERY="recovery"; UNKNOWN="unknown"

@dataclass
class Target:
    gold:int=0; elixir:int=0; dark_elixir:int=0; trophies:int=0; confidence:float=0.0; score:float=0.0

@dataclass
class RuntimeStatus:
    state:BotState=BotState.STOPPED; connected:bool=False; running:bool=False; searches:int=0; attacks:int=0; errors:int=0; last_error:str|None=None; target:Target|None=None; metadata:dict[str,Any]=field(default_factory=dict)

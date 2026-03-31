from dataclasses import dataclass
from typing import Optional


@dataclass
class Material:
    id: Optional[str] = None
    name: Optional[str] = None
    density: Optional[float] = None
    appearance_name: Optional[str] = None


@dataclass
class FusionAppearance:
    id: Optional[str] = None
    name: Optional[str] = None

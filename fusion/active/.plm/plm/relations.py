from dataclasses import dataclass
from typing import Optional


@dataclass
class FusionRelation:
    quantity: Optional[float] = None
    relation_type: Optional[str] = None


@dataclass
class FusionComponentRelation(FusionRelation):
    parent_fusion_id: Optional[str] = None
    parent_revision_id: Optional[str] = None
    child_fusion_id: Optional[str] = None
    child_revision_id: Optional[str] = None


@dataclass
class FusionBomRelation(FusionRelation):
    parent_fusion_id: Optional[str] = None
    parent_revision_id: Optional[str] = None
    child_fusion_id: Optional[str] = None
    child_revision_id: Optional[str] = None

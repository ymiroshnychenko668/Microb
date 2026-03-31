from dataclasses import dataclass, field
from typing import List, Optional, Dict

from plm.types import Vector3D, Matrix3D, BoundingBox
from plm.material import Material, FusionAppearance
from plm.relations import FusionComponentRelation, FusionBomRelation


@dataclass
class FusionThread:
    diameter: Optional[float] = None
    thread_description: Optional[str] = None
    is_internal: Optional[bool] = None
    is_modeled: Optional[bool] = None


@dataclass
class FusionJointMotion:
    joint_id: Optional[str] = None
    rotation_axis_x: Optional[float] = None
    rotation_axis_y: Optional[float] = None
    rotation_axis_z: Optional[float] = None
    rotation_value: Optional[float] = None
    rotation_min: Optional[float] = None
    rotation_max: Optional[float] = None
    rotation_min_enabled: Optional[bool] = None
    rotation_max_enabled: Optional[bool] = None
    slide_direction_x: Optional[float] = None
    slide_direction_y: Optional[float] = None
    slide_direction_z: Optional[float] = None
    slide_value: Optional[float] = None
    slide_min: Optional[float] = None
    slide_max: Optional[float] = None
    slide_min_enabled: Optional[bool] = None
    slide_max_enabled: Optional[bool] = None
    pitch_value: Optional[float] = None
    yaw_value: Optional[float] = None
    roll_value: Optional[float] = None


@dataclass
class FusionRigidGroupMember:
    rigid_group_id: Optional[str] = None
    component_fusion_id: Optional[str] = None
    component_revision_id: Optional[str] = None
    occurrence_path: Optional[str] = None
    fusion_entity_token: Optional[str] = None


@dataclass
class FusionRigidGroup:
    rigid_group_id: Optional[str] = None
    name: Optional[str] = None
    bom_id: Optional[str] = None
    suppressed: Optional[bool] = None
    fusion_entity_token: Optional[str] = None
    members: List[FusionRigidGroupMember] = field(default_factory=list)


@dataclass
class FusionJoint:
    joint_id: Optional[str] = None
    name: Optional[str] = None
    joint_type: Optional[str] = None
    bom_id: Optional[str] = None
    component_one_fusion_id: Optional[str] = None
    component_one_revision_id: Optional[str] = None
    component_two_fusion_id: Optional[str] = None
    component_two_revision_id: Optional[str] = None
    occurrence_one_path: Optional[str] = None
    occurrence_two_path: Optional[str] = None
    locked: Optional[bool] = None
    suppressed: Optional[bool] = None
    flipped: Optional[bool] = None
    fusion_entity_token: Optional[str] = None
    motion: Optional[FusionJointMotion] = None


@dataclass
class FusionBody:
    body_id: Optional[str] = None
    body_name: Optional[str] = None
    type: Optional[str] = None
    is_visible: Optional[bool] = None
    length_mm: Optional[float] = None
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    mass_kg: Optional[float] = None
    area_cm2: Optional[float] = None
    density_kg_cm3: Optional[float] = None
    volume_cm3: Optional[float] = None
    material: Optional[Material] = None
    appearance: Optional[FusionAppearance] = None


@dataclass
class FusionOccurrence:
    occurrence_id: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    component_fusion_id: Optional[str] = None
    component_revision_id: Optional[str] = None
    is_visible: Optional[bool] = None
    is_light_bulb_on: Optional[bool] = None
    appearance: Optional[FusionAppearance] = None
    world_transform: Optional[Matrix3D] = None
    local_transform: Optional[Matrix3D] = None
    translation: Optional[Vector3D] = None


@dataclass
class ManifestRef:
    fusion_id: Optional[str] = None
    name: Optional[str] = None
    quantity: float = 1.0


@dataclass
class FusionPhysicalProperty:
    component_fusion_id: Optional[str] = None
    component_revision_id: Optional[str] = None
    body_name: Optional[str] = None
    width_mm: Optional[float] = None
    length_mm: Optional[float] = None
    height_mm: Optional[float] = None
    volume_cm3: Optional[float] = None
    area_cm2: Optional[float] = None
    mass_kg: Optional[float] = None
    density_kg_cm3: Optional[float] = None
    material: Optional['Material'] = None


@dataclass
class FusionComponent:
    fusion_id: Optional[str] = None
    revision_id: Optional[str] = None
    bom_id: Optional[str] = None
    bom_revision_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    part_name: Optional[str] = None
    source_file: Optional[str] = None
    path: Optional[str] = None
    entity_token: Optional[str] = None
    type: Optional[str] = None
    is_root: Optional[bool] = None
    is_library_item: Optional[bool] = None
    is_configuration: Optional[bool] = None
    is_configured_design: Optional[bool] = None
    is_external_bom: Optional[bool] = None
    material: Optional[Material] = None
    appearance: Optional[FusionAppearance] = None
    bounding_box: Optional[BoundingBox] = None
    bodies: List[FusionBody] = field(default_factory=list)
    attributes: Optional[Dict[str, Dict[str, str]]] = None
    threads: List[FusionThread] = field(default_factory=list)
    occurrences: List[FusionOccurrence] = field(default_factory=list)
    joints: List[FusionJoint] = field(default_factory=list)
    rigid_groups: List[FusionRigidGroup] = field(default_factory=list)

    def mass(self):
        """Total mass from all bodies."""
        return sum(b.mass_kg or 0.0 for b in self.bodies)

    def volume(self):
        """Total volume from all bodies."""
        return sum(b.volume_cm3 or 0.0 for b in self.bodies)


@dataclass
class FusionBom:
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    design_id: Optional[str] = None
    fusion_id: Optional[str] = None
    revision_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    version: Optional[str] = None
    is_parametric: Optional[bool] = None
    is_assembly: Optional[bool] = None
    product_id: Optional[int] = None
    engineering_bom_id: Optional[int] = None
    step_file_url: Optional[str] = None
    components: List[FusionComponent] = field(default_factory=list)
    component_relations: List[FusionComponentRelation] = field(default_factory=list)
    component_refs: List[ManifestRef] = field(default_factory=list)
    sub_bom_refs: List[ManifestRef] = field(default_factory=list)

    def component_count(self):
        """Number of unique components."""
        return len(self.components)

    def find_component(self, fusion_id: str):
        """Find component by fusion_id."""
        return next((c for c in self.components if c.fusion_id == fusion_id), None)

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Vector3D:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


@dataclass
class Matrix3D:
    m00: float = 1.0
    m01: float = 0.0
    m02: float = 0.0
    m03: float = 0.0
    m10: float = 0.0
    m11: float = 1.0
    m12: float = 0.0
    m13: float = 0.0
    m20: float = 0.0
    m21: float = 0.0
    m22: float = 1.0
    m23: float = 0.0
    m30: float = 0.0
    m31: float = 0.0
    m32: float = 0.0
    m33: float = 1.0

    def translation(self) -> Vector3D:
        return Vector3D(x=self.m03, y=self.m13, z=self.m23)


@dataclass
class BoundingBox:
    min_point: Optional[Vector3D] = None
    max_point: Optional[Vector3D] = None

    def dimensions(self) -> Vector3D:
        if self.min_point is None or self.max_point is None:
            return Vector3D()
        return Vector3D(
            x=self.max_point.x - self.min_point.x,
            y=self.max_point.y - self.min_point.y,
            z=self.max_point.z - self.min_point.z,
        )

    def volume(self) -> float:
        d = self.dimensions()
        return d.x * d.y * d.z

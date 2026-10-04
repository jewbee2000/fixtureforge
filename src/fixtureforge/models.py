"""Versioned, finite, bounded data-only contracts. No CAD imports here."""
from pathlib import PurePosixPath, PureWindowsPath
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Number = Annotated[float, Field(allow_inf_nan=False, ge=-1000, le=1000)]
Positive = Annotated[float, Field(allow_inf_nan=False, gt=0, le=500)]
Vector = tuple[Number, Number, Number]
Identifier = Annotated[str, Field(pattern=r'^[A-Za-z][A-Za-z0-9_-]{0,63}$')]


class Contract(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_default=True, allow_inf_nan=False)


class FixtureSpec(Contract):
    schema_version: Literal['1.0'] = '1.0'
    units: Literal['mm'] = 'mm'
    sensor_diameter_mm: float = Field(default=24, ge=12, le=40)
    sensor_length_mm: float = Field(default=40, ge=25, le=80)
    clearance_mm: float = Field(default=0.4, ge=0.2, le=1)
    wall_mm: float = Field(default=3, ge=2.4, le=6)
    base_mm: float = Field(default=5, ge=5, le=12)
    mount_pitch_x_mm: float = Field(default=40, ge=32, le=160)
    mount_pitch_y_mm: float = Field(default=64, ge=32, le=160)
    connector_length_mm: float = Field(default=12, ge=1, le=40)
    connector_width_mm: float = Field(default=12, ge=1, le=40)
    connector_height_mm: float = Field(default=12, ge=1, le=40)
    cable_exit_mm: float = Field(default=8, ge=0, le=40)
    connector_end: Literal['+x', '-x'] = '+x'
    manufacturing_profile: Literal['fdm-0.4-0.2-v1'] = 'fdm-0.4-0.2-v1'
    assembly_direction: Literal['+z'] = '+z'
    assumption_source: str = Field(default='Synthetic reference; SPEC.md', min_length=1, max_length=500)

    @model_validator(mode='after')
    def feasible(self):
        r = (self.sensor_diameter_mm + self.clearance_mm) / 2
        minimum = 2 * (r + self.wall_mm + 14)
        if self.mount_pitch_y_mm < minimum:
            raise ValueError(f'FF-01: mount_pitch_y_mm must be >= {minimum:g} for bore, wall and ears')
        if self.connector_height_mm > 2 * (r + self.wall_mm):
            raise ValueError('FF-01: connector height reaches the base mounting plane')
        return self


class Envelope(Contract):
    kind: Literal['box', 'cylinder']
    size_mm: tuple[Positive, Positive, Positive] | None = None
    radius_mm: Positive | None = None
    height_mm: Positive | None = None
    axis: Literal['x', 'y', 'z'] = 'z'

    @model_validator(mode='after')
    def complete(self):
        if self.kind == 'box':
            if self.size_mm is None or self.radius_mm is not None or self.height_mm is not None:
                raise ValueError('box requires size_mm only')
        elif self.radius_mm is None or self.height_mm is None or self.size_mm is not None:
            raise ValueError('cylinder requires radius_mm and height_mm only')
        return self


class PartSpec(Contract):
    id: Identifier
    file: str = Field(min_length=1, max_length=200)
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    translation_mm: Vector = (0, 0, 0)

    @model_validator(mode='after')
    def local_file(self):
        for cls in (PurePosixPath, PureWindowsPath):
            p = cls(self.file)
            if p.is_absolute() or p.drive or '..' in p.parts:
                raise ValueError('part file must be relative with no path traversal')
        if ':' in self.file or '\\' in self.file or not self.file.lower().endswith(('.step', '.stp')):
            raise ValueError('use relative forward-slash STEP paths')
        return self


class AccessPath(Contract):
    id: Identifier
    requirement: Literal['FF-04', 'FF-05', 'FF-14', 'FF-15'] = 'FF-15'
    envelope: Envelope
    start_mm: Vector
    end_mm: Vector
    motion: Literal['straight'] = 'straight'
    orientation_deg: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)
    end_orientation_deg: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)
    occupied: list[Identifier] = Field(min_length=1, max_length=20)
    intended_end_contacts: list[Identifier] = Field(default_factory=list, max_length=20)
    margin_mm: float = Field(default=0, ge=0, le=20)
    purpose: str = Field(default='Explicit nominal access envelope', max_length=500)

    @model_validator(mode='after')
    def valid_contacts(self):
        if len(set(self.occupied)) != len(self.occupied):
            raise ValueError('duplicate occupancy')
        if not set(self.intended_end_contacts) <= set(self.occupied):
            raise ValueError('contact must name an occupied part')
        return self


class AccessSpec(Contract):
    schema_version: Literal['1.0']
    units: Literal['mm']
    parts: list[PartSpec] = Field(min_length=1, max_length=20)
    paths: list[AccessPath] = Field(min_length=1, max_length=40)
    datums: dict[str, Vector] = Field(default_factory=lambda: {'origin': (0.0, 0.0, 0.0)}, max_length=12)
    assumptions: list[str] = Field(default_factory=list, max_length=20)

    @model_validator(mode='after')
    def references(self):
        ids = {part.id for part in self.parts}
        if len(ids) != len(self.parts) or len({p.id for p in self.paths}) != len(self.paths):
            raise ValueError('ambiguous duplicate part/path IDs')
        for path in self.paths:
            if not set(path.occupied) <= ids:
                raise ValueError(f'{path.id}: unknown occupied part')
        if any(len(a) > 1000 for a in self.assumptions):
            raise ValueError('assumption length limit')
        return self

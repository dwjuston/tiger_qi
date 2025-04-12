from __future__ import annotations

from enums import UnitClan
from grid_position import GridPosition
import uuid

class Unit:
    uuid: str
    name: str
    unit_clan: UnitClan
    is_marching: bool = False
    priority: int = 1

    face = GridPosition
    loc: GridPosition
    health = 5
    attack = 1
    relative_attack_range: list[GridPosition] = [GridPosition(-1, 0), GridPosition(1, 0), GridPosition(0, 1)]  # relative position
    group_id: int = 1

    max_x: int
    max_y: int

    def __init__(self, name: str, unit_clan: UnitClan, loc: GridPosition, face: GridPosition) -> None:
        self.uuid = uuid.uuid4().hex[0:8]  # generate a unique ID for the unit
        self.name = name
        self.unit_clan = unit_clan
        self.loc = loc
        self.face = face
        self.is_marching = True

    def set_group_id(self, group_id: int) -> None:
        self.group_id = group_id

    @property
    def attack_range(self):
        li = []

        # adjust relative attack range based on face direction
        adjusted_relative_attack_range = [rng.adjust_with_direction(self.face) for rng in self.relative_attack_range]

        for rel_pos in adjusted_relative_attack_range:
            new_grid_position = self.loc + rel_pos
            li.append(new_grid_position)
        return li

    @property
    def move_destination(self) -> GridPosition | None:
        if not self.is_marching:
            return None

        new_position = self.loc + self.face
        return new_position
"""
Module for handling movement collisions in the grid game.
Contains stateless functions to resolve each collision case.
"""
import random
from typing import List, Tuple, Dict, Optional
from grid_position import GridPosition
from Unit import Unit
from enums import UnitClan


def resolve_boundary_collision(
        movement_requests: Dict[GridPosition, List[Unit]],
        grid_rows: int,
        grid_cols: int
) -> Dict[GridPosition, List[Unit]]:
    """

    """
    keys_to_remove = []
    for destination, unit_list in list(movement_requests.items()):
        # Check if the destination is out of bounds
        if not destination.check_bounds(grid_rows, grid_cols):
            # Remove the destination from the movement requests
            keys_to_remove.append(destination)

    # Remove invalid destinations from the movement requests
    for key in keys_to_remove:
        del movement_requests[key]

    return movement_requests


def resolve_occupied_cell_collision(
        movement_requests: Dict[GridPosition, List[Unit]],
        units: Dict[GridPosition, Unit]
) -> Dict[GridPosition, List[Unit]]:
    """
    """

    keys_to_remove = []

    for destination, unit_list in movement_requests.items():
        if destination in units:
            occupying_unit = units[destination]
            if not occupying_unit.is_marching:
                keys_to_remove.append(destination)

    # Remove invalid destinations from the movement requests
    for key in keys_to_remove:
        del movement_requests[key]
    return movement_requests


def resolve_multiple_units_collision(
        movement_requests: Dict[GridPosition, List[Unit]]
) -> Dict[GridPosition, Unit]:
    result_dict = {}
    for destination, unit_list in movement_requests.items():
        max_priority = max(unit.priority for unit in unit_list)
        filtered_unit_list = [unit for unit in unit_list if unit.priority == max_priority]
        chosen_unit = random.choice(filtered_unit_list)
        result_dict[destination] = chosen_unit
    return result_dict


def resolve_opposite_clan_collision(
        movement_requests_single: Dict[GridPosition, Unit],
        units: Dict[GridPosition, Unit],
) -> Dict[GridPosition, Unit]:
    """
    """
    # find pairs that are opposite clans and bump into each other

    keys_to_remove = set()

    for destination, unit in movement_requests_single.items():
        if destination in keys_to_remove:
            continue

        origin = unit.loc
        unit2 = units.get(destination)
        # if the destination is occupied by a unit of the opposite clan
        if unit2 and unit2.unit_clan != unit.unit_clan:
            # if the opponent is marching towards the unit
            if unit2.is_marching and movement_requests_single.get(origin) == unit2:
                keys_to_remove.add(destination)
                keys_to_remove.add(origin)

    # Remove invalid destinations from the movement requests
    for key in keys_to_remove:
        del movement_requests_single[key]
    return movement_requests_single


def resolve_movement_collision(
        movement_requests: Dict[GridPosition, List[Unit]],
        units: Dict[GridPosition, Unit],
        grid_rows: int,
        grid_cols: int
) -> Dict[GridPosition, Unit]:
    """
    """
    # Step 1: Remove keys
    movement_requests = resolve_boundary_collision(movement_requests, grid_rows, grid_cols)
    movement_requests = resolve_occupied_cell_collision(movement_requests, units)

    # Step 2: Shrink the movement requests into a single unit
    movement_requests_single = resolve_multiple_units_collision(movement_requests)

    # Step 3: Remove opposite clan collisions
    movement_requests_single = resolve_opposite_clan_collision(movement_requests_single, units)

    return movement_requests_single

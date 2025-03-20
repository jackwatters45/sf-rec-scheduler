from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class TimeSlotDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    is_booked: bool = Field(alias="status")
    time: str


class FieldInfo(BaseModel):
    resource_id: int
    resource_name: str
    time_slots: List[str]
    time_slot_details: List[TimeSlotDetail]


def find_available_fields(
    fields: List[FieldInfo],
    primary_time: str,
    alternate_times: Optional[List[str]] = None,
    field_prefix: Optional[str] = None,
) -> Tuple[Optional[FieldInfo], str]:
    """
    Find available fields matching the specified criteria.

    Args:
        fields (List[FieldInfo]): List of fields to search through
        primary_time (str): Primary time to check for availability
        alternate_times (Optional[List[str]]): List of alternate times to check if primary time is unavailable
        field_prefix (Optional[str]): Prefix to filter field names by

    Returns:
        Tuple[Optional[FieldInfo], str]: Tuple containing the available field (if any) and the selected time
    """
    # Filter fields by prefix if specified
    if field_prefix:
        fields = [
            field for field in fields if field.resource_name.startswith(field_prefix)
        ]

    # Try primary time first
    available_fields = [
        field
        for field in fields
        if any(
            detail.time == primary_time and not detail.is_booked
            for detail in field.time_slot_details
        )
    ]

    selected_time = primary_time

    # If no fields available at primary time and alternate times are specified, try each alternate time
    if not available_fields and alternate_times:
        for alt_time in alternate_times:
            available_fields = [
                field
                for field in fields
                if any(
                    detail.time == alt_time and not detail.is_booked
                    for detail in field.time_slot_details
                )
            ]
            if available_fields:
                selected_time = alt_time
                break

    return (available_fields[0] if available_fields else None, selected_time)

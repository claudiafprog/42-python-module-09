#!/usr/bin/env python3

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-09-17T10:00:00"),
            is_operational=True,
            notes="All systems nominal."
        )
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        if valid_station.is_operational:
            status_str = "Operational"
        else:
            status_str = "Offline"
        print(f"Status: {status_str}")
    except ValidationError as err:
        print(f"Unexpected error: {err}")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS_BAD",
            name="Bad Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.fromisoformat("2026-09-17T10:00:00"),
        )
    except ValidationError as err:
        for error in err.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()

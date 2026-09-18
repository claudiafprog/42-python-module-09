#!/usr/bin/env python3

from enum import Enum
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def safety_requirements(self) -> Any:
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        has_leader = any(
                m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew
            )
        if not has_leader:
            raise ValueError("Mission requires at least one Commander "
                             "or Captain")
        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if (experienced_count / len(self.crew)) < 0.5:
                raise ValueError("Long missions need 50% experienced "
                                 "crew (5+ years)")
        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    try:
        info = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-10-01T00:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001", name="Sarah Connor",
                    rank=Rank.COMMANDER, age=40,
                    specialization="Mission Command", years_experience=15
                ),
                CrewMember(
                    member_id="C002", name="John Smith",
                    rank=Rank.LIEUTENANT, age=32,
                    specialization="Navigation", years_experience=6
                ),
                CrewMember(
                    member_id="C003", name="Alice Johnson",
                    rank=Rank.OFFICER, age=28,
                    specialization="Engineering", years_experience=2
                ),
            ]
        )
        print("Valid mission created:")
        print(f"Mission: {info.mission_name}")
        print(f"ID: {info.mission_id}")
        print(f"Destination: {info.destination}")
        print(f"Duration: {info.duration_days} days")
        print(f"Budget: ${info.budget_millions}M")
        print(f"Crew size: {len(info.crew)}")
        print("Crew members:")
        for member in info.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
    except ValidationError as err:
        print(f"Unexpected error: {err}")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        info = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-10-01T00:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001", name="Sarah Connor",
                    rank=Rank.CADET, age=40,
                    specialization="Mission Command", years_experience=15
                ),
                CrewMember(
                    member_id="C002", name="John Smith",
                    rank=Rank.LIEUTENANT, age=32,
                    specialization="Navigation", years_experience=6
                ),
                CrewMember(
                    member_id="C003", name="Alice Johnson",
                    rank=Rank.OFFICER, age=28,
                    specialization="Engineering", years_experience=2
                ),
            ]
        )
    except ValidationError as err:
        for error in err.errors():
            msg = error.get("msg", "")
            if msg.startswith("Value error, "):
                msg = msg[len("Value error, "):]
            print(msg)


if __name__ == "__main__":
    main()

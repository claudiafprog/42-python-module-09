#!/usr/bin/env python3

from enum import Enum
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_alien_rules(self) -> Any:
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires at "
                                 "least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) must include a message")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    try:
        alien_message = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-09-17T12:00:00"),
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="'Greetings from Zeta Reticuli'"
        )
        print("Valid contact report:")
        print(f"ID: {alien_message.contact_id}")
        print(f"Type: {alien_message.contact_type}")
        print(f"Location: {alien_message.location}")
        print(f"Signal: {alien_message.signal_strength}/10")
        print(f"Duration: {alien_message.duration_minutes} minutes")
        print(f"Witnesses: {alien_message.witness_count}")
        print(f"Message: {alien_message.message_received}")
    except ValidationError as err:
        print(f"Unexpected error: {err}")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        alien_message = AlienContact(
            contact_id="AC_BAD_001",
            timestamp=datetime.fromisoformat("2026-09-17T12:00:00"),
            contact_type=ContactType.TELEPATHIC,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received=None
        )
        print(f"ID: {alien_message.contact_id}")
        print(f"Type: {alien_message.contact_type}")
        print(f"Location: {alien_message.location}")
        print(f"Signal: {alien_message.signal_strength}")
        print(f"Duration: {alien_message.duration_minutes}")
        print(f"Witnesses: {alien_message.witness_count}")
        print(f"Message: {alien_message.message_received}")
    except ValidationError as err:
        for error in err.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()

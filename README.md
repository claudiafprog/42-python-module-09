# Cosmic Data — Pydantic Models & Validation

Master Pydantic v2 data validation through space-themed data engineering exercises.

---

## 📁 Repository Structure

```text
├── generated_data/            # Pre-generated test data / integration outputs
├── data_generator.py          # Provided test data generator
├── data_exporter.py           # Provided export utility (JSON/CSV/Python)
├── ex0/
│   └── space_station.py       # SpaceStation model + main() demonstration
├── ex1/
│   └── alien_contact.py       # ContactType enum, AlienContact model + @model_validator
└── ex2/
    └── space_crew.py          # Rank enum, CrewMember, SpaceMission + nested validation
```

# 🛠️ General Rules & Requirements
* Python: 3.10+ with virtual environment (venv, virtualenv, or conda).
* Package Manager: pip (Pydantic 2.x required).
* Standards: flake8 compliant, comprehensive type annotations (mypy ready).
* Restrictions: Standard library + pydantic only. Handle data stream exceptions gracefully.

# 📦 Exercise Breakdown
Exercise 0: Space Station Data (ex0/space_station.py)
* Focus: Basic model creation with BaseModel and Field.
* Key Fields: station_id (3-10 chars), name (1-50 chars), crew_size (1-20), power_level (0.0-100.0), oxygen_level (0.0-100.0), last_maintenance (datetime), is_operational (True), notes (optional max 200).
* Test / Demo: main() function showing valid station creation and validation error handling (e.g., crew_size > 20).

Exercise 1: Alien Contact Logs (ex1/alien_contact.py)
* Focus: Custom business logic validation via @model_validator(mode='after').
* Enums/Types: ContactType (radio, visual, physical, telepathic).
* Key Fields: contact_id (5-15 chars), timestamp (datetime), location (3-100 chars), contact_type, signal_strength (0.0-10.0), duration_minutes (1-1440), witness_count (1-100), message_received (optional max 500), is_verified (False).
* Validation Rules:
   * ID must start with "AC"
   * Physical contact must be verified (is_verified == True)
   * Telepathic contact requires $\ge 3$ witnesses
   * Strong signals ($> 7.0$) require a received message

Exercise 2: Space Crew Management (ex2/space_crew.py)
* Focus: Nested Pydantic models and relationship validation.
* Enums/Types: Rank (cadet, officer, lieutenant, captain, commander).
* Key Models:
   * CrewMember: member_id (3-10), name (2-50), rank, age (18-80), specialization (3-30), years_experience (0-50), is_active (True).
   * SpaceMission: mission_id (5-15), mission_name (3-100), destination (3-50), launch_date (datetime), duration_days (1-3650), crew (list[CrewMember], 1-12), mission_status ("planned"), budget_millions (1.0-10000.0).
* Validation Rules:
   * Mission ID must start with "M"
   * Must include at least one Commander or Captain
   * Long missions ($> 365$ days) require $\ge 50\%$ experienced crew ($\ge 5$ years experience)
   * All crew members must be active (is_active == True)
     
# 🚀 Quick Start / VerificationBash# Setup virtual environment & dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pydantic mypy flake8

# Linting & Type Checking
flake8 .
mypy .

# Run exercise demonstrations
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py


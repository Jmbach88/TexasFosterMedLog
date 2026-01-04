# Architecture Documentation

## Design Philosophy

This application is built with **separation of concerns** to enable easy interface swapping. The business logic is completely independent of the user interface.

## Layer Architecture

```
┌─────────────────────────────────────┐
│      User Interface Layer           │
│   (gui/tkinter_app.py)              │  ← Swappable
│   - Tkinter widgets                 │
│   - User interactions               │
│   - Display logic only              │
└─────────────────────────────────────┘
              ↓ uses ↓
┌─────────────────────────────────────┐
│      Business Logic Layer           │
│   (core/)                           │  ← Never changes
│   - ProfileManager                  │
│   - LogManager                      │
│   - MedicationCardManager           │
│   - ExportManager                   │
│   - No GUI dependencies             │
└─────────────────────────────────────┘
              ↓ uses ↓
┌─────────────────────────────────────┐
│      Data Storage Layer             │
│   (data/)                           │
│   - JSON files                      │
│   - File system                     │
└─────────────────────────────────────┘
```

## Core Modules (GUI-Independent)

### ProfileManager (core/profiles.py)
**Purpose:** Manage patient profile data

**Key Methods:**
- `get_all_profiles()` → Dict
- `get_profile(profile_id)` → Dict
- `create_profile(profile_data)` → profile_id
- `update_profile(profile_id, profile_data)` → bool
- `delete_profile(profile_id)` → bool

**Storage:** `data/profiles.json`

**No dependencies on:** GUI, Tkinter, or any UI framework

### LogManager (core/logs.py)
**Purpose:** Manage medication administration logs

**Key Methods:**
- `get_log(profile_id, month_year)` → Dict
- `create_log(profile_id, month_year, medication_info)` → Dict
- `add_entry(profile_id, month_year, entry_data)` → None
- `delete_entry(profile_id, month_year, day, admin_index)` → None
- `list_logs_for_profile(profile_id)` → List[str]

**Storage:** `data/logs/{profile_id}_{month_year}.json`

**No dependencies on:** GUI, Tkinter, or any UI framework

### MedicationCardManager (core/medication_cards.py)
**Purpose:** Manage medication card data for patients

**Key Methods:**
- `get_card(profile_id, medicine_name)` → Dict
- `create_card(profile_id, medicine_name, card_data)` → Dict
- `update_card(profile_id, medicine_name, card_data)` → Dict
- `delete_card(profile_id, medicine_name)` → bool
- `list_cards_for_profile(profile_id)` → List[str]

**Storage:** `data/patients/{profile_id}/medication_cards/{medicine_name}.json`

**No dependencies on:** GUI, Tkinter, or any UI framework

### ExportManager (core/export.py)
**Purpose:** Generate Word/PDF/Excel documents

**Key Methods:**
- `export_to_word(profile_data, log_data, output_path)` → str
- `export_to_pdf(word_path, pdf_path)` → str
- `export_to_excel(profile_data, log_data, output_path)` → str
- `export_log(profile_data, log_data, output_dir, ...)` → Dict

**Dependencies:** python-docx, docx2pdf (optional), openpyxl

**No dependencies on:** GUI, Tkinter, or any UI framework

## GUI Module (Interface-Specific)

### MedicationTrackerApp (gui/tkinter_app.py)
**Purpose:** Provide Tkinter-based user interface

**Responsibilities:**
- Display data from core modules
- Capture user input
- Pass data to core modules
- Handle UI events and interactions

**Dependencies:**
- tkinter (UI framework)
- core modules (ProfileManager, LogManager, MedicationCardManager, ExportManager)

**Does NOT:**
- Contain business logic
- Directly manipulate JSON files
- Perform calculations or data validation (delegates to core)

## Data Flow Examples

### Creating a Profile
```
User Input (GUI) 
  → tkinter_app.save_profile() 
    → ProfileManager.create_profile(data) 
      → Save to data/profiles.json
```

### Adding an Entry
```
User Input (GUI)
  → tkinter_app.add_administration_entry()
    → LogManager.add_entry(profile_id, month_year, entry_data)
      → Load log from JSON
      → Append entry
      → Sort by day
      → Save to data/logs/*.json
```

### Exporting
```
User Action (GUI)
  → tkinter_app.export_current_log()
    → Get profile from ProfileManager
    → Get log from LogManager
    → ExportManager.export_log(profile, log, output_dir, formats)
      → If Word: Fill Word template → Save .docx
      → If PDF: Convert .docx → Save .pdf
      → If Excel: Generate spreadsheet → Save .xlsx
```

## Swapping the GUI

### Current: Tkinter Desktop App
```python
# main.py
from gui.tkinter_app import MedicationTrackerApp
import tkinter as tk

root = tk.Tk()
app = MedicationTrackerApp(root)
root.mainloop()
```

### Future: Web Application (Flask)
```python
# web_main.py
from flask import Flask, render_template, request, jsonify
from core.profiles import ProfileManager
from core.logs import LogManager
from core.medication_cards import MedicationCardManager
from core.export import ExportManager

app = Flask(__name__)
pm = ProfileManager()
lm = LogManager()
mcm = MedicationCardManager()
em = ExportManager()

@app.route('/api/profiles')
def get_profiles():
    return jsonify(pm.get_all_profiles())

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    data = request.json
    profile_id = pm.create_profile(data)
    return jsonify({'profile_id': profile_id})

# ... more routes using same core logic
```

### Future: Mobile API (FastAPI)
```python
# mobile_api.py
from fastapi import FastAPI
from core.profiles import ProfileManager
from core.logs import LogManager
from core.medication_cards import MedicationCardManager

app = FastAPI()
pm = ProfileManager()
lm = LogManager()
mcm = MedicationCardManager()

@app.get("/profiles")
def get_profiles():
    return pm.get_all_profiles()

@app.post("/profiles")
def create_profile(profile_data: dict):
    profile_id = pm.create_profile(profile_data)
    return {"profile_id": profile_id}

# ... more endpoints using same core logic
```

### Future: Command Line Interface
```python
# cli.py
import sys
from core.profiles import ProfileManager
from core.logs import LogManager
from core.medication_cards import MedicationCardManager

pm = ProfileManager()
lm = LogManager()
mcm = MedicationCardManager()

def main():
    command = sys.argv[1]

    if command == "list-profiles":
        profiles = pm.get_all_profiles()
        for pid, data in profiles.items():
            print(f"{pid}: {data['child_name']}")

    elif command == "create-profile":
        # Get data from command line args
        # ...
        pm.create_profile(data)

    # ... more commands using same core logic
```

## Key Principles

1. **GUI never directly accesses data files**
   - Always go through ProfileManager or LogManager
   - This ensures data consistency and validation

2. **Core modules never import GUI modules**
   - ProfileManager doesn't know about Tkinter
   - LogManager doesn't know about buttons or windows
   - Can test core logic independently

3. **Single Responsibility**
   - ProfileManager: Only profiles
   - LogManager: Only logs
   - MedicationCardManager: Only medication cards
   - ExportManager: Only document generation
   - GUI: Only user interface

4. **Dependency Direction**
   ```
   GUI → Core → Data
   ```
   Never: Data → Core or Core → GUI

## Testing Strategy

### Unit Tests (Core Modules)
```python
# test_profiles.py
from core.profiles import ProfileManager

def test_create_profile():
    pm = ProfileManager("test_data")
    data = {"child_name": "Test", "foster_home": "Test Home"}
    profile_id = pm.create_profile(data)
    assert pm.profile_exists(profile_id)
```

### Integration Tests (Full Flow)
```python
# test_integration.py
from core.profiles import ProfileManager
from core.logs import LogManager
from core.medication_cards import MedicationCardManager

def test_full_workflow():
    pm = ProfileManager("test_data")
    lm = LogManager("test_data/patients")
    mcm = MedicationCardManager("test_data/patients")

    # Create profile
    pid = pm.create_profile({"child_name": "Test", ...})

    # Create medication card
    mcm.create_card(pid, "Aspirin", {...})

    # Create log
    lm.create_log(pid, "January 2025", {...})

    # Add entry
    lm.add_entry(pid, "January 2025", {...})

    # Verify
    log = lm.get_log(pid, "January 2025")
    assert len(log['administration_log']) == 1
```

### GUI Tests (Manual or with Testing Framework)
```python
# test_gui.py (requires GUI testing framework)
# Manual testing recommended for Tkinter apps
```

## Migration Paths

### Phase 1: Current (Desktop Only)
- Tkinter GUI
- Local JSON storage
- Single computer use

### Phase 2: Local Network
- Keep Tkinter GUI
- Add optional web interface
- SQLite instead of JSON
- Multiple computers on same network

### Phase 3: Cloud/Mobile
- Full web application
- Mobile app (using same API)
- Cloud database (encrypted)
- Authentication and authorization

**At each phase, core modules remain unchanged!**

## Performance Considerations

### Current Scale
- Up to ~100 patients: No issues with JSON
- Up to ~1000 logs: File system handles well
- Export: Fast enough for individual documents

### Future Scale (if needed)
- 100+ patients → Consider SQLite
- 10,000+ logs → Definitely use database
- Batch export → Add queue system
- Multi-user → Add proper concurrency handling

## Security Evolution

### Current (Single Computer)
- File system permissions
- Physical access control
- Regular backups to external drive

### Future (Network Access)
- Add user authentication
- Role-based permissions
- Audit logging
- Data encryption at rest
- HTTPS for data in transit

### Future (HIPAA Compliance)
- Encrypted database
- Detailed audit trails
- Access controls
- Data retention policies
- Secure backup procedures

## Conclusion

This architecture enables:
- ✅ Easy GUI replacement
- ✅ Independent testing
- ✅ Future scalability
- ✅ Multiple interface types
- ✅ Code reusability

The key is: **Business logic lives in core/, UI lives in gui/, and they communicate through well-defined interfaces.**

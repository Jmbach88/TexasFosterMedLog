# Complete Setup and Usage Guide

## 📦 What You Have

A complete desktop application for tracking medication administration with:
- ✅ Patient profile management
- ✅ Daily medication logging (up to 3 doses/day)
- ✅ JSON data editor
- ✅ Word/PDF export
- ✅ Sample data included
- ✅ Modular architecture (easy to modify/extend)

## 🚀 Installation

### Step 1: Install Python (if needed)

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ CHECK "Add Python to PATH"
4. Click Install

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt install python3 python3-pip
```

### Step 2: Install Requirements

Open terminal/command prompt in the `medication_tracker` folder:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-docx
pip install docx2pdf  # Optional, Windows only
```

### Step 3: Run the Application

```bash
python main.py
```

The application window should open!

## 📚 Quick Tour

### The Application Has 3 Tabs:

**1. Profiles Tab**
- Manage patient information
- Store once, reuse for all logs
- Fields: Name, Foster Home, Allergies, Prescriber, Pharmacy

**2. Medication Logs Tab**
- Create monthly medication logs
- Add daily administration entries
- Track time, caregiver initials, amount remaining
- Up to 3 administrations per day

**3. JSON Editor Tab**
- View raw data
- Make bulk edits
- Copy/paste between logs
- Advanced troubleshooting

## 🎯 Your First Log (Step by Step)

### 1️⃣ Create a Patient Profile

1. Open application → **Profiles** tab
2. Click **New Profile**
3. Fill in:
   - Child's Name: "Sarah Miller"
   - Foster Home: "Jones Family Home"
   - Allergies: "None known"
   - (Optional) Prescriber/Pharmacy info
4. Click **Save Profile**

### 2️⃣ Create a Medication Log

1. Go to **Medication Logs** tab
2. Select "Sarah Miller" from patient dropdown
3. Click **New Log**
4. Enter:
   - Month and Year: "January 2025"
   - Medicine Name: "Ibuprofen"
   - Strength: "200mg"
   - Dosage: "1 tablet"
5. Click **Create**

### 3️⃣ Add Daily Entries

For each medication dose:

1. Day: `1` (for January 1st)
2. Time: `8:00 AM`
3. Initials: `JJ` (caregiver initials)
4. Amount Remaining: `30 doses`
5. Click **Add Entry**

Repeat for each dose:
- Morning dose (8:00 AM)
- Afternoon dose (2:00 PM) - if applicable
- Evening dose (8:00 PM) - if applicable

### 4️⃣ Export to PDF

1. Go to **File → Export Current Log**
2. Choose where to save
3. Get both `.docx` and `.pdf` files!

## 📂 File Structure Explained

```
medication_tracker/
├── main.py                    ← Run this to start!
├── requirements.txt           ← Python packages needed
│
├── core/                      ← Business logic (no GUI)
│   ├── profiles.py           ← Profile management
│   ├── logs.py               ← Log management  
│   └── export.py             ← Word/PDF generation
│
├── gui/                       ← User interface
│   └── tkinter_app.py        ← Desktop app (swappable!)
│
├── data/                      ← Your data (auto-created)
│   ├── profiles.json         ← All patient profiles
│   └── logs/                 ← Individual log files
│       └── *.json
│
└── templates/
    └── med_log_template.docx  ← Form template
```

## 💾 Understanding Your Data

### Profiles (data/profiles.json)
One file contains all patient profiles:
```json
{
  "sarah_miller": {
    "child_name": "Sarah Miller",
    "foster_home": "Jones Family Home",
    ...
  }
}
```

### Logs (data/logs/)
Each patient/month gets its own file:
- `sarah_miller_january_2025.json`
- `sarah_miller_february_2025.json`
- `john_doe_january_2025.json`

## 🔄 Daily Workflow

**Morning Routine:**
1. Open application
2. Select patient and current month
3. Add today's morning dose
4. Close application (auto-saves)

**Throughout the Day:**
- Open app → Add dose → Close

**End of Month:**
1. Review entries
2. Export to PDF
3. Save/print for records
4. Start new month's log

## 🛠️ Common Tasks

### View Past Month's Log
1. Medication Logs tab
2. Select patient
3. Select month from dropdown
4. View/edit entries

### Edit Past Entry
1. Load the log
2. JSON Editor tab → Load Current Log
3. Edit the JSON directly
4. Save Changes

### Backup Your Data
Copy entire `data/` folder to:
- USB drive
- Cloud storage (Dropbox, Google Drive)
- External hard drive

### Restore From Backup
Copy `data/` folder back to application directory

### Delete Old Logs
1. Load the log
2. Click "Delete Log"
3. Confirm deletion

## 🎨 Customization

### Change the Template
Replace `templates/med_log_template.docx` with your own template.

Keep placeholder names like:
- `{{ChildName}}`
- `{{MedicineName}}`
- etc.

### Add More Profile Fields
Edit `core/profiles.py` and `gui/tkinter_app.py` to add new fields.

### Change Storage Location
Modify paths in `main.py`:
```python
ProfileManager("/path/to/data")
LogManager("/path/to/logs")
```

## 🔒 Privacy & Security

**Current Setup (Local Only):**
- ✅ Data stays on your computer
- ✅ No internet connection needed
- ✅ Privacy through physical access control
- ✅ Easy to backup

**Backup Strategy:**
1. Weekly: Copy `data/` to USB drive
2. Monthly: Copy to cloud storage (encrypted)
3. Before major changes: Make backup copy

## 🚨 Troubleshooting

### Application Won't Start
```bash
# Check Python installation
python --version

# Reinstall requirements
pip install --force-reinstall python-docx
```

### "ModuleNotFoundError"
```bash
pip install python-docx
```

### PDF Export Fails
- The `.docx` file is still created
- Open it manually
- File → Save As → PDF

### Can't Find My Data
- Check `data/profiles.json`
- Check `data/logs/` folder
- Use JSON Editor tab to view

### Changes Not Saving
- Check file permissions on `data/` folder
- Ensure sufficient disk space
- Close and reopen application

### Want Fresh Start
1. Close application
2. Delete or rename `data/` folder
3. Restart application (creates new empty data)

## 📱 Future Enhancements (Optional)

The modular architecture allows easy upgrades:

**Phase 2: Network Access**
- Add web interface
- Access from tablets/phones
- Multiple computers share data

**Phase 3: Mobile App**
- Native iOS/Android app
- Same data, different interface
- Core logic unchanged!

See `ARCHITECTURE.md` for technical details.

## 📞 Getting Help

1. **Read the docs:**
   - `QUICKSTART.md` - Quick reference
   - `README.md` - Detailed guide
   - `ARCHITECTURE.md` - Technical details

2. **Check sample data:**
   - `data/profiles.json` - Example profile
   - `data/logs/emma_johnson_december_2024.json` - Example log
   - `sample_export.docx` - Example output

3. **Experiment safely:**
   - Make a backup of `data/` folder
   - Try things out
   - Restore if needed

## ✅ You're Ready!

You now have:
- ✅ Working medication tracker
- ✅ Sample data to learn from
- ✅ Complete documentation
- ✅ Modular, extensible design

Start by exploring the sample data, then create your first profile and log!

**Next Steps:**
1. Run `python main.py`
2. Explore the sample data (Emma Johnson)
3. Create your first real profile
4. Add some test entries
5. Export to see the result
6. Start using it daily!

Good luck! 🎉

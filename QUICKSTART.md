# Quick Start Guide

## Installation (First Time Setup)

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - Version 3.7 or higher required

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install python-docx
   pip install docx2pdf  # Optional, Windows only
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## First Use Workflow

### Step 1: Create a Patient Profile
1. Open the application
2. Go to **Profiles** tab
3. Click **New Profile**
4. Fill in:
   - Child's Name (required)
   - Foster Home (required)
   - Allergies/contraindications
   - Prescriber information
   - Pharmacy information
5. Click **Save Profile**

### Step 2: Create a Medication Log
1. Go to **Medication Logs** tab
2. Select patient from dropdown
3. Click **New Log**
4. Enter:
   - Month and Year (e.g., "December 2024")
   - Medicine Name
   - Strength
   - Dosage
5. Click **Create**

### Step 3: Add Daily Entries
1. Make sure your log is loaded
2. For each medication administration:
   - Enter Day (1-31)
   - Enter Time (e.g., "8:00 AM")
   - Enter Caregiver Initials
   - Enter Amount Remaining
   - Click **Add Entry**
3. Repeat for each dose (up to 3 per day)

### Step 4: Export to PDF
1. Make sure your log is loaded
2. Go to **File → Export Current Log**
3. Select where to save
4. Get both .docx and .pdf files

## Tips

- **Profile reuse**: Create profile once, use for multiple months
- **Editing**: Use JSON Editor tab for bulk changes
- **Backup**: Copy the entire `data/` folder regularly
- **Multiple computers**: Copy `data/` folder to sync between computers

## Common Tasks

### Add a New Patient
Profiles tab → New Profile → Fill info → Save

### Start a New Month
Medication Logs tab → Select patient → New Log → Enter details

### View Past Logs
Medication Logs tab → Select patient → Select month from dropdown

### Edit Past Entry
1. Load the log
2. Switch to JSON Editor tab
3. Click "Load Current Log"
4. Edit the JSON
5. Click "Save Changes"

### Delete a Day's Entries
1. Load the log
2. Enter the day number in "Day" field
3. Click "Clear All for Day"

### Generate Monthly Report
File → Export Current Log → Choose location

## Keyboard Shortcuts

- Tab: Move between fields
- Enter: Activate focused button (in most dialogs)
- Ctrl+Tab: Switch between tabs (Windows/Linux)
- Cmd+Tab: Switch between tabs (Mac)

## Troubleshooting

**"Module not found" error:**
```bash
pip install python-docx
```

**PDF not generating:**
- The .docx file is still created
- Open it and use File → Save As → PDF

**Can't find my data:**
- Check `data/profiles.json` for profiles
- Check `data/logs/` folder for individual logs

**Want to start fresh:**
- Delete the `data/` folder
- Restart the application

## Next Steps

1. Create profiles for all patients
2. Create logs as needed
3. Add entries daily
4. Export monthly for records
5. Backup `data/` folder regularly

## Getting Help

- Check README.md for detailed documentation
- Look at the example data in `data/` folder
- Examine JSON files to understand the structure

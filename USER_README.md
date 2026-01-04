# Medication Logger - User Guide

## Welcome

Thank you for using Medication Logger! This application helps foster homes track and manage medication administration for children in care.

## Installation

### First-Time Setup

1. **Download** the application zip file
2. **Extract** the zip file to a location on your computer (e.g., `C:\Program Files\MedicationLogger\`)
3. **Run** `MedicationLogger.exe` from the extracted folder

That's it! No installation wizard needed.

### System Requirements

- **Operating System:** Windows 7 or later
- **Disk Space:** ~100 MB for application, plus space for your data
- **Display:** 1024x768 or higher resolution recommended

## First Run

When you run the application for the first time:

1. The application will create a folder for your data:
   - **Location:** `C:\Users\<YourName>\MedicationLogger\`

2. This folder will contain:
   - `data/` - All patient profiles and medication logs
   - `logs/` - Application log files (for troubleshooting)

3. If you had previous data in the old location, it will be automatically migrated to the new location

## Your Data

### Where is my data stored?

All your data is stored locally on your computer in:
```
C:\Users\<YourName>\MedicationLogger\data\
```

This folder contains:
- **profiles.json** - Patient profiles
- **patients/** - Individual patient folders with:
  - Medication logs
  - Medication cards
  - Medication images

### Backing Up Your Data

**IMPORTANT:** Regularly back up your data!

To back up:
1. Close the Medication Logger application
2. Copy the entire `MedicationLogger` folder from your user directory
3. Save it to:
   - External hard drive
   - USB flash drive
   - Cloud storage (Dropbox, OneDrive, etc.)
   - Network drive

**Recommended:** Back up weekly or after making significant changes.

### Restoring from Backup

To restore your data:
1. Close the Medication Logger application
2. Delete or rename the current `MedicationLogger` folder in your user directory
3. Copy your backup `MedicationLogger` folder to your user directory
4. Restart the application

## Features

### Patient Profiles
- Add patient information (name, foster home, allergies, etc.)
- Track prescriber and pharmacy contact information
- Edit and delete profiles as needed

### Medication Cards
- Create reusable medication information templates
- Include medication images for easy identification
- Track dosage, strength, and prescribing information

### Medication Logs
- Record daily medication administration
- Track time, initials, and amount remaining
- Monthly logs for each medication

### Export Options
The application can export logs to:
- **Word (.docx)** - Editable documents
- **PDF (.pdf)** - Print-ready reports
- **Excel (.xlsx)** - Spreadsheets for further analysis

## Troubleshooting

### Application won't start
1. Make sure you've extracted the zip file (don't run from inside the zip)
2. Check that you have permission to run programs on this computer
3. Try running as administrator (right-click → Run as administrator)

### Can't see my old data
The application automatically migrates data from old locations on first run. If your data is missing:
1. Check `C:\Users\<YourName>\MedicationLogger\logs\` for error messages
2. Look for your old data in the application's original location
3. You can manually copy data to the new location

### Export features not working

**Word export:** Should always work

**PDF export:** May not work on all systems. If it fails, you can:
- Export to Word format instead
- Open the Word file and use "Save As PDF" from Microsoft Word

**Excel export:** Should always work

### Application errors or crashes
1. Check the log files in `C:\Users\<YourName>\MedicationLogger\logs\`
2. Look for the most recent log file (named with today's date)
3. Send the log file to your IT support person

## Updates

When a new version is released:
1. Download the new version zip file
2. Extract it to replace your old application folder
3. Your data will remain safe in your user directory
4. Run the new version - it will use your existing data

## Data Privacy and Security

- All data is stored locally on your computer
- No data is sent to the internet
- No account or registration required
- You control all backups and data storage

## Getting Help

### Application Logs
Detailed logs are stored in:
```
C:\Users\<YourName>\MedicationLogger\logs\
```

These logs can help diagnose problems. Share them with IT support if you need help.

### Common Questions

**Q: Can I install this on multiple computers?**
A: Yes! Each computer will have its own data folder. To share data between computers, you'll need to manually copy the data folder or use shared network storage.

**Q: Can multiple users share the same data?**
A: If multiple Windows users share the same computer, each will have their own separate data. For shared data, all users should use the same Windows account, or data should be stored on a network location.

**Q: How do I move to a new computer?**
A:
1. Back up your data from the old computer (copy the MedicationLogger folder)
2. Install the application on the new computer
3. Copy your backup to `C:\Users\<YourName>\MedicationLogger\` on the new computer

**Q: Is this HIPAA compliant?**
A: The application stores data locally and doesn't transmit data. For HIPAA compliance, you must:
- Use appropriate physical security for the computer
- Use encrypted backups
- Follow your organization's data handling policies

## Best Practices

1. **Daily backups** if you make changes daily
2. **Weekly backups** for regular use
3. **Keep backups in multiple locations**
4. **Test your backups** periodically by restoring to a test location
5. **Document your backup procedure** for other staff members

## Contact

For technical support, contact your IT administrator or the person who provided this application.

---

**Version:** See "Help → About" in the application
**Last Updated:** 2026-01-01

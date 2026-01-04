# Build Instructions for Medication Logger

## Overview

This document describes how to build a standalone executable version of the Medication Logger application for distribution to foster homes.

## Prerequisites

### Required Software
- Python 3.8 or higher
- pip (Python package installer)

### Required Python Packages
```bash
pip install pyinstaller
pip install python-docx
pip install openpyxl
pip install Pillow
pip install docx2pdf  # Optional, for PDF export on Windows
```

Or install all at once:
```bash
pip install -r requirements.txt
```

## Build Process

### Quick Build
The easiest way to build is using the automated build script:

```bash
python build.py
```

This will:
1. Clean old build files
2. Increment the build number automatically
3. Run PyInstaller
4. Create a distribution zip file
5. Display a build summary

### Build Options

**Build without incrementing version:**
```bash
python build.py --no-increment
```

**Clean build directories only:**
```bash
python build.py --clean-only
```

**Build without creating zip file:**
```bash
python build.py --no-zip
```

### Manual Build
If you need to build manually:

```bash
# Clean old builds
rmdir /s build dist

# Run PyInstaller
pyinstaller --clean medication_logger.spec
```

## Build Output

After building, you'll find:

```
dist/
├── MedicationLogger/           # Executable and dependencies
│   ├── MedicationLogger.exe    # Main executable (Windows)
│   ├── templates/              # Bundled Word template
│   └── [various DLL files]
└── MedicationLogger-v1.0.0-buildX-platform.zip  # Distribution package
```

## Version Management

Version information is stored in `config.py`:
- `APP_VERSION`: Semantic version (e.g., "1.0.0")
- `BUILD_NUMBER`: Auto-incremented build number
- `BUILD_DATE`: Date of last build

To manually update the version:
1. Edit `config.py`
2. Change `APP_VERSION` to new version number
3. Optionally reset `BUILD_NUMBER` to 1

## Testing the Build

### Development Testing
Before building, always test in development mode:

```bash
python main.py
```

Verify:
- Application launches without errors
- All features work correctly
- Data is saved and loaded properly
- Export functions work (Word, PDF, Excel)

### Executable Testing
After building, test the executable:

1. Navigate to `dist/MedicationLogger/`
2. Run `MedicationLogger.exe`
3. Test all functionality:
   - Create a test profile
   - Create a medication card
   - Create a medication log
   - Add entries to the log
   - Export to Word/PDF/Excel
4. Check user data location:
   - Windows: `C:\Users\<username>\MedicationLogger\`
   - Data should persist between runs
5. Check log files:
   - `C:\Users\<username>\MedicationLogger\logs\`

## Distribution

### Packaging for Distribution

The build script automatically creates a zip file. To distribute:

1. Upload the zip file to your distribution location
2. Include `USER_README.md` (or create installation instructions)
3. Optionally include the User Guide

### What Gets Bundled
✅ Included in bundle:
- Python runtime
- All required libraries (tkinter, docx, openpyxl, etc.)
- Word template file
- Application code

❌ NOT included in bundle:
- User data (profiles, logs, etc.)
- Application logs
- User settings

User data is stored separately in the user's home directory.

## Troubleshooting Build Issues

### ImportError during build
**Problem:** Module not found during PyInstaller build

**Solution:** Add the module to `hiddenimports` in `medication_logger.spec`

### Missing files in bundle
**Problem:** Template or resource file not found in executable

**Solution:** Add to `datas` section in `medication_logger.spec`:
```python
datas=[
    ('templates/med_log_template.docx', 'templates'),
    # Add more files here
],
```

### Large bundle size
**Problem:** Executable is too large

**Solution:** Add unnecessary modules to `excludes` in `medication_logger.spec`

### PDF export not working
**Problem:** docx2pdf fails in bundled version

**Solution:** This is expected on non-Windows platforms. PDF export is optional and gracefully degrades.

## Platform-Specific Notes

### Windows
- PyInstaller creates a single folder distribution
- No console window appears (windowed mode)
- PDF export works with docx2pdf

### macOS/Linux
- Similar process, but may need to adjust paths
- PDF export may not work (docx2pdf is Windows-only)
- Users can still export Word and Excel formats

## Architecture Notes

The application is designed with separation of concerns:

- **GUI Layer** (`gui/tkinter_app.py`): User interface only
- **Business Logic** (`core/`): All data management
- **ResourceManager** (`core/resource_manager.py`): Handles paths for both development and bundled environments

This means:
- Business logic never depends on GUI
- Easy to test core functionality independently
- Future GUI replacements are possible (web, mobile, etc.)

## Continuous Integration

For automated builds, you can integrate the build script into CI/CD:

```bash
# Example GitHub Actions / CI script
python -m pip install -r requirements.txt
python build.py --no-increment  # Don't auto-increment in CI
```

## Need Help?

- Check PyInstaller documentation: https://pyinstaller.org/
- Review `medication_logger.spec` for build configuration
- Test in development mode first with `python main.py`
- Check application logs in `~/MedicationLogger/logs/`

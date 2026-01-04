# Project Overview - Medication Logger

## Project Summary

**Medication Logger** is a desktop application designed to help foster care providers track medication administration for children in their care. The application provides an intuitive interface for managing patient profiles, creating medication logs, and generating professional reports.

## Project Goals

### Primary Objectives
1. **Simplify Record Keeping** - Make it easy to track daily medication administration
2. **Ensure Accuracy** - Reduce errors through structured data entry
3. **Professional Reporting** - Generate documents suitable for regulatory review
4. **Easy Distribution** - Package as standalone executables requiring no technical setup
5. **Data Privacy** - Keep all data local on the user's computer

### Target Users
- Foster care providers
- Group homes
- Residential treatment facilities
- Anyone responsible for tracking medication administration for multiple individuals

## Technology Stack

### Core Technologies
- **Language:** Python 3.8+
- **GUI Framework:** Tkinter (included with Python)
- **Data Storage:** JSON files (local filesystem)
- **Packaging:** PyInstaller (for standalone executables)

### Key Libraries
- **python-docx** - Word document generation
- **openpyxl** - Excel export functionality
- **Pillow (PIL)** - Image handling and validation for medication cards
- **pillow-heif** - HEIC/HEIF support for iPhone images
- **docx2pdf** - PDF conversion (Windows only, optional)

### Development Tools
- Git for version control
- PyInstaller for building executables
- Virtual environments for dependency isolation

## Architecture Overview

### Design Philosophy

The application follows a **modular architecture** with strict **separation of concerns**:

```
┌──────────────────────────────────────────┐
│  Presentation Layer (GUI)                │
│  - Tkinter-based user interface          │
│  - No business logic                     │
│  - Could be swapped for web/mobile UI    │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│  Business Logic Layer (Core Modules)     │
│  - ProfileManager: Patient data          │
│  - LogManager: Medication logs           │
│  - MedicationCardManager: Med templates  │
│  - ExportManager: Document generation    │
│  - ResourceManager: Path management      │
│  - SettingsManager: User preferences     │
│  - No GUI dependencies                   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│  Data Layer (Storage)                    │
│  - JSON files on local filesystem        │
│  - User data directory: ~/MedicationLogger/ │
└──────────────────────────────────────────┘
```

### Why This Architecture?

**1. Testability**
- Core modules can be tested independently of the GUI
- Business logic is isolated and predictable

**2. Maintainability**
- Clear separation makes the codebase easy to navigate
- Changes to GUI don't affect core logic and vice versa

**3. Flexibility**
- GUI can be replaced (e.g., web interface, mobile app)
- Core modules remain unchanged
- Could add API layer for multi-user scenarios

**4. Development/Production Parity**
- ResourceManager handles paths for both modes
- Same code runs in development and bundled executable
- No environment-specific code needed

## Key Features

### 1. Patient Management
- Create, update, and delete patient profiles
- Store demographic and medical information
- Track prescriber and pharmacy contacts
- Search and filter capabilities

### 2. Medication Cards
- Reusable medication templates
- **Mobile-ready image support** - iPhone (HEIC), Android (WebP), and standard formats
- **Automatic image validation** - Format, size (10MB max), and dimension (4000×4000) checks
- Track dosing instructions and PRN reasons
- Linked to medication logs

### 3. Medication Logs
- Monthly logs per patient/medication
- Track date, time, initials, amount remaining
- Multiple doses per day (up to 3)
- **Dual view modes** - Calendar view with visual indicators or detailed list view
- Click calendar days to quickly add entries
- Edit and delete entries
- **Memory optimized** - No memory leaks from event handlers

### 4. Export & Reporting
- **Word Documents** - Professional, editable reports (no Word installation required)
- **PDF Files** - Print-ready documents (Windows only, requires activated Microsoft Word)
- **Excel Spreadsheets** - Data for analysis (no Excel installation required)
- **Template validation** - Automatic verification before export
- **Auto-open after export** - Checkbox to automatically open folder after successful export
- Batch export multiple logs
- Customizable export options
- Default export folder configuration

### 5. Data Management & Reliability
- **Atomic file writes** - Prevents data corruption during saves (write to temp, then atomic rename)
- **Error recovery** - Graceful handling of initialization and runtime errors
- **UTF-8 encoding** - Proper handling of international characters
- Automatic data migration from old versions
- User data in home directory (not with application)
- **Quick access button** - "Open Folder" to view data location
- Comprehensive logging for troubleshooting
- Simple backup (copy one folder)

### 6. Settings & Preferences
- **Settings tab** - Dedicated UI for application configuration
- **Default export folder** - Set preferred location for exported files
- **View data location** - Display current data storage path
- **Persistent settings** - Preferences saved across sessions in JSON format

## File Structure

```
medication_tracker/
│
├── main.py                         # Application entry point
├── config.py                       # Version and configuration
├── build.py                        # Build automation script
├── medication_logger.spec          # PyInstaller configuration
├── requirements.txt                # Python dependencies
│
├── core/                           # Business logic modules
│   ├── __init__.py
│   ├── profiles.py                 # Patient profile management
│   ├── logs.py                     # Medication log management
│   ├── medication_cards.py         # Medication card templates
│   ├── export.py                   # Document generation
│   ├── resource_manager.py         # Path management
│   ├── settings_manager.py         # User preferences & settings
│   ├── data_migration.py           # First-run data migration
│   └── logging_config.py           # Application logging setup
│
├── gui/                            # User interface
│   ├── __init__.py
│   └── tkinter_app.py              # Tkinter GUI implementation
│
├── templates/                      # Document templates
│   └── med_log_template.docx       # Word template for exports
│
├── data/                           # Development data (gitignored)
│   ├── profiles.json
│   └── patients/
│
└── docs/                           # Documentation
    ├── README.md                   # Main readme
    ├── INSTALLATION.md             # Installation guide
    ├── BUILD_INSTRUCTIONS.md       # Build guide
    ├── USER_README.md              # End-user guide
    ├── ARCHITECTURE.md             # Architecture details
    └── PROJECT_OVERVIEW.md         # This file
```

## Data Flow Examples

### Creating a Profile

```
User clicks "New Profile"
    ↓
GUI captures form data
    ↓
tkinter_app calls ProfileManager.create_profile(data)
    ↓
ProfileManager generates ID, adds timestamps
    ↓
ProfileManager saves to profiles.json
    ↓
GUI refreshes profile list
```

### Adding a Log Entry

```
User fills entry form (day, time, initials, amount)
    ↓
GUI validates input
    ↓
tkinter_app calls LogManager.add_entry(profile_id, med_name, month_year, entry_data)
    ↓
LogManager loads log from JSON
    ↓
LogManager appends entry, sorts by day
    ↓
LogManager saves updated log
    ↓
GUI refreshes entry list
```

### Exporting to Word/PDF/Excel

```
User selects "Export" and chooses formats
    ↓
GUI collects profile data from ProfileManager
    ↓
GUI collects log data from LogManager
    ↓
tkinter_app calls ExportManager.export_log(profile, log, output_dir, formats)
    ↓
ExportManager generates Word document from template
    ↓
ExportManager converts to PDF (if requested)
    ↓
ExportManager generates Excel spreadsheet (if requested)
    ↓
Files saved to user-selected directory
    ↓
GUI shows success message
```

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/Jmbach88/TexasFosterMedLog.git
cd medication-logger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Making Changes

1. **Branch:** Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Code:** Make your changes
   - Edit core modules for business logic
   - Edit GUI modules for interface changes
   - Update documentation as needed

3. **Test:** Run the application
   ```bash
   python main.py
   ```

4. **Build:** Test as executable
   ```bash
   python build.py
   cd dist/MedicationLogger
   ./MedicationLogger.exe
   ```

5. **Commit:** Commit your changes
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push:** Push to your branch
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Pull Request:** Create a PR on GitHub

### Testing Checklist

Before submitting changes, verify:

- [ ] Application runs in development mode
- [ ] Application builds without errors
- [ ] Bundled executable runs correctly
- [ ] All features work (create profile, log, export)
- [ ] Data persists between runs
- [ ] No errors in application logs
- [ ] Documentation updated if needed

## Build and Distribution Process

### Build Process

```bash
# Automated build (recommended)
python build.py

# This does:
# 1. Cleans old build files
# 2. Increments build number
# 3. Runs PyInstaller
# 4. Creates distribution zip
# 5. Shows build summary
```

### Distribution Package

The build creates:
```
dist/
├── MedicationLogger/                    # Executable and dependencies
│   ├── MedicationLogger.exe             # Main executable
│   ├── templates/                       # Bundled template
│   └── [DLL files and libraries]
└── MedicationLogger-v1.0.0-buildX.zip   # Distribution package
```

### What Gets Bundled

**Included:**
- Python runtime
- All dependencies (tkinter, docx, openpyxl, etc.)
- Word template file
- Application code

**NOT Included (Stored Separately):**
- User data (profiles, logs, etc.)
- Application logs
- User settings

This separation ensures:
- Updates don't delete user data
- Data is easily backed up
- Multiple versions can coexist

## Roadmap

### Version 1.0 (Current - Production Ready)
- ✅ Patient profile management
- ✅ Medication log tracking with calendar view
- ✅ Medication card templates with images
- ✅ Word/PDF/Excel export
- ✅ Standalone executable packaging
- ✅ Automatic data migration
- ✅ Comprehensive logging
- ✅ **Mobile image support (HEIC/HEIF for iPhone, WebP for Android)**
- ✅ **Atomic file writes for data integrity**
- ✅ **Comprehensive error handling and recovery**
- ✅ **Memory leak prevention in calendar view**
- ✅ **Image validation (format, size, dimensions)**
- ✅ **Quick access to data folder**
- ✅ **UTF-8 encoding support**

### Version 1.1 (Planned)
- [ ] Enhanced search and filtering
- [ ] Medication interaction warnings
- [ ] Refill reminders
- [ ] Improved medication card images
- [ ] Custom export templates

### Version 2.0 (Future)
- [ ] Web interface option
- [ ] Mobile companion app
- [ ] Cloud backup integration (optional)
- [ ] Multi-user support with permissions
- [ ] Database backend option
- [ ] API for third-party integration

### Long-term Vision
- [ ] HIPAA compliance mode
- [ ] Barcode medication verification
- [ ] Electronic signature support
- [ ] Integration with pharmacy systems
- [ ] Advanced analytics and reporting

## Contributing

We welcome contributions! See [Contributing Guidelines](#) for details.

### Ways to Contribute

1. **Report Bugs** - Use GitHub Issues
2. **Suggest Features** - Open an issue with enhancement label
3. **Improve Documentation** - Fix typos, add examples
4. **Submit Code** - Fork, code, test, submit PR
5. **Test Builds** - Try pre-release versions

### Development Guidelines

- **Code Style:** Follow PEP 8
- **Separation:** Keep GUI separate from business logic
- **Comments:** Add docstrings and comments
- **Testing:** Test in both dev and bundled modes
- **Documentation:** Update docs for changes

## Support and Resources

### Documentation
- [README.md](README.md) - Main readme
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [USER_README.md](USER_README.md) - End-user documentation
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Build guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture details

### Getting Help
- **GitHub Issues** - Report bugs or request features
- **Discussions** - Ask questions
- **Documentation** - Check the docs folder

### Project Links
- **Repository:** https://github.com/Jmbach88/TexasFosterMedLog
- **Issues:** https://github.com/Jmbach88/TexasFosterMedLog/issues
- **Releases:** https://github.com/Jmbach88/TexasFosterMedLog/releases

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is built with care for foster care providers who work tirelessly to ensure the health and safety of children in their care.

---

**Project Status:** Active Development
**Current Version:** 1.0.0
**Last Updated:** 2026-01-01

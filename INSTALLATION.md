# Installation Instructions

Complete guide for installing and setting up the Medication Logger application.

## Table of Contents

- [For End Users (Non-Technical)](#for-end-users-non-technical)
- [For Developers](#for-developers)
- [System Requirements](#system-requirements)
- [Troubleshooting](#troubleshooting)

---

## For End Users (Non-Technical)

### Windows Installation

1. **Download the Application**
   - Go to the [Releases](../../releases) page
   - Download the latest `MedicationLogger-vX.X.X-buildX-win32.zip` file
   - Save it to your Downloads folder

2. **Extract the Files**
   - Right-click the downloaded ZIP file
   - Select "Extract All..."
   - Choose a destination (recommended: `C:\Program Files\MedicationLogger\`)
   - Click "Extract"

3. **Run the Application**
   - Navigate to the extracted folder
   - Double-click `MedicationLogger.exe`
   - The application will start

4. **First Run**
   - On first run, the application will create a data folder at:
     ```
     C:\Users\<YourName>\MedicationLogger\
     ```
   - If you have existing data from an older version, it will be automatically migrated

5. **Create a Shortcut (Optional)**
   - Right-click `MedicationLogger.exe`
   - Select "Create shortcut"
   - Drag the shortcut to your Desktop or Start Menu

### macOS Installation

1. **Download the Application**
   - Download the latest `.zip` file for macOS from [Releases](../../releases)

2. **Extract and Move**
   - Double-click the ZIP file to extract
   - Drag `MedicationLogger.app` to your Applications folder

3. **First Run (Important!)**
   - Right-click the app and select "Open" (don't double-click)
   - Click "Open" when you see the security warning
   - This is only needed the first time

4. **Data Location**
   - Your data will be stored in:
     ```
     /Users/<YourName>/MedicationLogger/
     ```

### Linux Installation

1. **Download the Application**
   - Download the latest Linux release from [Releases](../../releases)

2. **Extract the Archive**
   ```bash
   unzip MedicationLogger-vX.X.X-buildX-linux.zip
   cd MedicationLogger
   ```

3. **Make Executable**
   ```bash
   chmod +x MedicationLogger
   ```

4. **Run the Application**
   ```bash
   ./MedicationLogger
   ```

5. **Data Location**
   ```
   /home/<username>/MedicationLogger/
   ```

---

## For Developers

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

**Verify Installation:**
```bash
python --version    # Should show 3.8 or higher
pip --version       # Should show pip version
git --version       # Should show git version
```

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/Jmbach88/TexasFosterMedLog.git

# Navigate to project directory
cd medication-logger
```

Alternatively, download and extract the source code ZIP from GitHub.

### Step 2: Set Up Virtual Environment (Recommended)

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This installs:
- `python-docx` - Word document generation
- `openpyxl` - Excel export functionality
- `Pillow` - Image handling and validation
- `pillow-heif` - HEIC/HEIF support for iPhone images
- `docx2pdf` - PDF conversion (Windows only)
- `pyinstaller` - For building standalone executables

**Note:** If `pillow-heif` installation fails on your platform, the app will still work but won't support HEIC images from iPhones. Users would need to convert HEIC to JPEG first.

### Step 4: Verify Installation

```bash
# Run the application
python main.py
```

The application should launch and create a data directory at `~/MedicationLogger/`.

### Step 5: Development Setup (Optional)

**Install Development Tools:**
```bash
pip install pytest          # For testing
pip install black           # For code formatting
pip install pylint          # For code linting
```

**VS Code Setup:**
If using VS Code, install these extensions:
- Python (Microsoft)
- Pylance
- Python Docstring Generator

**PyCharm Setup:**
- Open the project folder
- PyCharm will automatically detect `requirements.txt`
- Click "Install requirements" when prompted

### Development Workflow

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run the application
python main.py

# Run with logging to console
python main.py --debug  # (if implemented)

# Deactivate virtual environment when done
deactivate
```

---

## System Requirements

### Minimum Requirements

**Operating System:**
- Windows 10 or later (Windows 7/8 may work but unsupported)
- macOS 10.14 (Mojave) or later
- Linux (tested on Ubuntu 18.04+)

**Hardware:**
- CPU: 1 GHz or faster
- RAM: 512 MB (1 GB recommended)
- Storage: 100 MB for application + space for your data
- Display: 1024x768 resolution (1280x720 or higher recommended)

**For PDF Export (Optional):**
⚠️ **Microsoft Word Required**
- PDF export requires **Microsoft Word to be installed AND activated**
- Word must be properly licensed (signed into a Microsoft account)
- Word is used to convert .docx files to PDF format
- **If Word is not available:**
  - You can still export to Word (.docx) and Excel (.xlsx) formats
  - Use free online PDF converters (e.g., CloudConvert, Smallpdf)
  - All other application features work normally

**Note:** Word and Excel document creation does NOT require Microsoft Office. Only PDF conversion requires an activated Word installation.

### Recommended Requirements

**Hardware:**
- CPU: 2 GHz dual-core or better
- RAM: 2 GB or more
- Storage: 500 MB (allows for extensive logs and images)
- Display: 1920x1080 resolution

**Software (For Developers):**
- Python 3.10 or higher
- Git 2.x
- Text editor or IDE (VS Code, PyCharm, etc.)

---

## Troubleshooting

### Common Issues

#### Application Won't Start (End Users)

**Windows:**
- **Error:** "VCRUNTIME140.dll was not found"
  - **Solution:** Install Microsoft Visual C++ Redistributable
  - Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

- **Error:** "Windows protected your PC"
  - **Solution:** Click "More info" → "Run anyway"
  - The app is not signed yet; this is normal

**macOS:**
- **Error:** "App can't be opened because it is from an unidentified developer"
  - **Solution:** Right-click → Open → Click "Open" in the dialog

**Linux:**
- **Error:** "Permission denied"
  - **Solution:** Make the file executable: `chmod +x MedicationLogger`

#### Application Won't Start (Developers)

**Python not found:**
```bash
# Windows: Add Python to PATH, or use full path
C:\Python39\python.exe main.py

# macOS/Linux: Use python3
python3 main.py
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific missing module
pip install python-docx
```

**Virtual environment not activated:**
```bash
# Activate it first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Data Issues

**Can't find my data:**
- Check `~/MedicationLogger/data/`
  - Windows: `C:\Users\<YourName>\MedicationLogger\data\`
  - macOS: `/Users/<YourName>/MedicationLogger/data/`
  - Linux: `/home/<username>/MedicationLogger/data/`

**Migration failed:**
- Check application logs in `~/MedicationLogger/logs/`
- Look for the most recent log file
- Search for "ERROR" or "FAILED"

**Data from old version not showing:**
- Old data should auto-migrate on first run
- If migration failed, manually copy:
  - From: `<app_folder>/data/`
  - To: `~/MedicationLogger/data/`

#### Export Issues

**PDF export not working:**
- Windows: Install `docx2pdf`: `pip install docx2pdf`
- macOS/Linux: PDF export is currently Windows-only
- Workaround: Export to Word, then use Microsoft Word to save as PDF

**Excel export fails:**
- Install openpyxl: `pip install openpyxl`
- Check that you have write permissions to the destination folder

**Template not found:**
- Verify `templates/med_log_template.docx` exists in the application folder
- For standalone executables, the template is bundled automatically

#### Image Upload Issues

**HEIC images from iPhone not working:**
- Install pillow-heif: `pip install pillow-heif`
- On some platforms, you may need additional system libraries
- Workaround: Convert HEIC to JPEG on your phone before uploading (iOS Settings → Camera → Formats → Most Compatible)

**Image upload fails with "Unsupported format" error:**
- Supported formats: JPEG, PNG, HEIC/HEIF (iPhone), WebP (Android), GIF, BMP, TIFF
- Check that the file is not corrupted
- Maximum file size: 10 MB
- Maximum dimensions: 4000×4000 pixels

**Image file too large:**
- Resize the image before uploading
- On iPhone: Use third-party apps to compress
- On Android: Use built-in gallery editing tools

#### Development Issues

**PyInstaller build fails:**
```bash
# Clean and rebuild
python build.py --clean-only
python build.py
```

**Import errors after building:**
- Check `hiddenimports` in `medication_logger.spec`
- Add missing modules to the list

**Application works in development but not in executable:**
- Check paths - use ResourceManager for all file operations
- Test both modes: development (`python main.py`) and bundled

---

## Getting Help

### For End Users

1. **Check the User Guide:** [USER_README.md](USER_README.md)
2. **Review Application Logs:** `~/MedicationLogger/logs/`
3. **Contact Support:** Open an issue on GitHub or contact your IT support

### For Developers

1. **Documentation:** Review all `.md` files in the repository
2. **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Build Guide:** See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
4. **Issues:** Check [GitHub Issues](../../issues) for similar problems
5. **Ask for Help:** Open a new issue with:
   - Your OS and Python version
   - Steps to reproduce the problem
   - Error messages and log files
   - What you've already tried

---

## Next Steps

After installation:

1. **End Users:**
   - Read the [User Guide](USER_README.md)
   - Create your first patient profile
   - Set up regular backups

2. **Developers:**
   - Review [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
   - Explore the [Architecture](ARCHITECTURE.md)
   - Check out the [Development Workflow](#development-workflow)
   - Consider contributing!

---

**Last Updated:** 2026-01-01

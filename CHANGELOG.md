# Changelog

All notable changes to the Medication Logger project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v1.1
- **Direct PDF export** - ReportLab-based PDF generation (no Word requirement)
- Enhanced search and filtering across profiles and logs
- Medication interaction warnings
- Automated refill reminders
- Custom export templates
- Print preview functionality

---

## [1.0.0] - 2026-01-01

### Added
- **Patient profile management** - Create, edit, delete, and search patient profiles
- **Medication card templates** - Reusable medication information with image support
- **Medication logs** - Monthly administration tracking with calendar and list views
- **Dual view modes** - Toggle between calendar view and detailed list view for logs
- **Calendar interface** - Visual calendar with clickable days for quick entry
- **Word document export** - Professional, editable `.docx` reports
- **PDF export** - Print-ready documents (Windows only)
- **Excel export** - Data export to `.xlsx` spreadsheets for analysis
- **Mobile image support** - Direct upload from smartphones:
  - iPhone: HEIC/HEIF (iOS 11+), JPEG, PNG
  - Android: JPEG, WebP, PNG
  - Also supports: GIF, BMP, TIFF
- **Image validation** - Automatic checks for:
  - Supported formats
  - File size (max 10 MB)
  - Dimensions (max 4000×4000 pixels)
  - Image integrity (corruption detection)
- **Atomic file writes** - Prevents data corruption during save operations
- **Error recovery** - Graceful handling of initialization failures
- **Data location access** - "Open Folder" button to quickly view data directory
- **Automatic data migration** - Seamless upgrade from old data formats
- **UTF-8 encoding** - Support for international characters throughout
- **Comprehensive logging** - Detailed application logs for troubleshooting
- **Template validation** - Automatic verification of export templates
- **Settings tab** - Configure application preferences:
  - Default export folder location
  - View current data storage location
  - Settings persist across sessions
- **Open folder after export** - Automatic folder opening after successful export
  - Checkbox option in export dialogs (enabled by default)
  - Cross-platform support (Windows/macOS/Linux)
- **Standalone executable** - PyInstaller-based packaging for easy distribution
- **Cross-platform support** - Windows (primary), macOS, Linux (experimental)

### Changed
- **User data location** - Now stored in `~/MedicationLogger/` instead of app directory
- **Font standardization** - Unified Segoe UI font family across entire application
- **Memory optimization** - Improved calendar view performance

### Fixed
- **Memory leaks** - Calendar view event handlers now properly cleaned up
- **File handle leaks** - All file operations use proper exception handling
- **Data corruption risk** - Implemented atomic writes for all JSON operations
- **Missing error messages** - Added user-friendly error dialogs for all failure scenarios
- **Template errors** - Export validates template existence and structure before use
- **Image upload failures** - Comprehensive validation prevents corrupted images

### Security
- **Input validation** - Image files validated before processing
- **File encoding** - UTF-8 encoding prevents injection attacks
- **Error handling** - No sensitive information leaked in error messages

### Technical Details

#### Core Modules
- **profiles.py** - Atomic writes with UTF-8 encoding, proper exception handling
- **logs.py** - Atomic writes with UTF-8 encoding, proper exception handling
- **medication_cards.py** - Image validation (format, size, dimensions, integrity)
- **export.py** - Template validation before export operations
- **resource_manager.py** - Cross-platform path management for dev/production
- **settings_manager.py** - User preferences persistence with JSON storage

#### GUI
- **tkinter_app.py** - Error recovery on initialization, memory leak prevention in calendar view
- **Calendar view** - Event handler cleanup, proper unbinding of mouse events
- **Data location** - Quick access button with cross-platform folder opening
- **Settings tab** - User preferences UI with default export folder configuration
- **Export dialogs** - "Open folder after export" checkbox with automatic folder opening

#### Dependencies
- `python-docx>=0.8.11` - Word document generation (no Word installation required)
- `openpyxl>=3.0.9` - Excel export (no Excel installation required)
- `Pillow>=9.0.0` - Image handling and validation
- `pillow-heif>=0.10.0` - HEIC/HEIF support for iPhone images
- `docx2pdf>=0.1.8` - PDF conversion (Windows only, **requires activated Microsoft Word**)
- `pyinstaller>=5.0.0` - Executable packaging

#### Architecture
- **Separation of concerns** - Clean separation between GUI and business logic
- **Modular design** - Core modules independent of presentation layer
- **Resource management** - Single source of truth for all file paths
- **Development/production parity** - Works identically in both modes

---

## Version History

### Pre-1.0 Development Versions

**v0.9.0** - Beta Release
- Initial feature-complete version
- Basic profile, log, and export functionality
- JSON-based data storage
- Simple GUI with tabs

**v0.5.0** - Alpha Release
- Proof of concept
- Basic medication logging
- Manual data entry only

---

## Upgrade Notes

### Upgrading to 1.0.0

**From v0.x:**
- Data will automatically migrate to `~/MedicationLogger/` on first run
- Old data in application directory will be preserved
- No manual intervention required
- Backup recommended before upgrade (copy `data/` folder)

**New Dependencies:**
```bash
pip install pillow-heif  # For iPhone HEIC support
```

**Breaking Changes:**
- None - fully backward compatible with v0.x data formats

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development workflow

---

## Support

- **Documentation:** See the `docs/` folder
- **Issues:** [GitHub Issues](../../issues)
- **Questions:** [GitHub Discussions](../../discussions)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** Dates in this changelog use YYYY-MM-DD format (ISO 8601).

[Unreleased]: https://github.com/Jmbach88/TexasFosterMedLog/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Jmbach88/TexasFosterMedLog/releases/tag/v1.0.0

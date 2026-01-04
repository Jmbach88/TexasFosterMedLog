# Contributing to Medication Logger

Thank you for your interest in contributing to Medication Logger! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or discriminatory comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**How to Submit a Good Bug Report:**

1. **Use a clear and descriptive title**
2. **Describe the exact steps to reproduce the problem**
3. **Provide specific examples** (sample data, screenshots)
4. **Describe the behavior you observed** and what you expected
5. **Include details about your environment:**
   - OS and version
   - Python version (if running from source)
   - Application version

**Example:**
```markdown
**Bug:** Export to PDF fails on macOS

**Steps to reproduce:**
1. Create a medication log
2. Click Export → Export to PDF
3. Error appears

**Expected:** PDF file created
**Actual:** Error message "docx2pdf not available"

**Environment:**
- macOS 13.0
- Medication Logger v1.0.0
```

### Suggesting Features

We welcome feature suggestions! Before creating a feature request:

1. **Check if it aligns with project goals** (foster care medication tracking)
2. **Search existing issues** to avoid duplicates
3. **Provide clear use cases** - How would this help users?

**Template:**
```markdown
**Feature:** [Brief description]

**Problem it solves:**
[Describe the problem or need]

**Proposed solution:**
[How would this feature work?]

**Alternatives considered:**
[What other approaches did you consider?]

**Use case:**
[Real-world scenario where this would be useful]
```

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** (following our coding guidelines)
4. **Test thoroughly** (both dev and built modes)
5. **Update documentation** as needed
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to your fork** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/medication-logger.git
cd medication-logger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Development Workflow

```bash
# Create a new branch for your feature
git checkout -b feature/my-feature

# Make changes and test
python main.py

# Test the build
python build.py

# Commit changes
git add .
git commit -m "Description of changes"

# Push to your fork
git push origin feature/my-feature
```

---

## Coding Guidelines

### Python Style

- **Follow PEP 8** style guidelines
- **Use meaningful variable names** (no single letters except in loops)
- **Add docstrings** to all functions and classes
- **Keep functions focused** - one function, one purpose
- **Maximum line length:** 100 characters (not strict, but preferred)

**Example:**
```python
def calculate_total_doses(entries: List[Dict]) -> int:
    """
    Calculate total number of doses from administration entries.

    Args:
        entries: List of administration entry dictionaries

    Returns:
        Total number of doses recorded
    """
    return len(entries)
```

### Architecture Guidelines

**CRITICAL: Maintain separation of concerns**

1. **Business logic** goes in `core/` modules
   - ProfileManager, LogManager, etc.
   - NO GUI code in core modules
   - NO tkinter imports in core modules

2. **GUI code** goes in `gui/` modules
   - Only UI-related code
   - Call core modules for business logic

3. **Use ResourceManager** for all file paths
   - Never hardcode paths
   - Works in both dev and bundled modes

**Good Example:**
```python
# core/profiles.py
class ProfileManager:
    def create_profile(self, data):
        # Business logic only
        profile_id = self._generate_id(data['name'])
        # ... save logic
        return profile_id

# gui/tkinter_app.py
class MedicationTrackerApp:
    def on_create_profile_click(self):
        # Get data from UI
        data = self._get_form_data()
        # Call business logic
        profile_id = self.profile_manager.create_profile(data)
        # Update UI
        self.refresh_profile_list()
```

**Bad Example:**
```python
# core/profiles.py - DON'T DO THIS
import tkinter as tk  # ❌ No GUI imports in core!

class ProfileManager:
    def create_profile(self, data):
        messagebox.showinfo("Success", "Profile created!")  # ❌ No GUI in core!
```

### Testing Guidelines

**Before submitting a PR, test:**

1. **Development mode:** `python main.py`
2. **Built mode:** `python build.py` then run the executable
3. **All affected features** work correctly
4. **No new errors** in application logs (`~/MedicationLogger/logs/`)

### Documentation Guidelines

**Update documentation when you:**

- Add a new feature → Update README.md features list
- Change architecture → Update ARCHITECTURE.md
- Add dependencies → Update requirements.txt and INSTALLATION.md
- Fix a bug → Add entry to CHANGELOG.md (Unreleased section)

---

## Pull Request Process

### Before Submitting

- [ ] Code follows PEP 8 style guidelines
- [ ] All new functions have docstrings
- [ ] Separation of concerns maintained (GUI vs core)
- [ ] Tested in development mode
- [ ] Tested in built/bundled mode
- [ ] Documentation updated
- [ ] No unnecessary files included (e.g., `__pycache__`, `.pyc`)

### PR Template

```markdown
## Description
[Describe what this PR does]

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
[Describe how you tested this]

## Checklist
- [ ] My code follows the project's coding guidelines
- [ ] I have tested in both development and built modes
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added entries to CHANGELOG.md (Unreleased section)

## Screenshots (if applicable)
[Add screenshots here]
```

### Review Process

1. **Automated checks** (if configured) must pass
2. **Maintainer review** - We'll review your code and provide feedback
3. **Address feedback** - Make requested changes
4. **Approval** - Once approved, we'll merge your PR
5. **Thank you!** - Your contribution will be credited in the changelog

### After Your PR is Merged

- Delete your feature branch (both local and remote)
- Pull the latest changes from main
- Your contribution will appear in the next release!

---

## Commit Message Guidelines

Use clear, descriptive commit messages:

**Good:**
```
Add HEIC image support for iPhone uploads
Fix memory leak in calendar view event handlers
Update README with mobile image support documentation
```

**Bad:**
```
fixed stuff
updates
WIP
```

**Format:**
```
<type>: <short description>

[Optional longer description]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, no logic change)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## Project Structure

Understanding the project structure helps you contribute more effectively:

```
medication_tracker/
├── core/              # Business logic (NO GUI code here!)
│   ├── profiles.py
│   ├── logs.py
│   ├── medication_cards.py
│   ├── export.py
│   └── resource_manager.py
├── gui/               # GUI code only
│   └── tkinter_app.py
├── templates/         # Document templates
├── data/              # Dev data (gitignored)
└── docs/              # Documentation
```

**Key principle:** Core modules should be completely independent of the GUI. They could work with a web interface, CLI, or any other frontend.

---

## Getting Help

- **Questions?** Open a discussion on GitHub
- **Stuck?** Check existing issues or ask in discussions
- **Not sure if your idea fits?** Open an issue to discuss before coding

---

## Recognition

Contributors will be:
- Listed in CHANGELOG.md for their contributions
- Credited in release notes
- Appreciated by foster care providers who use this software!

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Medication Logger!** 🎉

Your work helps foster care providers better track medication administration and ultimately helps keep children safe and healthy.

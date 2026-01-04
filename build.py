#!/usr/bin/env python3
"""
Build Script for Medication Logger
Automates the PyInstaller build process with version management
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import re

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_current_version():
    """Read current version from config.py"""
    config_file = Path('config.py')

    with open(config_file, 'r') as f:
        content = f.read()

    # Extract version
    version_match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
    build_match = re.search(r'BUILD_NUMBER\s*=\s*(\d+)', content)

    if version_match and build_match:
        return version_match.group(1), int(build_match.group(1))

    return "1.0.0", 1


def increment_build_number():
    """Increment build number in config.py"""
    config_file = Path('config.py')

    with open(config_file, 'r') as f:
        content = f.read()

    # Get current build number
    build_match = re.search(r'BUILD_NUMBER\s*=\s*(\d+)', content)
    if build_match:
        current_build = int(build_match.group(1))
        new_build = current_build + 1

        # Replace build number
        content = re.sub(
            r'BUILD_NUMBER\s*=\s*\d+',
            f'BUILD_NUMBER = {new_build}',
            content
        )

        # Update build date
        today = datetime.now().strftime('%Y-%m-%d')
        content = re.sub(
            r'BUILD_DATE\s*=\s*["\'][^"\']*["\']',
            f'BUILD_DATE = "{today}"',
            content
        )

        # Write back
        with open(config_file, 'w') as f:
            f.write(content)

        print(f"✓ Incremented build number: {current_build} → {new_build}")
        return new_build

    return 1


def clean_build_directories():
    """Remove old build and dist directories"""
    dirs_to_clean = ['build', 'dist']

    for dirname in dirs_to_clean:
        dir_path = Path(dirname)
        if dir_path.exists():
            print(f"Cleaning {dirname}/...")
            shutil.rmtree(dir_path)

    print("✓ Build directories cleaned")


def run_pyinstaller():
    """Run PyInstaller with the spec file"""
    spec_file = 'medication_logger.spec'

    if not Path(spec_file).exists():
        print(f"✗ Error: {spec_file} not found")
        return False

    print(f"\nRunning PyInstaller...")
    print("=" * 60)

    try:
        # Use python -m PyInstaller for better compatibility on Windows
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--clean', spec_file],
            check=True,
            capture_output=False
        )

        print("=" * 60)
        print("✓ PyInstaller completed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print(f"✗ PyInstaller failed with error code {e.returncode}")
        return False
    except FileNotFoundError:
        print("✗ Error: PyInstaller not found. Install it with: pip install pyinstaller")
        return False


def create_distribution_package(version, build_number):
    """Create a distributable zip file"""
    dist_dir = Path('dist/MedicationLogger')

    if not dist_dir.exists():
        print("✗ Error: Distribution directory not found")
        return False

    # Create zip file name
    zip_name = f"MedicationLogger-v{version}-build{build_number}-{sys.platform}"
    zip_path = Path(f'dist/{zip_name}')

    print(f"\nCreating distribution package...")

    try:
        # Create zip file
        shutil.make_archive(str(zip_path), 'zip', dist_dir.parent, dist_dir.name)
        print(f"✓ Created: {zip_path}.zip")
        return True

    except Exception as e:
        print(f"✗ Error creating zip: {e}")
        return False


def print_build_summary(version, build_number):
    """Print summary of the build"""
    dist_dir = Path('dist/MedicationLogger')

    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)
    print(f"Version:        {version}")
    print(f"Build Number:   {build_number}")
    print(f"Build Date:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Platform:       {sys.platform}")
    print(f"\nOutput Directory: {dist_dir.absolute()}")

    if dist_dir.exists():
        # Calculate total size
        total_size = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"Package Size:     {size_mb:.2f} MB")

    print("=" * 60)


def main():
    """Main build process"""
    parser = argparse.ArgumentParser(description='Build Medication Logger application')
    parser.add_argument('--no-increment', action='store_true',
                       help='Do not increment build number')
    parser.add_argument('--clean-only', action='store_true',
                       help='Only clean build directories')
    parser.add_argument('--no-zip', action='store_true',
                       help='Do not create distribution zip file')

    args = parser.parse_args()

    print("=" * 60)
    print("MEDICATION LOGGER - BUILD SCRIPT")
    print("=" * 60)

    # Get current version
    version, build_number = get_current_version()
    print(f"Current Version: {version}")
    print(f"Current Build:   {build_number}")

    # Clean build directories
    clean_build_directories()

    if args.clean_only:
        print("\n✓ Clean completed")
        return 0

    # Increment build number if requested
    if not args.no_increment:
        build_number = increment_build_number()
        print(f"New Build:       {build_number}")

    # Run PyInstaller
    if not run_pyinstaller():
        print("\n✗ Build failed")
        return 1

    # Create distribution package
    if not args.no_zip:
        if not create_distribution_package(version, build_number):
            print("\n⚠ Warning: Failed to create distribution package")

    # Print summary
    print_build_summary(version, build_number)

    print("\n✓ Build completed successfully!")
    print("\nNext steps:")
    print("  1. Test the executable in dist/MedicationLogger/")
    print("  2. Distribute the application to foster homes")
    print("  3. User data will be stored in ~/MedicationLogger/")

    return 0


if __name__ == '__main__':
    sys.exit(main())

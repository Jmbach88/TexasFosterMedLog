"""
Generate Sample Data for Medication Tracker
Run this script to populate the app with test data
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.profiles import ProfileManager
from core.logs import LogManager
from core.medication_cards import MedicationCardManager


def generate_sample_data():
    """Generate sample patients, medication cards, and logs"""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    # Initialize managers
    profile_manager = ProfileManager(data_dir)
    log_manager = LogManager(os.path.join(data_dir, "patients"))
    med_card_manager = MedicationCardManager(os.path.join(data_dir, "patients"))

    print("Generating sample data...")
    print("=" * 50)

    # Sample patients
    patients = [
        {
            "child_name": "Emma Johnson",
            "foster_home": "Sunrise Foster Home",
            "allergies": "Penicillin, Peanuts",
            "prescriber_name": "Dr. Sarah Mitchell",
            "prescriber_phone": "(555) 123-4567",
            "pharmacy": "MedCare Pharmacy",
            "pharmacy_phone": "(555) 234-5678"
        },
        {
            "child_name": "Michael Chen",
            "foster_home": "Hope House",
            "allergies": "None known",
            "prescriber_name": "Dr. James Rodriguez",
            "prescriber_phone": "(555) 345-6789",
            "pharmacy": "HealthPlus Pharmacy",
            "pharmacy_phone": "(555) 456-7890"
        },
        {
            "child_name": "Sofia Martinez",
            "foster_home": "Caring Hearts Foster Care",
            "allergies": "Latex, Sulfa drugs",
            "prescriber_name": "Dr. Emily Thompson",
            "prescriber_phone": "(555) 567-8901",
            "pharmacy": "Community Pharmacy",
            "pharmacy_phone": "(555) 678-9012"
        }
    ]

    # Sample medications for each patient
    medications = {
        "emma_johnson": [
            {
                "medicine_name": "Methylphenidate",
                "strength": "10mg",
                "dosage": "1 tablet twice daily",
                "reason_prescribed": "ADHD management - helps with focus and attention in school",
                "reason_prn": ""
            },
            {
                "medicine_name": "Melatonin",
                "strength": "3mg",
                "dosage": "1 tablet at bedtime",
                "reason_prescribed": "Sleep support - helps establish healthy sleep patterns",
                "reason_prn": ""
            }
        ],
        "michael_chen": [
            {
                "medicine_name": "Fluoxetine",
                "strength": "20mg",
                "dosage": "1 capsule daily",
                "reason_prescribed": "Anxiety and depression management",
                "reason_prn": ""
            },
            {
                "medicine_name": "Ibuprofen",
                "strength": "200mg",
                "dosage": "1-2 tablets as needed",
                "reason_prescribed": "",
                "reason_prn": "Pain relief for headaches or minor injuries. Max 3 doses per day."
            }
        ],
        "sofia_martinez": [
            {
                "medicine_name": "Albuterol Inhaler",
                "strength": "90mcg",
                "dosage": "2 puffs as needed",
                "reason_prescribed": "",
                "reason_prn": "Asthma rescue inhaler - use during breathing difficulty or before exercise"
            },
            {
                "medicine_name": "Montelukast",
                "strength": "10mg",
                "dosage": "1 tablet daily at bedtime",
                "reason_prescribed": "Asthma prevention - long-term control medication",
                "reason_prn": ""
            },
            {
                "medicine_name": "Loratadine",
                "strength": "10mg",
                "dosage": "1 tablet daily",
                "reason_prescribed": "Seasonal allergies management",
                "reason_prn": ""
            }
        ]
    }

    # Create profiles and medication cards
    profile_ids = {}

    for patient in patients:
        print(f"\nCreating profile for {patient['child_name']}...")

        try:
            profile_id = profile_manager.create_profile(patient)
            profile_ids[patient['child_name']] = profile_id
            print(f"  [OK] Profile created (ID: {profile_id})")

            # Create medication cards
            patient_meds = medications.get(profile_id, [])
            for med in patient_meds:
                med_card_manager.create_card(profile_id, med)
                print(f"  [OK] Medication card created: {med['medicine_name']}")

        except Exception as e:
            print(f"  [ERROR] {e}")

    # Create sample logs with administration entries
    print("\n" + "=" * 50)
    print("Creating medication logs...")

    # Get current month and previous month
    now = datetime.now()
    current_month = now.strftime("%B %Y")
    previous_month = (now.replace(day=1) - timedelta(days=1)).strftime("%B %Y")

    # Emma - Methylphenidate logs
    print(f"\nCreating logs for Emma Johnson...")
    emma_id = profile_ids.get("Emma Johnson")
    if emma_id:
        # Current month log
        try:
            med_info = {
                "medicine_name": "Methylphenidate",
                "strength": "10mg",
                "dosage": "1 tablet twice daily",
                "reason_prescribed": "ADHD management - helps with focus and attention in school",
                "reason_prn": ""
            }
            log_manager.create_log(emma_id, current_month, med_info)

            # Add some sample entries
            for day in range(1, min(now.day + 1, 16)):  # Up to day 15 or current day
                # Morning dose
                log_manager.add_entry(emma_id, "Methylphenidate", current_month, {
                    "day": day,
                    "time": "7:30 AM",
                    "initials": "JD",
                    "amount_remaining": f"{30 - (day * 2)} tablets"
                })
                # Afternoon dose
                log_manager.add_entry(emma_id, "Methylphenidate", current_month, {
                    "day": day,
                    "time": "3:00 PM",
                    "initials": "JD",
                    "amount_remaining": f"{30 - (day * 2) - 1} tablets"
                })

            print(f"  [OK] Methylphenidate log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

        # Melatonin log
        try:
            med_info = {
                "medicine_name": "Melatonin",
                "strength": "3mg",
                "dosage": "1 tablet at bedtime",
                "reason_prescribed": "Sleep support - helps establish healthy sleep patterns",
                "reason_prn": ""
            }
            log_manager.create_log(emma_id, current_month, med_info)

            for day in range(1, min(now.day + 1, 16)):
                log_manager.add_entry(emma_id, "Melatonin", current_month, {
                    "day": day,
                    "time": "8:00 PM",
                    "initials": "JD",
                    "amount_remaining": f"{30 - day} tablets"
                })

            print(f"  [OK] Melatonin log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

    # Michael - Fluoxetine logs
    print(f"\nCreating logs for Michael Chen...")
    michael_id = profile_ids.get("Michael Chen")
    if michael_id:
        try:
            med_info = {
                "medicine_name": "Fluoxetine",
                "strength": "20mg",
                "dosage": "1 capsule daily",
                "reason_prescribed": "Anxiety and depression management",
                "reason_prn": ""
            }
            log_manager.create_log(michael_id, current_month, med_info)

            for day in range(1, min(now.day + 1, 16)):
                log_manager.add_entry(michael_id, "Fluoxetine", current_month, {
                    "day": day,
                    "time": "8:00 AM",
                    "initials": "SM",
                    "amount_remaining": f"{30 - day} capsules"
                })

            print(f"  [OK] Fluoxetine log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

        # Ibuprofen PRN log with sporadic entries
        try:
            med_info = {
                "medicine_name": "Ibuprofen",
                "strength": "200mg",
                "dosage": "1-2 tablets as needed",
                "reason_prescribed": "",
                "reason_prn": "Pain relief for headaches or minor injuries. Max 3 doses per day."
            }
            log_manager.create_log(michael_id, current_month, med_info)

            # Add sporadic PRN entries
            prn_days = [2, 5, 7, 12]
            for day in prn_days:
                if day <= now.day:
                    log_manager.add_entry(michael_id, "Ibuprofen", current_month, {
                        "day": day,
                        "time": "2:00 PM",
                        "initials": "SM",
                        "amount_remaining": "24 tablets"
                    })

            print(f"  [OK] Ibuprofen PRN log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

    # Sofia - Multiple medications
    print(f"\nCreating logs for Sofia Martinez...")
    sofia_id = profile_ids.get("Sofia Martinez")
    if sofia_id:
        # Montelukast daily
        try:
            med_info = {
                "medicine_name": "Montelukast",
                "strength": "10mg",
                "dosage": "1 tablet daily at bedtime",
                "reason_prescribed": "Asthma prevention - long-term control medication",
                "reason_prn": ""
            }
            log_manager.create_log(sofia_id, current_month, med_info)

            for day in range(1, min(now.day + 1, 16)):
                log_manager.add_entry(sofia_id, "Montelukast", current_month, {
                    "day": day,
                    "time": "8:30 PM",
                    "initials": "LR",
                    "amount_remaining": f"{30 - day} tablets"
                })

            print(f"  [OK] Montelukast log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

        # Albuterol PRN
        try:
            med_info = {
                "medicine_name": "Albuterol Inhaler",
                "strength": "90mcg",
                "dosage": "2 puffs as needed",
                "reason_prescribed": "",
                "reason_prn": "Asthma rescue inhaler - use during breathing difficulty or before exercise"
            }
            log_manager.create_log(sofia_id, current_month, med_info)

            # Add some PRN entries
            prn_entries = [
                (3, "8:00 AM", "Before PE class"),
                (6, "2:30 PM", "Shortness of breath"),
                (10, "7:45 AM", "Before soccer practice"),
                (14, "3:00 PM", "Wheezing after playing")
            ]

            for day, time, _ in prn_entries:
                if day <= now.day:
                    log_manager.add_entry(sofia_id, "Albuterol Inhaler", current_month, {
                        "day": day,
                        "time": time,
                        "initials": "LR",
                        "amount_remaining": "160 puffs"
                    })

            print(f"  [OK] Albuterol Inhaler PRN log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

        # Loratadine
        try:
            med_info = {
                "medicine_name": "Loratadine",
                "strength": "10mg",
                "dosage": "1 tablet daily",
                "reason_prescribed": "Seasonal allergies management",
                "reason_prn": ""
            }
            log_manager.create_log(sofia_id, current_month, med_info)

            for day in range(1, min(now.day + 1, 16)):
                log_manager.add_entry(sofia_id, "Loratadine", current_month, {
                    "day": day,
                    "time": "7:00 AM",
                    "initials": "LR",
                    "amount_remaining": f"{30 - day} tablets"
                })

            print(f"  [OK] Loratadine log for {current_month}")
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n" + "=" * 50)
    print("[SUCCESS] Sample data generation complete!")
    print("\nGenerated:")
    print(f"  • {len(patients)} patient profiles")
    print(f"  • {sum(len(meds) for meds in medications.values())} medication cards")
    print(f"  • Multiple medication logs with administration entries")
    print("\nYou can now open the application and explore the sample data.")
    print("\nNote: To add sample images to medication cards,")
    print("      use the 'Add Image' button in the Medication Cards tab.")


if __name__ == "__main__":
    try:
        generate_sample_data()
    except Exception as e:
        print(f"\n[ERROR] Error generating sample data: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Update Character Rules - Updates all state JSONs with character handling rules
Based on OOSv2.txt documentation for stacked/slanted characters and O vs 0 usage
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class CharacterRulesUpdater:
    """Updates state JSON files with character handling rules"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data" / "states"
        
        # Character handling rules from OOSv2.txt
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load all character handling rules"""
        return {
            # O vs 0 Rules
            "no_letter_o": {
                "states": [
                    "alabama", "connecticut", "florida", "georgia", "hawaii",
                    "idaho", "kansas", "michigan", "minnesota", "missouri",
                    "montana", "nebraska", "nevada", "new_jersey", "new_mexico",
                    "texas", "utah"
                ],
                "description": "Does not use letter O on standard plates. Always use zero 0."
            },
            
            "o_with_letters_0_with_numbers": {
                "states": [
                    "alaska", "arkansas", "california", "colorado", "delaware",
                    "illinois", "indiana", "iowa", "louisiana", "massachusetts",
                    "maryland", "mississippi", "north_dakota", "ohio", "oklahoma",
                    "puerto_rico", "rhode_island", "virginia", "washington"
                ],
                "description": "Uses O with letters/personalized; uses 0 with numbers."
            },
            
            "o_only_personalized": {
                "states": ["arizona", "kentucky", "maine", "new_hampshire"],
                "description": "O only on personalized/vanity; standard uses 0."
            },
            
            "special_o_rules": {
                "new_york": "No O on standard plates; O and 0 allowed on vanity; O rounder, 0 slimmer.",
                "north_carolina": "O only used on Outer Banks (OBX) special tags.",
                "tennessee": "Standard plates do not use O; O and 0 used on Drive Out Tags and Temporary Operating Permits.",
                "pennsylvania": "Both O and 0 used; numbers are ¼\" taller than letters.",
                "oregon": "Interchangeable/treated as identical; O and 0 not distinguished for selection."
            },
            
            # Stacked/Slanted Character Rules
            "include_stacked": {
                "alabama": {
                    "include": ["X2", "TL", "TR", "DV", "Q1"],
                    "omit": ["200", "T"],
                    "position": "Middle of plate for include; left side for omit",
                    "notes": "Include stacked in middle, omit on left side"
                },
                "arkansas": {
                    "include": ["AB", "EM", "US", "PHS", "Ex", "FX", "PF"],
                    "omit": ["TRUCK", "ARK"],
                    "notes": "Include military/service codes, omit vehicle type"
                },
                "california": {
                    "include": [],
                    "omit": ["E"],
                    "max_characters": 10,
                    "notes": "OMIT stacked on LEFT if plate exceeds 10 characters. Omit letter E."
                },
                "colorado": {
                    "omit": ["FLT", "DV"],
                    "notes": "Omit fleet and disabled veteran codes"
                },
                "delaware": {
                    "include": ["CL"],
                    "notes": "Include CL stacked characters"
                },
                "idaho": {
                    "omit": ["PRP"],
                    "notes": "Omit PRP stacked characters"
                },
                "kansas": {
                    "include": ["PWR"],
                    "notes": "Include PWR stacked characters"
                },
                "kentucky": {
                    "include": ["BX", "AY", "GX", "HK", "V"],
                    "notes": "Include military/service stacked codes"
                },
                "louisiana": {
                    "include": ["MA", "NA", "AR", "MH", "NG"],
                    "omit": ["USMC", "NAVY", "ARMY"],
                    "notes": "ALWAYS include state codes. OMIT slanted branch names. Include slanted if no stacked (e.g., LA-ARMY453)"
                },
                "maryland": {
                    "include": ["AF", "HDV"],
                    "notes": "ALWAYS include Air Force and handicapped disabled veteran codes"
                },
                "michigan": {
                    "include": ["M", "S", "D"],
                    "omit": ["EX POW", "DV", "IRAQ", "VIETNAM"],
                    "notes": "Include university M, S and smaller M, D in middle. Omit one DV if both present. Omit branch/campaign names."
                },
                "minnesota": {
                    "omit": ["E"],
                    "notes": "Omit letter E on top right corner (it's a sticker)"
                },
                "mississippi": {
                    "include": ["TLR", "AU", "AV", "MC", "MQ", "DB"],
                    "omit": ["TLR on red plates ending with A"],
                    "prefix_rules": {
                        "B_F_small_numbers": "MUST be keyed",
                        "national_guard": "ADD prefix NG (e.g., MS-NG28624)"
                    },
                    "notes": "Include codes except TLR on specific red plates. Key B/F plates with small numbers. Add NG prefix for National Guard."
                },
                "nevada": {
                    "include": ["DT"],
                    "notes": "Include DT stacked characters"
                },
                "new_hampshire": {
                    "include": ["CH"],
                    "symbols": ["&", "+", "and", "-"],
                    "notes": "INCLUDE CH. ALWAYS INCLUDE symbols (&, +, and, -). Dropdown always Standard, not 'DASH IN tag'. NH ONLY accepts these symbols."
                },
                "new_jersey": {
                    "include": ["WD", "NG", "HM", "NJ"],
                    "omit": ["small characters on dealer plates"],
                    "notes": "Include stacked/small numbers. Omit small chars on New/Used Dealer plates. Non-dealer plates include ALL characters including small ones (e.g., NJ-5647DTM where 47 is small)"
                },
                "new_mexico": {
                    "include": ["MI", "LC", "SU", "KID"],
                    "notes": "Include ALL stacked characters"
                },
                "new_york": {
                    "include": ["EMTP", "VAS", "DAV", "MD"],
                    "notes": "Include stacked characters like emergency medical, veterans, disabled, medical"
                },
                "north_carolina": {
                    "include": ["DV", "IC", "VF", "PH", "PD", "NC", "NG"],
                    "omit": ["ALL symbols (-)"],
                    "prefix_rules": {
                        "supreme_court": "ADD prefix SC"
                    },
                    "notes": "Include stacked chars. Vertical/small NC or NG must be keyed. Omit dashes. Add SC prefix for Supreme Court plates."
                },
                "north_dakota": {
                    "omit": ["PRP"],
                    "notes": "Omit PRP on left side of plate"
                },
                "oklahoma": {
                    "omit": ["UD013"],
                    "notes": "Omit UD013 on Used Dealer plates"
                },
                "ontario": {
                    "omit": ["PRP"],
                    "notes": "Omit PRP on YOURS TO DISCOVER plate"
                },
                "oregon": {
                    "include": ["HP", "HU", "Y"],
                    "notes": "INCLUDE stacked HP, HU. Apportioned plates INCLUDE small Y."
                },
                "pennsylvania": {
                    "include": ["US ARMY VETERAN", "US AIR VETERAN", "VETERAN", "NATIONAL GUARD", "EMERGENCY MEDICAL SERVICES", "FIRE FIGHTER", "PD"],
                    "notes": "Include stacked on veteran/service plates. Include small PD by wheelchair symbol."
                },
                "rhode_island": {
                    "include": ["TRL"],
                    "omit": ["dash (-)"],
                    "notes": "Include TRL stacked. DO NOT add dash."
                },
                "south_carolina": {
                    "include": ["CC", "EA", "VT", "ZD"],
                    "visual_notes": "Tree in middle of plate",
                    "notes": "Include stacked characters CC, EA, VT, ZD"
                },
                "tennessee": {
                    "include": ["V0"],
                    "omit": ["T"],
                    "notes": "Volunteers plates: DO NOT include T. Include V0 characters."
                },
                "texas": {
                    "include": ["DV"],
                    "omit": ["T"],
                    "notes": "Include DV stacked. Omit letter T in white part of plate."
                },
                "vermont": {
                    "omit": ["TRK"],
                    "notes": "Omit TRK stacked characters"
                },
                "virginia": {
                    "include": ["ID", "ZE", "TR", "RS", "FD"],
                    "omit": ["DV", "VET"],
                    "notes": "Include stacked ID, ZE, TR, RS. Include FD from Fire Fighter logo. Omit vertical/diagonal DV, VET with different font/color."
                },
                "washington": {
                    "include": ["AR", "GRN"],
                    "omit": ["TRAN"],
                    "notes": "Include stacked AR, GRN. Omit word TRAN."
                },
                "wyoming": {
                    "include": ["TRL", "22T"],
                    "prefix_rules": {
                        "single_digit_before_horse": "Include 0 in front (e.g., WY-013918)"
                    },
                    "notes": "Include slanted TRL, 22T for TRUCK. Single digit before horse needs leading 0."
                }
            },
            
            # Special visual notes
            "visual_identifiers": {
                "south_carolina": "Tree in middle",
                "oregon": "OR in top left"
            },
            
            # Special rules
            "special_notes": {
                "u_haul": "U-Haul can use customer plates"
            }
        }
    
    def update_state_json(self, state_filename: str):
        """Update a single state JSON file with character rules"""
        json_file = self.data_dir / f"{state_filename}.json"
        
        if not json_file.exists():
            print(f"  ⚠️  File not found: {state_filename}.json")
            return False
        
        try:
            # Read current JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update O vs 0 rules
            state_updated = False
            
            # Check if state should not use letter O
            if state_filename in self.rules["no_letter_o"]["states"]:
                data["uses_zero_for_o"] = True
                data["allows_letter_o"] = False
                if "notes" not in data or "does not allow" not in data["notes"].lower():
                    note_addition = "Does not use letter 'O' on standard plates. Always use zero '0'."
                    data["notes"] = f"{data.get('notes', '')} {note_addition}".strip()
                state_updated = True
            
            elif state_filename in self.rules["o_with_letters_0_with_numbers"]["states"]:
                data["uses_zero_for_o"] = True
                data["allows_letter_o"] = True
                note_addition = "Uses 'O' with letters/personalized plates; uses '0' with numbers."
                if "notes" not in data or note_addition not in data["notes"]:
                    data["notes"] = f"{data.get('notes', '')} {note_addition}".strip()
                state_updated = True
            
            elif state_filename in self.rules["o_only_personalized"]["states"]:
                data["uses_zero_for_o"] = True
                data["allows_letter_o"] = True
                note_addition = "Letter 'O' only appears on personalized/vanity plates; standard plates use '0'."
                if "notes" not in data or note_addition not in data["notes"]:
                    data["notes"] = f"{data.get('notes', '')} {note_addition}".strip()
                state_updated = True
            
            # Add stacked character rules
            if state_filename in self.rules["include_stacked"]:
                stacked_rules = self.rules["include_stacked"][state_filename]
                
                # Ensure processing_metadata exists
                if "processing_metadata" not in data:
                    data["processing_metadata"] = {}
                
                if "global_rules" not in data["processing_metadata"]:
                    data["processing_metadata"]["global_rules"] = {}
                
                # Add stacked character handling rules
                data["processing_metadata"]["global_rules"]["stacked_characters"] = {
                    "include": stacked_rules.get("include", []),
                    "omit": stacked_rules.get("omit", []),
                    "position": stacked_rules.get("position"),
                    "max_characters": stacked_rules.get("max_characters"),
                    "prefix_rules": stacked_rules.get("prefix_rules"),
                    "symbols_allowed": stacked_rules.get("symbols"),
                    "notes": stacked_rules.get("notes")
                }
                
                state_updated = True
            
            # Add special rules from special_o_rules
            if state_filename in self.rules["special_o_rules"]:
                special_rule = self.rules["special_o_rules"][state_filename]
                if "notes" not in data or special_rule not in data["notes"]:
                    data["notes"] = f"{data.get('notes', '')} {special_rule}".strip()
                state_updated = True
            
            # Add visual identifiers
            if state_filename in self.rules["visual_identifiers"]:
                visual_note = self.rules["visual_identifiers"][state_filename]
                data["visual_identifier_notes"] = visual_note
                state_updated = True
            
            # Save if updated
            if state_updated:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ Error updating {state_filename}: {e}")
            return False
    
    def update_all_states(self):
        """Update all state JSON files with character rules"""
        print("🚀 Updating State Character Rules")
        print("=" * 60)
        print()
        
        # Get all JSON files
        json_files = sorted(self.data_dir.glob("*.json"))
        
        updated_count = 0
        skipped_count = 0
        
        for json_file in json_files:
            state_filename = json_file.stem
            print(f"Processing {state_filename}...", end=" ")
            
            if self.update_state_json(state_filename):
                print("✅ Updated")
                updated_count += 1
            else:
                print("⏭️  No updates needed")
                skipped_count += 1
        
        print()
        print("=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Updated: {updated_count} states")
        print(f"⏭️  Skipped: {skipped_count} states")
        print(f"📁 Total: {len(json_files)} states")
        print()
        print("🎉 Character rules update complete!")
        print()
        print("Next steps:")
        print("1. Review updated JSON files")
        print("2. Run: python scripts/updating/auto_update_dropdown.py")
        print("3. Restart application")


def main():
    updater = CharacterRulesUpdater()
    updater.update_all_states()


if __name__ == "__main__":
    main()

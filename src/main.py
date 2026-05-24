"""
Maltese Location Fuzzy Matching - For Vapi Python Execution
Run this directly in Vapi as a Python code artifact
"""

import json

from rapidfuzz import fuzz, process

# All 68 Malta localities
MALTA_LOCALITIES = {
    "Valletta": {"postcode": "VLT", "region": "Capital", "phonetic": "vah-LET-tah"},
    "Sliema": {"postcode": "SLM", "region": "Eastern", "phonetic": "SLEE-mah"},
    "Marsaskala": {
        "postcode": "MSK",
        "region": "Southeastern",
        "phonetic": "mar-sah-SCAH-lah",
    },
    "Żabbar": {"postcode": "ZBR", "region": "Southern", "phonetic": "zab-bar"},
    "Żejtun": {"postcode": "ZJT", "region": "Southern", "phonetic": "zay-TOON"},
    "Siggiewi": {"postcode": "SGI", "region": "Western", "phonetic": "sig-JOO-ee"},
    "Mdina": {"postcode": "MDN", "region": "Western", "phonetic": "im-DEE-nah"},
    "Mosta": {"postcode": "MST", "region": "Northern", "phonetic": "MOS-tah"},
    "Mellieha": {"postcode": "MLH", "region": "Northern", "phonetic": "mel-LEE-hah"},
    "San Pawl il-Bahar": {
        "postcode": "SPB",
        "region": "Northern",
        "phonetic": "san POWL il bah-HAR",
    },
    "Birkirkara": {
        "postcode": "BKR",
        "region": "Eastern",
        "phonetic": "bir-kir-KAH-rah",
    },
    "Naxxar": {"postcode": "NXR", "region": "Northern", "phonetic": "NAH-shar"},
    "Tarxien": {"postcode": "TXN", "region": "Southeastern", "phonetic": "tar-SHEEN"},
    "Paola": {"postcode": "PLA", "region": "Southern", "phonetic": "PAH-oh-lah"},
    "Luqa": {"postcode": "LQA", "region": "Southern", "phonetic": "LOO-ah"},
    "Marsaxlokk": {
        "postcode": "MXL",
        "region": "Southeastern",
        "phonetic": "mar-sah-SHLOCK",
    },
    "Dingli": {"postcode": "DNJ", "region": "Western", "phonetic": "DIN-glee"},
    "Birgu": {"postcode": "BRG", "region": "Southern Harbour", "phonetic": "Beer-goo"},
    "Bormla": {"postcode": "BML", "region": "Southern Harbour", "phonetic": "Bor-mla"},
    "Senglea": {
        "postcode": "SGL",
        "region": "Southern Harbour",
        "phonetic": "Seng-LEE-ah",
    },
    "Rabat": {"postcode": "RBT", "region": "Western", "phonetic": "rah-BAT"},
    "Qormi": {"postcode": "QRM", "region": "Central", "phonetic": "or-mee"},
    "Attard": {"postcode": "ATT", "region": "Central", "phonetic": "ah-TARD"},
    "Balzan": {"postcode": "BZN", "region": "Central", "phonetic": "bal-ZAN"},
    "Lija": {"postcode": "LJA", "region": "Central", "phonetic": "Lee-ya"},
    "Gżira": {"postcode": "GZR", "region": "Eastern", "phonetic": "zee-rah"},
    "Msida": {"postcode": "MSD", "region": "Eastern", "phonetic": "msi-DAH"},
    "Swieqi": {"postcode": "SWQ", "region": "Eastern", "phonetic": "SWAY-kee"},
    "St. Julian's": {
        "postcode": "STJ",
        "region": "Eastern",
        "phonetic": "saint JOO-leeanz",
    },
    "Floriana": {
        "postcode": "FLR",
        "region": "Capital Adjacent",
        "phonetic": "flor-ee-AH-nah",
    },
    "Hamrun": {"postcode": "HMR", "region": "Central", "phonetic": "HAM-run"},
    "Paceville": {"postcode": "PCL", "region": "Eastern", "phonetic": "pace-VIL"},
    "Pembroke": {"postcode": "PMB", "region": "Eastern", "phonetic": "PEM-broke"},
    "Pietà": {"postcode": "PTA", "region": "Central", "phonetic": "Pee-ta"},
    "Xgħajra": {"postcode": "XGH", "region": "Southeastern", "phonetic": "SHAY-rah"},
    "Fgura": {"postcode": "FGR", "region": "Southern", "phonetic": "foo-ra"},
    "Għarb": {"postcode": "GHB", "region": "Gozo", "phonetic": "HARB"},
    "Għaxaq": {"postcode": "GHX", "region": "Southern", "phonetic": "ah-SHAK"},
    "Victoria": {"postcode": "VCT", "region": "Gozo", "phonetic": "vik-TOR-ee-ah"},
    "Xagħra": {"postcode": "XGR", "region": "Gozo", "phonetic": "SHAH-rah"},
    "Nadur": {"postcode": "NDR", "region": "Gozo", "phonetic": "nah-DUR"},
    "Xlendi": {"postcode": "XLD", "region": "Gozo", "phonetic": "SHLEN-dee"},
    "Sannat": {"postcode": "SNT", "region": "Gozo", "phonetic": "san-NAT"},
    "San Lawrenz": {"postcode": "SNL", "region": "Gozo", "phonetic": "san LAH-rents"},
    "Kerċem": {"postcode": "KRC", "region": "Gozo", "phonetic": "ker-CHEM"},
    "Fontana": {"postcode": "FTN", "region": "Gozo", "phonetic": "fon-TAH-nah"},
    "Żebbuġ": {"postcode": "ZEB", "region": "Western", "phonetic": "zeb-BUG"},
    "Żebbuġ (Gozo)": {"postcode": "ZEG", "region": "Gozo", "phonetic": "zeb-BUG"},
    "Zurrieq": {"postcode": "ZRQ", "region": "Southern", "phonetic": "zoo-REE-ek"},
    "Qrendi": {"postcode": "QRD", "region": "Southern", "phonetic": "ren-DEE"},
    "Xemxija": {"postcode": "XEM", "region": "Northern", "phonetic": "shem-SHEE-yah"},
    "Safi": {"postcode": "SAF", "region": "Southern", "phonetic": "SAH-fee"},
    "Kirkop": {"postcode": "KRK", "region": "Southern", "phonetic": "kir-KOP"},
    "Gudja": {"postcode": "GDJ", "region": "Southern", "phonetic": "GOOD-yah"},
    "Marsa": {"postcode": "MRS", "region": "Central", "phonetic": "mar-sa"},
    "Imsida": {"postcode": "IMS", "region": "Eastern", "phonetic": "mi-see-DAH"},
    "Imqabba": {"postcode": "IMQ", "region": "Southern", "phonetic": "im-KAB-bah"},
    "Imġarr": {"postcode": "IMG", "region": "Northern", "phonetic": "im-JAHR"},
    "Iklin": {"postcode": "IKL", "region": "Northern", "phonetic": "L-Iklin"},
    "Ta' Xbiex": {"postcode": "TXB", "region": "Eastern", "phonetic": "Ta-Shbeesh"},
    "Xewkija": {"postcode": "XWK", "region": "Gozo", "phonetic": "shew-KIE-yah"},
    "Munxar": {"postcode": "MNX", "region": "Gozo", "phonetic": "moon-SHAR"},
    "Għajnsielem": {"postcode": "GHS", "region": "Gozo", "phonetic": "ain-SEEL-em"},
    "Imtarfa": {"postcode": "IMT", "region": "Western", "phonetic": "im-TAR-fah"},
    "Kalkara": {"postcode": "KLK", "region": "Southeastern", "phonetic": "kal-KAH-rah"},
    "Mtaħleb": {"postcode": "MTH", "region": "Western", "phonetic": "im-tah-HLEB"},
    "Santa Venera": {
        "postcode": "STV",
        "region": "Central",
        "phonetic": "san-tah veh-NAY-rah",
    },
    "San Ġwann": {"postcode": "SGW", "region": "Central", "phonetic": "San Jwann"},
    "Qala": {"postcode": "QLa", "region": "Gozo", "phonetic": "AH-lah"},
    "Santa Luċija": {
        "postcode": "STL",
        "region": "Gozo",
        "phonetic": "san-tah loo-CHEE-yah",
    },
    "Dwejra": {"postcode": "DWJ", "region": "Gozo", "phonetic": "dwaj-RAH"},
    "Comino": {"postcode": "CMN", "region": "Island", "phonetic": "KOM-ee-no"},
}

# Phonetic variant mapping
PHONETIC_VARIANTS = {
    "shamsia": "Xemxija",
    "shemsia": "Xemxija",
    "shemshia": "Xemxija",
    "kshem": "Xemxija",
    "kshia": "Xemxija",
}


def normalize_maltese(text):
    """Normalize Maltese characters to ASCII for matching."""
    if not text:
        return ""

    text = text.lower().strip()
    text = text.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

    maltese_map = {
        "ż": "z",
        "ħ": "h",
        "ċ": "c",
        "ġ": "j",
        "à": "a",
        "è": "e",
        "ì": "i",
        "ò": "o",
        "ù": "u",
    }

    for maltese_char, ascii_char in maltese_map.items():
        text = text.replace(maltese_char, ascii_char)

    return text.strip()


def fuzzy_match_location(user_input, context=None):
    """Match user-spoken location to official Malta locality."""

    if context is None:
        context = {}

    user_input = user_input.strip() if user_input else ""

    if not user_input:
        return {"error": "No input provided", "recommendation": "Provide location name"}

    # Normalize user input
    normalized_input = normalize_maltese(user_input)

    if not normalized_input:
        return {
            "error": "Input became empty after normalization",
            "user_input": user_input,
        }

    # Check phonetic variants first
    if normalized_input in PHONETIC_VARIANTS:
        official_name = PHONETIC_VARIANTS[normalized_input]
        locality_data = MALTA_LOCALITIES[official_name]
        return {
            "location": official_name,
            "postcode": locality_data["postcode"],
            "region": locality_data["region"],
            "phonetic": locality_data["phonetic"],
            "confidence": 95,
            "recommendation": "Confirm location with user",
        }

    # Fuzzy matching
    localities = list(MALTA_LOCALITIES.keys())
    normalized_localities = [normalize_maltese(loc) for loc in localities]

    matches = process.extract(
        normalized_input,
        normalized_localities,
        scorer=fuzz.TokenSetRatio,
        limit=5,
        score_cutoff=50,
    )

    jw_matches = process.extract(
        normalized_input,
        normalized_localities,
        scorer=fuzz.JaroWinkler,
        limit=5,
        score_cutoff=50,
    )

    all_matches = matches + jw_matches

    if not all_matches:
        return {"location": None, "confidence": 0, "message": "No locations found"}

    # Get best match
    best_match_normalized, score = all_matches[0]
    original_index = normalized_localities.index(best_match_normalized)
    official_name = localities[original_index]
    locality_data = MALTA_LOCALITIES[official_name]

    confidence = int(score)

    # Low confidence - return candidates
    if confidence < 70:
        seen = set()
        candidates = []
        for match_norm, match_score in all_matches:
            idx = normalized_localities.index(match_norm)
            loc_name = localities[idx]
            if loc_name not in seen:
                seen.add(loc_name)
                candidates.append(
                    {
                        "location": loc_name,
                        "postcode": MALTA_LOCALITIES[loc_name]["postcode"],
                        "region": MALTA_LOCALITIES[loc_name]["region"],
                        "score": int(match_score),
                    }
                )
            if len(candidates) >= 3:
                break

        return {
            "location": None,
            "confidence": confidence,
            "top_candidates": candidates,
            "recommendation": "Ask user to clarify from candidates",
            "message": f"Did you mean {candidates[0]['location']}, {candidates[1]['location']}, or {candidates[2]['location']}?",
        }

    # Context-aware disambiguation
    if "geographic_hint" in context:
        hint = context["geographic_hint"].lower()
        if any(
            word in hint
            for word in [
                "coast",
                "water",
                "south",
                "sea",
                "fish",
                "restaurant",
                "waterfront",
            ]
        ):
            if official_name == "Marsa":
                official_name = "Marsaskala"
                locality_data = MALTA_LOCALITIES["Marsaskala"]

    # Marsa vs Marsaskala special handling
    if official_name == "Marsa" and normalized_input.startswith("mar"):
        marsaskala_norm = normalize_maltese("Marsaskala")
        marsaskala_score = fuzz.TokenSetRatio(normalized_input, marsaskala_norm)
        jw_score = fuzz.JaroWinkler(normalized_input, marsaskala_norm)
        marsaskala_confidence = int(max(marsaskala_score, jw_score))

        if marsaskala_confidence > confidence - 5:
            official_name = "Marsaskala"
            locality_data = MALTA_LOCALITIES["Marsaskala"]
            confidence = marsaskala_confidence

    return {
        "location": official_name,
        "postcode": locality_data["postcode"],
        "region": locality_data["region"],
        "phonetic": locality_data["phonetic"],
        "confidence": confidence,
        "recommendation": "Confirm location with user"
        if confidence >= 85
        else "Ask for confirmation",
    }


# Example usage
if __name__ == "__main__":
    # Test cases
    test_inputs = [
        ("Valletta", {}),
        ("Shamsia", {}),
        ("Marsa", {"geographic_hint": "coast"}),
        ("Zabbar", {}),
    ]

    for user_input, context in test_inputs:
        result = fuzzy_match_location(user_input, context)
        print(f"Input: '{user_input}' -> {json.dumps(result, indent=2)}\n")

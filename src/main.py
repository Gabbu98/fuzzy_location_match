"""
Maltese Location Fuzzy Matching API - FULL VERSION
For deployment to Render with src/main.py structure
"""

from flask import Flask, jsonify, request
from rapidfuzz import fuzz, process

app = Flask(__name__)

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

# Phonetic variant mapping - maps common misspellings/accent variants to official names
PHONETIC_VARIANTS = {
    "shamsia": "Xemxija",  # "Shamsia" → Xemxija (shem-SHEE-yah)
    "shemsia": "Xemxija",
    "shemshia": "Xemxija",
    "kshem": "Xemxija",
    "kshia": "Xemxija",
}


def normalize_maltese(text):
    """Normalize Maltese characters to ASCII for matching."""
    if not text:
        return ""

    # Convert to lowercase and decompose
    text = text.lower().strip()

    # Remove punctuation
    text = text.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

    # Maltese character mapping
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


@app.route("/api/fuzzy-match-location", methods=["POST"])
def fuzzy_match_location():
    """Match user-spoken location to official Malta locality."""
    try:
        data = request.json or {}
        user_input = data.get("input", "").strip()

        # Handle stt_confidence - can be number, string, or missing
        stt_conf_raw = data.get("stt_confidence", 1.0)
        try:
            if isinstance(stt_conf_raw, str) and stt_conf_raw:
                stt_confidence = float(stt_conf_raw)
            elif stt_conf_raw:
                stt_confidence = float(stt_conf_raw)
            else:
                stt_confidence = 1.0  # Default to high confidence
        except (ValueError, TypeError):
            stt_confidence = 1.0

        context = data.get("context", {})

        # Validate input
        if not user_input:
            return jsonify(
                {
                    "error": "No input provided",
                    "recommendation": "Provide location name",
                }
            ), 400

        # Normalize user input
        normalized_input = normalize_maltese(user_input)

        if not normalized_input:
            return jsonify(
                {
                    "error": "Input became empty after normalization",
                    "user_input": user_input,
                }
            ), 400

        # CHECK PHONETIC VARIANTS FIRST - these are known problematic spellings
        if normalized_input in PHONETIC_VARIANTS:
            official_name = PHONETIC_VARIANTS[normalized_input]
            locality_data = MALTA_LOCALITIES[official_name]
            return jsonify(
                {
                    "location": official_name,
                    "postcode": locality_data["postcode"],
                    "region": locality_data["region"],
                    "phonetic": locality_data["phonetic"],
                    "confidence": 95,  # High confidence for known variant
                    "stt_confidence": stt_confidence,
                    "recommendation": "Confirm location with user",
                }
            )

        # Get all locality names and normalize them
        localities = list(MALTA_LOCALITIES.keys())
        normalized_localities = [normalize_maltese(loc) for loc in localities]

        # Use RapidFuzz - Token Set Ratio is best for partial/fuzzy matches
        matches = process.extract(
            normalized_input,
            normalized_localities,
            scorer=fuzz.TokenSetRatio,  # Better for word-by-word matching
            limit=5,
            score_cutoff=50,  # Lower cutoff to get candidates
        )

        # Also try Jaro-Winkler for phonetic matching
        jw_matches = process.extract(
            normalized_input,
            normalized_localities,
            scorer=fuzz.JaroWinkler,
            limit=5,
            score_cutoff=50,
        )

        # Take best from both methods
        all_matches = matches + jw_matches

        if not all_matches:
            return jsonify(
                {
                    "location": None,
                    "confidence": 0,
                    "stt_confidence": stt_confidence,
                    "message": "No locations found",
                }
            )

        # Get best match
        best_match_normalized, score = all_matches[0]
        original_index = normalized_localities.index(best_match_normalized)
        official_name = localities[original_index]
        locality_data = MALTA_LOCALITIES[official_name]

        confidence = int(score)

        # If confidence is low, return candidates
        if confidence < 70:
            # Get top 3 unique candidates
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

            return jsonify(
                {
                    "location": None,
                    "confidence": confidence,
                    "stt_confidence": stt_confidence,
                    "top_candidates": candidates,
                    "recommendation": "Ask user to clarify from candidates",
                    "message": f"Did you mean {candidates[0]['location']}, {candidates[1]['location']}, or {candidates[2]['location']}?",
                }
            )

        # CONTEXT-AWARE DISAMBIGUATION
        # If context hints point to Marsaskala, prefer it
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
                # Geographic hint suggests Marsaskala (coastal)
                if official_name == "Marsa":
                    official_name = "Marsaskala"
                    locality_data = MALTA_LOCALITIES["Marsaskala"]

        # SPECIAL HANDLING: Marsa vs Marsaskala Disambiguation
        # If user said something like "Marcela/Marsha/Marsau" and best match is "Marsa",
        # check if "Marsaskala" might be what they meant
        if official_name == "Marsa" and normalized_input.startswith("mar"):
            # Check Marsaskala score
            marsaskala_norm = normalize_maltese("Marsaskala")
            marsaskala_score = fuzz.TokenSetRatio(normalized_input, marsaskala_norm)
            jw_score = fuzz.JaroWinkler(normalized_input, marsaskala_norm)
            marsaskala_confidence = int(max(marsaskala_score, jw_score))

            # If Marsaskala is very close in score, prefer it (more likely for "Marcela" inputs)
            if marsaskala_confidence > confidence - 5:  # Within 5% points
                official_name = "Marsaskala"
                locality_data = MALTA_LOCALITIES["Marsaskala"]
                confidence = marsaskala_confidence

        # High confidence match
        return jsonify(
            {
                "location": official_name,
                "postcode": locality_data["postcode"],
                "region": locality_data["region"],
                "phonetic": locality_data["phonetic"],
                "confidence": confidence,
                "stt_confidence": stt_confidence,
                "recommendation": "Confirm location with user"
                if confidence >= 85
                else "Ask for confirmation",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "error_type": type(e).__name__}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "Maltese Location Fuzzy Matcher",
            "localities_loaded": len(MALTA_LOCALITIES),
        }
    ), 200


@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {
            "message": "Maltese Location Fuzzy Matching API",
            "endpoints": {
                "health": "/health",
                "fuzzy_match": "/api/fuzzy-match-location (POST)",
            },
            "localities": len(MALTA_LOCALITIES),
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

"""
Golden Set Test Decks & Category Expectations for SIH ATS Scanner.
Contains:
- 3 Strong Decks
- 3 Weak Decks
- 2 Edge Case Decks (exactly 6 slides limit, borderline tech depth)
"""

GOLDEN_SET_SAMPLES = [
    # ==========================================
    # STRONG DECKS (3)
    # ==========================================
    {
        "id": "strong_deck_1",
        "name": "Smart Traffic System (Strong)",
        "ps_title": "AI-Based Smart Traffic Management System for Urban Cities",
        "ps_description": "Optimize traffic light signals using computer vision and edge computing.",
        "slides": [
            {"slide_number": 1, "raw_text": "AI-Based Smart Traffic Management System. Team Alpha.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Traffic congestion at urban intersections causes delays, emissions, and emergency vehicle blocking.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Dynamic traffic light control using real-time video analytics and automated queue detection.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: Built with Python, FastAPI, PostgreSQL database with pgvector, and YOLOv8 object detection model for vehicle count inference.", "bullet_count": 3},
            {"slide_number": 5, "raw_text": "Impact & Benefits: 35% reduction in wait time, 20% lower fuel consumption, priority corridor routing for ambulances.", "bullet_count": 3},
            {"slide_number": 6, "raw_text": "References & Team: Contact team@alpha.io. References: IEEE 2024 Traffic Paper.", "bullet_count": 2}
        ],
        "expected_ranges": {
            "structure_format": (90.0, 100.0),
            "clarity": (85.0, 100.0),
            "ps_alignment": (75.0, 100.0),
            "technical_depth": (80.0, 100.0),
            "originality": (80.0, 100.0),
            "overall_score": (80.0, 100.0)
        }
    },
    {
        "id": "strong_deck_2",
        "name": "Blockchain Supply Chain (Strong)",
        "ps_title": "Blockchain-Based Supply Chain Transparency for Agriculture Products",
        "ps_description": "Track agricultural produce from farm to consumer using decentralized ledger.",
        "slides": [
            {"slide_number": 1, "raw_text": "AgriChain: Decentralized Farm-to-Fork Traceability. Team AgriTech.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Lack of transparency and price exploitation by middlemen in produce distribution.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Smart contracts recording farmer batches with QR codes on packaging for consumer verification.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: Developed with Solidity smart contracts on Polygon, Node.js backend API, and IPFS for decentralized metadata storage.", "bullet_count": 3},
            {"slide_number": 5, "raw_text": "Impact & Benefits: Direct farmer payouts, zero counterfeit labeling, verifiably fresh produce.", "bullet_count": 2},
            {"slide_number": 6, "raw_text": "References & Team: Contact contact@agrichain.in. References: Polygon Docs, OpenZeppelin.", "bullet_count": 2}
        ],
        "expected_ranges": {
            "structure_format": (90.0, 100.0),
            "clarity": (85.0, 100.0),
            "ps_alignment": (75.0, 100.0),
            "technical_depth": (80.0, 100.0),
            "originality": (80.0, 100.0),
            "overall_score": (80.0, 100.0)
        }
    },
    {
        "id": "strong_deck_3",
        "name": "Water Quality Monitoring (Strong)",
        "ps_title": "IoT-Enabled Water Leakage and Quality Monitoring Network",
        "ps_description": "Real-time water pipe leakage detection and contamination alerting system.",
        "slides": [
            {"slide_number": 1, "raw_text": "AquaGuard: Smart Water Quality & Leakage Network. Team Hydro.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Over 40% clean municipal water lost to undetected pipe leaks and undetected chemical contamination.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Distributed IoT sensor nodes measuring pressure, pH, and turbidity with cellular telemetry alerts.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: ESP32 microcontrollers with MQTT protocol publishing to InfluxDB time-series database and Grafana dashboard visualization.", "bullet_count": 3},
            {"slide_number": 5, "raw_text": "Impact & Benefits: Early leak pinpointing within 10 meters, automatic valve shutdown upon chemical contamination.", "bullet_count": 2},
            {"slide_number": 6, "raw_text": "References & Team: Contact info@aquaguard.org. References: Jal Jeevan Mission Guidelines.", "bullet_count": 2}
        ],
        "expected_ranges": {
            "structure_format": (90.0, 100.0),
            "clarity": (85.0, 100.0),
            "ps_alignment": (75.0, 100.0),
            "technical_depth": (80.0, 100.0),
            "originality": (80.0, 100.0),
            "overall_score": (80.0, 100.0)
        }
    },

    # ==========================================
    # WEAK DECKS (3)
    # ==========================================
    {
        "id": "weak_deck_1",
        "name": "Bloated Decks (9 Slides + Boilerplate)",
        "ps_title": "AI-Based Smart Traffic Management System for Urban Cities",
        "ps_description": "Optimize traffic light signals.",
        "slides": [
            {"slide_number": 1, "raw_text": "Sample Team Name Here. Insert Title Here.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Traffic is bad.", "bullet_count": 1},
            {"slide_number": 3, "raw_text": "Slide 3 text lorem ipsum dolor sit amet " + "word " * 80, "bullet_count": 8},
            {"slide_number": 4, "raw_text": "Technical Stack: We will use Backend, Database, AI, Machine Learning, Cloud. " + "detail " * 80, "bullet_count": 7},
            {"slide_number": 5, "raw_text": "More Tech Stack: Software engineering principles will be applied. " + "text " * 80, "bullet_count": 8},
            {"slide_number": 6, "raw_text": "Architecture: The system connects to internet. " + "para " * 80, "bullet_count": 9},
            {"slide_number": 7, "raw_text": "Slide 7 details and extra stuff. " + "extra " * 80, "bullet_count": 7},
            {"slide_number": 8, "raw_text": "Slide 8 details and extra stuff. " + "content " * 80, "bullet_count": 8},
            {"slide_number": 9, "raw_text": "Slide 9 details and extra stuff. " + "more " * 80, "bullet_count": 8}
        ],
        "expected_ranges": {
            "structure_format": (30.0, 65.0), # Oversized (9 slides, >6 max limit penalty)
            "clarity": (20.0, 60.0),          # High bullet count per slide & wall of text
            "overall_score": (0.0, 65.0)
        }
    },
    {
        "id": "weak_deck_2",
        "name": "Off-Topic Deck",
        "ps_title": "Early Detection of Crop Diseases Using Satellite Imagery",
        "ps_description": "Analyze satellite images to detect agricultural crop diseases.",
        "slides": [
            {"slide_number": 1, "raw_text": "Crypto Trading Bot Platform. Team CryptoX.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: High volatility in Bitcoin and Ethereum trading markets.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Automated algorithmic trading bot executing high frequency arbitrage orders.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: Built with Python, Binance API, and WebSocket streaming connection.", "bullet_count": 2},
            {"slide_number": 5, "raw_text": "Impact & Benefits: Maximize portfolio yields and minimize liquidation risks.", "bullet_count": 2},
            {"slide_number": 6, "raw_text": "References & Team: Contact crypto@trade.io", "bullet_count": 2}
        ],
        "expected_ranges": {
            "ps_alignment": (0.0, 40.0),      # Completely off-topic compared to Satellite Crop Disease PS
            "overall_score": (0.0, 70.0)
        }
    },
    {
        "id": "weak_deck_3",
        "name": "Vague Tech & No Sections",
        "ps_title": "Automated Resume and Presentation ATS Evaluator",
        "ps_description": "Automated scoring of presentations.",
        "slides": [
            {"slide_number": 1, "raw_text": "Smart Scanner Presentation.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "We will build a website to scan files.", "bullet_count": 1},
            {"slide_number": 3, "raw_text": "Tech details: We will use web development, database management, and artificial intelligence algorithms.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Features: Fast scanning, accurate scores, modern UI.", "bullet_count": 3}
        ],
        "expected_ranges": {
            "structure_format": (40.0, 75.0), # Missing required sections
            "technical_depth": (40.0, 65.0),  # Vague tech stack (no specific framework/database/model named)
            "overall_score": (0.0, 70.0)
        }
    },

    # ==========================================
    # EDGE CASES (2)
    # ==========================================
    {
        "id": "edge_deck_1_exact_6_slides",
        "name": "Exact 6 Slides Boundary Limit",
        "ps_title": "AI-Based Smart Traffic Management System for Urban Cities",
        "ps_description": "Traffic control system.",
        "slides": [
            {"slide_number": 1, "raw_text": "Urban Traffic AI. Team Boundary.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Traffic jams in cities.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Adaptive light timing.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: Python FastAPI service with PostgreSQL database.", "bullet_count": 2},
            {"slide_number": 5, "raw_text": "Impact & Benefits: Reduced travel times.", "bullet_count": 2},
            {"slide_number": 6, "raw_text": "References & Team: Contact contact@boundary.org", "bullet_count": 2}
        ],
        "expected_ranges": {
            "structure_format": (90.0, 100.0), # Exactly 6 slides (limit compliance = 100% slide count score)
            "overall_score": (70.0, 100.0)
        }
    },
    {
        "id": "edge_deck_2_borderline_tech",
        "name": "Borderline Technical Depth Deck",
        "ps_title": "Automated Resume and Presentation ATS Evaluator",
        "ps_description": "Evaluate resumes and pitch decks.",
        "slides": [
            {"slide_number": 1, "raw_text": "ATS Evaluator Project. Team EdgeTech.", "bullet_count": 0},
            {"slide_number": 2, "raw_text": "Problem Statement: Manual evaluation of pitch decks takes too long.", "bullet_count": 2},
            {"slide_number": 3, "raw_text": "Proposed Solution: Automated scoring platform.", "bullet_count": 2},
            {"slide_number": 4, "raw_text": "Technical Approach: Built with Python for backend processing. Uses database for storing records. Machine learning is used for score calculation.", "bullet_count": 3},
            {"slide_number": 5, "raw_text": "Impact & Benefits: Speeds up evaluation time by 80%.", "bullet_count": 2},
            {"slide_number": 6, "raw_text": "References & Team: Contact team@edgetech.in", "bullet_count": 2}
        ],
        "expected_ranges": {
            "technical_depth": (50.0, 75.0), # Python named (+12.5), but no specific DB/model/workflow (+50 base = 62.5 pts)
            "overall_score": (60.0, 92.0)
        }
    }
]

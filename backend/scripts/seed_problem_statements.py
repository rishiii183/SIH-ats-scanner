import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import DBManager

SIH_PROBLEM_STATEMENTS = [
    {
        "ps_id": "SIH1601",
        "title": "AI-Driven Real-Time Urban Traffic Signal Control System",
        "description": "Develop an adaptive traffic signal control system using computer vision on junction CCTV cameras and edge IoT microcontrollers to prioritize emergency ambulances and minimize congestion delays.",
        "theme": "Smart Cities",
        "category": "Software"
    },
    {
        "ps_id": "SIH1602",
        "title": "Automated Resume and Presentation ATS Evaluator",
        "description": "Build an AI-powered ATS scanning engine that audits 6-slide presentation decks and resumes against official rubrics, computing sentence-transformers embeddings and technical depth metrics.",
        "theme": "EdTech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1603",
        "title": "Blockchain-Based Agricultural Supply Chain Traceability",
        "description": "Implement a decentralized blockchain solution using smart contracts and QR code tagging for transparent farm-to-fork tracking of organic agricultural produce.",
        "theme": "AgriTech & Food Tech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1604",
        "title": "IoT Smart Water Quality and Leakage Detection Network",
        "description": "Design an IoT-enabled sensor telemetry network for real-time monitoring of drinking water pH, turbidity, flow rate, and pipe burst localization in municipal distribution pipelines.",
        "theme": "Clean & Green Tech",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1605",
        "title": "Early Detection of Crop Leaf Diseases Using Drone Multispectral Imagery",
        "description": "Develop deep learning convolutional neural network models trained on high-resolution drone multispectral imagery for early automated diagnosis of fungal crop infections.",
        "theme": "AgriTech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1606",
        "title": "Autonomous Solar Panel Cleaning & Health Monitoring Robot",
        "description": "Build a self-powered dry cleaning robotic rover with thermal imaging sensors to clean dust accumulation and detect hotspot micro-cracks on large utility-scale solar farms.",
        "theme": "Renewable Energy",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1607",
        "title": "AI-Powered Early Wildfire Detection & Firebreak Prediction System",
        "description": "Create an integrated satellite and IoT remote sensing platform to detect forest thermal anomalies early and simulate predictive firebreak containment routes.",
        "theme": "Disaster Management",
        "category": "Software"
    },
    {
        "ps_id": "SIH1608",
        "title": "Decentralized Medical Record Exchange Protocol (ABDM Compliant)",
        "description": "Design an encrypted, patient-consented electronic health record (EHR) interoperability framework compliant with Ayushman Bharat Digital Mission (ABDM) standards.",
        "theme": "Healthcare & MedTech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1609",
        "title": "Smart Grid Load Balancing & Peak Shaving AI Controller",
        "description": "Develop machine learning forecasting models for real-time electrical grid load prediction and automated battery energy storage dispatch to mitigate peak demand surges.",
        "theme": "Smart Energy",
        "category": "Software"
    },
    {
        "ps_id": "SIH1610",
        "title": "Low-Cost Wearable ECG & Cardiac Arrhythmia Detection Patch",
        "description": "Develop a lightweight single-lead wearable patch with onboard edge AI inference for real-time detection and alert generation for atrial fibrillation.",
        "theme": "MedTech",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1611",
        "title": "Deepfake Video & Synthetic Audio Detection Engine",
        "description": "Build a multi-modal neural network pipeline to analyze facial motion inconsistency, artifact frequency shifts, and biological pulse signatures for deepfake verification.",
        "theme": "Cyber Security",
        "category": "Software"
    },
    {
        "ps_id": "SIH1612",
        "title": "Smart Helmet for Underground Mining Safety & Gas Leak Alert",
        "description": "Construct an industrial IoT helmet equipped with methane/CO gas sensors, thermal alert indicators, fallback mesh networking, and impact detection for subterranean miners.",
        "theme": "Industrial Safety",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1613",
        "title": "AI-Based Railway Track Defect & Ultrasonic Crack Inspection",
        "description": "Create a high-speed locomotive-mounted computer vision and ultrasonic sensor suite to continuously inspect rail joint cracks and track misalignment.",
        "theme": "Transportation",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1614",
        "title": "Automated Legal Document Summarization & Precedent Retrieval",
        "description": "Engineered NLP transformer pipeline to summarize complex legal judgments, extract cited statutory sections, and map similarity with past court precedents.",
        "theme": "LegalTech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1615",
        "title": "Smart E-Waste Sorting Robot Using Hyperspectral Vision",
        "description": "Build a robotic arm pick-and-place system driven by hyperspectral imaging to categorize printed circuit board (PCB) components and precious metal scrap.",
        "theme": "Waste Management",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1616",
        "title": "Marine Oil Spill Detection & Autonomous Remediation Skimmer",
        "description": "Construct a swarm drone surveillance and autonomous unmanned surface boat with absorbent skimmer booms to clean coastal oil slicks.",
        "theme": "Oceanography",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1617",
        "title": "Real-Time Sign Language to Multi-Lingual Speech Translator",
        "description": "Develop a mobile accessibility camera application translating Indian Sign Language (ISL) gestures into real-time spoken regional languages.",
        "theme": "Accessibility",
        "category": "Software"
    },
    {
        "ps_id": "SIH1618",
        "title": "Smart Cold Chain Logistics Monitoring for Milk & Vaccines",
        "description": "Build an ultra-low power cellular IoT sensor beacon tracking temperature, humidity, and door-open events inside refrigerated transport trucks.",
        "theme": "Supply Chain",
        "category": "Hardware"
    },
    {
        "ps_id": "SIH1619",
        "title": "Privacy-Preserving Federated Learning for Fraud Detection",
        "description": "Implement a differential privacy federated learning framework allowing multiple banking institutions to collaboratively train credit fraud detection models without sharing raw customer logs.",
        "theme": "FinTech",
        "category": "Software"
    },
    {
        "ps_id": "SIH1620",
        "title": "Micro-Hydro Turbine Energy Harvester for Rural Canals",
        "description": "Design a portable low-head kinetic water turbine generator optimized for continuous clean electrification along irrigation canals in off-grid villages.",
        "theme": "Rural Development",
        "category": "Hardware"
    }
]

def seed_problem_statements():
    client = DBManager.get_client()
    if not client:
        print("Error: Supabase client unavailable.")
        return

    print("==================================================")
    print("      SEEDING SIH PROBLEM STATEMENT BANK         ")
    print("==================================================")

    inserted_count = 0
    for ps in SIH_PROBLEM_STATEMENTS:
        try:
            # Check if exists
            res = client.table("problem_statements").select("id").eq("ps_id", ps["ps_id"]).execute()
            if not res.data:
                client.table("problem_statements").insert(ps).execute()
                inserted_count += 1
        except Exception as e:
            print(f"Error seeding {ps['ps_id']}: {e}")

    # Query total count
    count_res = client.table("problem_statements").select("count", count="exact").execute()
    total_count = count_res.count or 0

    print(f"\nSeeding Complete!")
    print(f"Newly Inserted Rows: {inserted_count}")
    print(f"Total Database Row Count: {total_count}")

    # Fetch 3 real sample rows
    samples = client.table("problem_statements").select("ps_id, title, theme, category").limit(3).execute()
    print("\n--- 3 REAL SAMPLE ROWS IN DATABASE ---")
    for row in (samples.data or []):
        print(f"[{row['ps_id']}] {row['title']} | Theme: {row['theme']} | Category: {row['category']}")

if __name__ == "__main__":
    seed_problem_statements()

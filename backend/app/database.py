import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

# In-Memory DB Store for fast local development and instant testing
IN_MEMORY_DB = {
    "problem_statements": [
            {
                    "id": "ps-1",
                    "ps_id": "SIH26001",
                    "title": "AI-Based early warning and landslide Risk Monitoring System in NER",
                    "description": "Ministry of Development of North Eastern Region (MDoNER) - AI-Based early warning and landslide Risk Monitoring System in NER",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-2",
                    "ps_id": "SIH26002",
                    "title": "Al-Based Smart Logistics and Accessibility Intelligence Platform for North Eastern Region (NER)",
                    "description": "Ministry of Development of North Eastern Region (MDoNER) - Al-Based Smart Logistics and Accessibility Intelligence Platform for North Eastern Region (NER)",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-3",
                    "ps_id": "SIH26003",
                    "title": "AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)",
                    "description": "Ministry of Development of North Eastern Region (MDoNER) - AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-4",
                    "ps_id": "SIH26004",
                    "title": "Al-Assisted Early Detection System for Osteoarthritis (OA) Risk Markers in North Eastern Region (NER)",
                    "description": "Ministry of Development of North Eastern Region (MDoNER) - Al-Assisted Early Detection System for Osteoarthritis (OA) Risk Markers in North Eastern Region (NER)",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-5",
                    "ps_id": "SIH26005",
                    "title": "Solar-Powered Smart Mini Cold Storage System for Fresh Vegetables in North Eastern Region (NER)",
                    "description": "Ministry of Development of North Eastern Region (MDoNER) - Solar-Powered Smart Mini Cold Storage System for Fresh Vegetables in North Eastern Region (NER)",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-6",
                    "ps_id": "SIH26006",
                    "title": "Development of an Intelligent Freight Forecasting Model for Optimized Vessel Chartering and Bulk Cargo Procurement from overseas to East Coast of India",
                    "description": "Ministry of Steel - Development of an Intelligent Freight Forecasting Model for Optimized Vessel Chartering and Bulk Cargo Procurement from overseas to East Coast of India",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-7",
                    "ps_id": "SIH26007",
                    "title": "Safe and Efficient Operation of Mine Vehicles in Fog and Low-Visibility Conditions in Open Cast Iron Ore Mines.",
                    "description": "Ministry of Steel - Safe and Efficient Operation of Mine Vehicles in Fog and Low-Visibility Conditions in Open Cast Iron Ore Mines.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-8",
                    "ps_id": "SIH26008",
                    "title": "Belt Joint Rupture and Conveyor Belt Damages in Iron Ore Mining Industry: Intelligent Monitoring and Prediction of Conveyor Belt Joint Rupture and Damages in Iron Ore Mining Industry.",
                    "description": "Ministry of Steel - Belt Joint Rupture and Conveyor Belt Damages in Iron Ore Mining Industry: Intelligent Monitoring and Prediction of Conveyor Belt Joint Rupture and Damages in Iron Ore Mining Industry.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-9",
                    "ps_id": "SIH26009",
                    "title": "Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.",
                    "description": "Ministry of Steel - Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-10",
                    "ps_id": "SIH26010",
                    "title": "Survey/Resurvey of Rural Agricultural Land in lndia",
                    "description": "Ministry of Rural Development - Survey/Resurvey of Rural Agricultural Land in lndia",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-11",
                    "ps_id": "SIH26011",
                    "title": "3D ULPIN Generation and vertical Property Mapping SYstem",
                    "description": "Ministry of Rural Development - 3D ULPIN Generation and vertical Property Mapping SYstem",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-12",
                    "ps_id": "SIH26012",
                    "title": "AI-Based Automated Urban Parcel Mapping and Cadastral Feature Extraction System using Drone lmagery",
                    "description": "Ministry of Rural Development - AI-Based Automated Urban Parcel Mapping and Cadastral Feature Extraction System using Drone lmagery",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-13",
                    "ps_id": "SIH26013",
                    "title": "Automated lntegration and lntelligent Harmonization of Multi-source Geospatial Data for urban Land Record Management.",
                    "description": "Ministry of Rural Development - Automated lntegration and lntelligent Harmonization of Multi-source Geospatial Data for urban Land Record Management.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-14",
                    "ps_id": "SIH26014",
                    "title": "An lntegrated GIS-based Digital Public lnfrastructure for Land Governance",
                    "description": "Ministry of Rural Development - An lntegrated GIS-based Digital Public lnfrastructure for Land Governance",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-15",
                    "ps_id": "SIH26015",
                    "title": "Application of Geospatial Techniques for visualization and analysis to interpret Geo-Coded lmages to enhance watershed Development Outcomes.",
                    "description": "Ministry of Rural Development - Application of Geospatial Techniques for visualization and analysis to interpret Geo-Coded lmages to enhance watershed Development Outcomes.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-16",
                    "ps_id": "SIH26016",
                    "title": "Real-Time National Land Acquisition & Management System for End-to-End Digital Monitoring and Decision Support",
                    "description": "Ministry of Rural Development - Real-Time National Land Acquisition & Management System for End-to-End Digital Monitoring and Decision Support",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-17",
                    "ps_id": "SIH26017",
                    "title": "Predictive Analytics System for Early Detection of Land Acquisition Delays",
                    "description": "Ministry of Rural Development - Predictive Analytics System for Early Detection of Land Acquisition Delays",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-18",
                    "ps_id": "SIH26018",
                    "title": "Intelligent Land Record Digitization and Validation System",
                    "description": "Ministry of Rural Development - Intelligent Land Record Digitization and Validation System",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-19",
                    "ps_id": "SIH26019",
                    "title": "National Digital Platform for Research, Policy Innovation, and Evidence-Based Land Governance",
                    "description": "Ministry of Rural Development - National Digital Platform for Research, Policy Innovation, and Evidence-Based Land Governance",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-20",
                    "ps_id": "SIH26020",
                    "title": "Design and Development of Innovative Hand-Spinning Equipment for Enhancing Khadi Artisan Productivity and Income",
                    "description": "Ministry of MSME - Design and Development of Innovative Hand-Spinning Equipment for Enhancing Khadi Artisan Productivity and Income",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-21",
                    "ps_id": "SIH26021",
                    "title": "Honey Chain: A block chain-based system for honey traceability and smart beekeeping management.",
                    "description": "Ministry of MSME - Honey Chain: A block chain-based system for honey traceability and smart beekeeping management.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-22",
                    "ps_id": "SIH26022",
                    "title": "Design and develop a smart, solar-powered drying and compact packaging system to support home-based agarbatti manufacturing by rural women artisans.",
                    "description": "Ministry of MSME - Design and develop a smart, solar-powered drying and compact packaging system to support home-based agarbatti manufacturing by rural women artisans.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-23",
                    "ps_id": "SIH26023",
                    "title": "AI-Powered Geological, Mining and other Reporting Solution for CMPDI/CIL subsidiaries",
                    "description": "Ministry of Coal - AI-Powered Geological, Mining and other Reporting Solution for CMPDI/CIL subsidiaries",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-24",
                    "ps_id": "SIH26024",
                    "title": "AI-Based Smart Governance and Compliance Monitoring System for Coal Mines",
                    "description": "Ministry of Coal - AI-Based Smart Governance and Compliance Monitoring System for Coal Mines",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-25",
                    "ps_id": "SIH26025",
                    "title": "Development of an AI-enabled Low Cost Real Time Mine Subsidence Monitoring, Prediction and Early Warning System for Underground Coal Mines in India",
                    "description": "Ministry of Coal - Development of an AI-enabled Low Cost Real Time Mine Subsidence Monitoring, Prediction and Early Warning System for Underground Coal Mines in India",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-26",
                    "ps_id": "SIH26026",
                    "title": "Development of Mobile (Quadruped)/Handheld Device/System for Real-Time Detection of Narcotics and Explosives across Indian Railways.",
                    "description": "Ministry of Railways - Development of Mobile (Quadruped)/Handheld Device/System for Real-Time Detection of Narcotics and Explosives across Indian Railways.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "hardware"
            },
            {
                    "id": "ps-27",
                    "ps_id": "SIH26027",
                    "title": "Al-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways",
                    "description": "Ministry of Railways - Al-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-28",
                    "ps_id": "SIH26028",
                    "title": "Dynamic Forecast of Expected Time of Arrival (ETA) for Coaching Trains",
                    "description": "Ministry of Railways - Dynamic Forecast of Expected Time of Arrival (ETA) for Coaching Trains",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-29",
                    "ps_id": "SIH26029",
                    "title": "Automated High-Current Short-Circuit Test System for IEC 60898-1:2015 MCB Compliance.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Automated High-Current Short-Circuit Test System for IEC 60898-1:2015 MCB Compliance.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-30",
                    "ps_id": "SIH26030",
                    "title": "Automated Cable Specimen Preparation System for IS 10810 and IS 7098 Compliance.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Automated Cable Specimen Preparation System for IS 10810 and IS 7098 Compliance.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-31",
                    "ps_id": "SIH26031",
                    "title": "Quality assessment and grading of onions are often subjective and vary across procurement centers, resulting in disputes and inconsistencies.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Quality assessment and grading of onions are often subjective and vary across procurement centers, resulting in disputes and inconsistencies.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-32",
                    "ps_id": "SIH26032",
                    "title": "Farmers often face long waiting times, lack of information regarding procurement schedules, and uncertainty about procurement status.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Farmers often face long waiting times, lack of information regarding procurement schedules, and uncertainty about procurement status.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-33",
                    "ps_id": "SIH26033",
                    "title": "Multiple intermediaries reduce farmers earnings and increase consumer prices.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Multiple intermediaries reduce farmers earnings and increase consumer prices.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-34",
                    "ps_id": "SIH26034",
                    "title": "Software System to check compliance of Packaged Commodities under Legal Metrology(Packaged Commodities) Rules, 2011 by scanning products, images and labels.",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Software System to check compliance of Packaged Commodities under Legal Metrology(Packaged Commodities) Rules, 2011 by scanning products, images and labels.",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-35",
                    "ps_id": "SIH26035",
                    "title": "Development of a Software Program/Application for Generation of Test Reports for Non-Automatic Weighing Instruments (NAWI) as per OIML Recommendation R- 76",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Development of a Software Program/Application for Generation of Test Reports for Non-Automatic Weighing Instruments (NAWI) as per OIML Recommendation R- 76",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-36",
                    "ps_id": "SIH26036",
                    "title": "Development of an Online Verification System for Weighing and Measuring Instruments",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Development of an Online Verification System for Weighing and Measuring Instruments",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-37",
                    "ps_id": "SIH26037",
                    "title": "Adaptive Path Planning and Collision Avoidance for Autonomous Vehicles on Unstructured Indian Roads",
                    "description": "MathWorks - Adaptive Path Planning and Collision Avoidance for Autonomous Vehicles on Unstructured Indian Roads",
                    "theme": "Smart Vehicles",
                    "category": "software"
            },
            {
                    "id": "ps-38",
                    "ps_id": "SIH26038",
                    "title": "Explainable AI for Diabetic Retinopathy Screening in Rural India",
                    "description": "MathWorks - Explainable AI for Diabetic Retinopathy Screening in Rural India",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-39",
                    "ps_id": "SIH26039",
                    "title": "Al-Powered Underground Mine Safety, Monitoring and Rescue System.",
                    "description": "Government of Jharkhand - Al-Powered Underground Mine Safety, Monitoring and Rescue System.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-40",
                    "ps_id": "SIH26040",
                    "title": "Smart Water Purification and Quality Monitoring System for Rural and Mining-Affected Areas.",
                    "description": "Government of Jharkhand - Smart Water Purification and Quality Monitoring System for Rural and Mining-Affected Areas.",
                    "theme": "Clean & Green Technology",
                    "category": "hardware"
            },
            {
                    "id": "ps-41",
                    "ps_id": "SIH26041",
                    "title": "AR-Based Vocational Training Simulator for Industrial Safety in Jharkhand's Mining & Manufacturing Sector",
                    "description": "Government of Jharkhand - AR-Based Vocational Training Simulator for Industrial Safety in Jharkhand's Mining & Manufacturing Sector",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-42",
                    "ps_id": "SIH26042",
                    "title": "Al-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education",
                    "description": "Government of Jharkhand - Al-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-43",
                    "ps_id": "SIH26043",
                    "title": "A digital platform to crowdsource societal challenges and facilitate collaborative problem solving through universities and industry partnerships",
                    "description": "Government of Jharkhand - A digital platform to crowdsource societal challenges and facilitate collaborative problem solving through universities and industry partnerships",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-44",
                    "ps_id": "SIH26044",
                    "title": "Portal for Academia - Industry collaboration for Skill Mapping, Internships and Placement",
                    "description": "Ministry of Ayush - Portal for Academia - Industry collaboration for Skill Mapping, Internships and Placement",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-45",
                    "ps_id": "SIH26045",
                    "title": "IP-SAKTI Sahayak a multilingual, RAG-based (source-cited) AI assistant for Intellectual Property and regulatory guidance in Ayurveda, across national and international regimes.",
                    "description": "Ministry of Ayush - IP-SAKTI Sahayak a multilingual, RAG-based (source-cited) AI assistant for Intellectual Property and regulatory guidance in Ayurveda, across national and international regimes.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-46",
                    "ps_id": "SIH26046",
                    "title": "AIIA Clinical Trials Dashboard - a real-time, cloud-based, GCP-compliant Clinical Trial Management System (CTMS) for Ayurveda research, with CDISC/FHIR-interoperable data, role-based KPIs, and integrated ethics, regulatory (CTRI / NDCT Rules 2019) and pharma covigilance tracking.",
                    "description": "Ministry of Ayush - AIIA Clinical Trials Dashboard - a real-time, cloud-based, GCP-compliant Clinical Trial Management System (CTMS) for Ayurveda research, with CDISC/FHIR-interoperable data, role-based KPIs, and integrated ethics, regulatory (CTRI / NDCT Rules 2019) and pharma covigilance tracking.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-47",
                    "ps_id": "SIH26047",
                    "title": "Patient Case-Taking Software",
                    "description": "Ministry of Ayush - Patient Case-Taking Software",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-48",
                    "ps_id": "SIH26048",
                    "title": "iKwath - a pod-based smart Kwatha (Kadha) maker that prepares a fresh, AFI/API-standardized decoction from coarse powder (yavaku?a c?r?a) on demand, in the shortest practical time without altering the decoctions quality or yield",
                    "description": "Ministry of Ayush - iKwath - a pod-based smart Kwatha (Kadha) maker that prepares a fresh, AFI/API-standardized decoction from coarse powder (yavaku?a c?r?a) on demand, in the shortest practical time without altering the decoctions quality or yield",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-49",
                    "ps_id": "SIH26049",
                    "title": "Modifications to improve the reliability, efficiency,and lifespan of electrical and electronic equipment and systems in the ambient condition of subzero temperature and low pressure of High Altitude Areas(HAA) and Super High Altitude Areas (SHAA) of Ladakh region.",
                    "description": "DRDO - Modifications to improve the reliability, efficiency,and lifespan of electrical and electronic equipment and systems in the ambient condition of subzero temperature and low pressure of High Altitude Areas(HAA) and Super High Altitude Areas (SHAA) of Ladakh region.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-50",
                    "ps_id": "SIH26050",
                    "title": "High Altitude Performance Optimization and Robust Design of Anti-Drone System.",
                    "description": "DRDO - High Altitude Performance Optimization and Robust Design of Anti-Drone System.",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-51",
                    "ps_id": "SIH26051",
                    "title": "Software Based Model Development for Design of Area Specific Shelter for Thermal Comfort Maintenance.",
                    "description": "DRDO - Software Based Model Development for Design of Area Specific Shelter for Thermal Comfort Maintenance.",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-52",
                    "ps_id": "SIH26052",
                    "title": "To develop an AI/ML-enabled adaptive noise cancellation (ANC) system that effectively suppresses stationary, non-stationary, and impulsive defence noises while maintaining high speech intelligibility and real-time performance on embedded hardware.",
                    "description": "DRDO - To develop an AI/ML-enabled adaptive noise cancellation (ANC) system that effectively suppresses stationary, non-stationary, and impulsive defence noises while maintaining high speech intelligibility and real-time performance on embedded hardware.",
                    "theme": "Miscellaneous",
                    "category": "hardware"
            },
            {
                    "id": "ps-53",
                    "ps_id": "SIH26053",
                    "title": "Adaptive Variable Resolution 2.5D Lidar Mapping for Dynamic Environment Perception",
                    "description": "DRDO - Adaptive Variable Resolution 2.5D Lidar Mapping for Dynamic Environment Perception",
                    "theme": "Smart Vehicles",
                    "category": "software"
            },
            {
                    "id": "ps-54",
                    "ps_id": "SIH26054",
                    "title": "AI-Enabled Real-Time Digital Twin System for Health Monitoring, Fault Prediction and Mission Reliability Enhancement of Aero Piston Engines used in MALE UAVs.",
                    "description": "DRDO - AI-Enabled Real-Time Digital Twin System for Health Monitoring, Fault Prediction and Mission Reliability Enhancement of Aero Piston Engines used in MALE UAVs.",
                    "theme": "Robotics and Drones",
                    "category": "software"
            },
            {
                    "id": "ps-55",
                    "ps_id": "SIH26055",
                    "title": "Smart Scan strategy for Electronic Warfare",
                    "description": "DRDO - Smart Scan strategy for Electronic Warfare",
                    "theme": "Robotics and Drones",
                    "category": "software"
            },
            {
                    "id": "ps-56",
                    "ps_id": "SIH26056",
                    "title": "Development of a Real-time Airfare Price Index for India through Automated Web Scraping of Airline and Online Travel Aggregator Portals for Augmentation of the Consumer Price Index (CPI).",
                    "description": "MoSPI - Development of a Real-time Airfare Price Index for India through Automated Web Scraping of Airline and Online Travel Aggregator Portals for Augmentation of the Consumer Price Index (CPI).",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-57",
                    "ps_id": "SIH26057",
                    "title": "AI-Powered Automated Underwater Marine Debris and Anomaly Detection System using Side-Scan Sonar Imagery",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Powered Automated Underwater Marine Debris and Anomaly Detection System using Side-Scan Sonar Imagery",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-58",
                    "ps_id": "SIH26058",
                    "title": "Development of a Low-Power, Real-Time Adaptive Software-Defined Sonar Transmitter Payload for Autonomous Underwater Vehicles (AUVs)",
                    "description": "Ministry of Earth Sciences (MoES) - Development of a Low-Power, Real-Time Adaptive Software-Defined Sonar Transmitter Payload for Autonomous Underwater Vehicles (AUVs)",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-59",
                    "ps_id": "SIH26059",
                    "title": "AI-Enabled Antarctic Sea-Ice, Iceberg Trajectory, and Navigation Decision Support System",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Enabled Antarctic Sea-Ice, Iceberg Trajectory, and Navigation Decision Support System",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-60",
                    "ps_id": "SIH26060",
                    "title": "Digital Platform for efficient remote management of Indian Antarctic Research Stations",
                    "description": "Ministry of Earth Sciences (MoES) - Digital Platform for efficient remote management of Indian Antarctic Research Stations",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-61",
                    "ps_id": "SIH26061",
                    "title": "AI-Driven Smart Energy Management System for Polar Research Stations",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Driven Smart Energy Management System for Polar Research Stations",
                    "theme": "Clean & Green Technology",
                    "category": "software"
            },
            {
                    "id": "ps-62",
                    "ps_id": "SIH26062",
                    "title": "Integrated Polar Expedition Logistics and Asset Management System",
                    "description": "Ministry of Earth Sciences (MoES) - Integrated Polar Expedition Logistics and Asset Management System",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-63",
                    "ps_id": "SIH26063",
                    "title": "Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal",
                    "description": "Ministry of Earth Sciences (MoES) - Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-64",
                    "ps_id": "SIH26064",
                    "title": "Low-Cost Deployable Seafloor Metal Detection Sensor for Ocean Resource Exploration",
                    "description": "Ministry of Earth Sciences (MoES) - Low-Cost Deployable Seafloor Metal Detection Sensor for Ocean Resource Exploration",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-65",
                    "ps_id": "SIH26065",
                    "title": "Autonomous Low-Cost Ocean Observation Platform for Polar and Southern Oceans",
                    "description": "Ministry of Earth Sciences (MoES) - Autonomous Low-Cost Ocean Observation Platform for Polar and Southern Oceans",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-66",
                    "ps_id": "SIH26066",
                    "title": "OceanEmbed - Satellite Embedding-Based Deep Learning Framework for Reconstruction of Subsurface Ocean Temperature from Surface Satellite Observations.",
                    "description": "Ministry of Earth Sciences (MoES) - OceanEmbed - Satellite Embedding-Based Deep Learning Framework for Reconstruction of Subsurface Ocean Temperature from Surface Satellite Observations.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-67",
                    "ps_id": "SIH26067",
                    "title": "Develop a web-based interactive 3D visualization platform that integrates numerical ocean model outputs and in-situ observations.",
                    "description": "Ministry of Earth Sciences (MoES) - Develop a web-based interactive 3D visualization platform that integrates numerical ocean model outputs and in-situ observations.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-68",
                    "ps_id": "SIH26068",
                    "title": "WeatherGPT: Conversational AI for Weather Forecasting, Alerts, and Climate Information",
                    "description": "Ministry of Earth Sciences (MoES) - WeatherGPT: Conversational AI for Weather Forecasting, Alerts, and Climate Information",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-69",
                    "ps_id": "SIH26069",
                    "title": "National Weather Big Data Analytics Platform",
                    "description": "Ministry of Earth Sciences (MoES) - National Weather Big Data Analytics Platform",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-70",
                    "ps_id": "SIH26070",
                    "title": "To develop an Artificial Intelligence (AI) / Machine Learning (ML) based system for identification, classification, and prediction of different tropical cyclone patterns using multi-source satellite data.",
                    "description": "Ministry of Earth Sciences (MoES) - To develop an Artificial Intelligence (AI) / Machine Learning (ML) based system for identification, classification, and prediction of different tropical cyclone patterns using multi-source satellite data.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-71",
                    "ps_id": "SIH26071",
                    "title": "AI/ML-Based Integrated heavy rainfall Early Warning and Inundation Prediction System using Satellite, Radar, observational Weather and numerical weather prediction model data.",
                    "description": "Ministry of Earth Sciences (MoES) - AI/ML-Based Integrated heavy rainfall Early Warning and Inundation Prediction System using Satellite, Radar, observational Weather and numerical weather prediction model data.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-72",
                    "ps_id": "SIH26072",
                    "title": "AIML based Nowcasting of thunderstorm and lightning using atmospheric observation including multiple radars, satellite, lightning and model data.",
                    "description": "Ministry of Earth Sciences (MoES) - AIML based Nowcasting of thunderstorm and lightning using atmospheric observation including multiple radars, satellite, lightning and model data.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-73",
                    "ps_id": "SIH26073",
                    "title": "AI/ML-Based Intelligent Anomaly Detection for Automatic Weather Stations (AWS)",
                    "description": "Ministry of Earth Sciences (MoES) - AI/ML-Based Intelligent Anomaly Detection for Automatic Weather Stations (AWS)",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-74",
                    "ps_id": "SIH26074",
                    "title": "Downscaling of weather forecast from Block level to Panchayat level: Inferring high-resolution plots/ data/ information from low-resolution plot /data /information /variables for agro-meteorological advisory services.",
                    "description": "Ministry of Earth Sciences (MoES) - Downscaling of weather forecast from Block level to Panchayat level: Inferring high-resolution plots/ data/ information from low-resolution plot /data /information /variables for agro-meteorological advisory services.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-75",
                    "ps_id": "SIH26075",
                    "title": "Participants are invited to design and develop **CAPACITY CONNECT A Digital Capacity Building and Learning Management Portal** to support organizational training, competency development, and knowledge sharing through a centralized web-based platform.",
                    "description": "Ministry of Earth Sciences (MoES) - Participants are invited to design and develop **CAPACITY CONNECT A Digital Capacity Building and Learning Management Portal** to support organizational training, competency development, and knowledge sharing through a centralized web-based platform.",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-76",
                    "ps_id": "SIH26076",
                    "title": "Development of personalized homepage for 'Mausam' mobile application:",
                    "description": "Ministry of Earth Sciences (MoES) - Development of personalized homepage for 'Mausam' mobile application:",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-77",
                    "ps_id": "SIH26077",
                    "title": "AI-Driven Hyper-Local Early Warning System for Severe Weather Nowcasting",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Driven Hyper-Local Early Warning System for Severe Weather Nowcasting",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-78",
                    "ps_id": "SIH26078",
                    "title": "AI-Driven Spatio-Temporal Tracking of Extreme Weather Anomalies in Medium-Range Forecasts",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Driven Spatio-Temporal Tracking of Extreme Weather Anomalies in Medium-Range Forecasts",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-79",
                    "ps_id": "SIH26079",
                    "title": "AI-Based Forecast Bust Detection for Medium-Range Weather Forecasts",
                    "description": "Ministry of Earth Sciences (MoES) - AI-Based Forecast Bust Detection for Medium-Range Weather Forecasts",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-80",
                    "ps_id": "SIH26080",
                    "title": "Regime-Aware AI Post-Processing of Monsoon Rainfall Forecasts",
                    "description": "Ministry of Earth Sciences (MoES) - Regime-Aware AI Post-Processing of Monsoon Rainfall Forecasts",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-81",
                    "ps_id": "SIH26081",
                    "title": "Hybrid AI\u2013NWP Multi-Model Forecast Blending System",
                    "description": "Ministry of Earth Sciences (MoES) - Hybrid AI\u2013NWP Multi-Model Forecast Blending System",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-82",
                    "ps_id": "SIH26082",
                    "title": "Air Pollution\u2013Weather Coupled Forecasting System (Delhi NCR Focus)",
                    "description": "Ministry of Earth Sciences (MoES) - Air Pollution\u2013Weather Coupled Forecasting System (Delhi NCR Focus)",
                    "theme": "Clean & Green Technology",
                    "category": "software"
            },
            {
                    "id": "ps-83",
                    "ps_id": "SIH26083",
                    "title": "Extreme Heatwave Early Warning and Human Thermal Stress Index",
                    "description": "Ministry of Earth Sciences (MoES) - Extreme Heatwave Early Warning and Human Thermal Stress Index",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-84",
                    "ps_id": "SIH26084",
                    "title": "Convective scale nowcasting for Thunderstorms, Hail & Cloudbursts (06 hr)",
                    "description": "Ministry of Earth Sciences (MoES) - Convective scale nowcasting for Thunderstorms, Hail & Cloudbursts (06 hr)",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-85",
                    "ps_id": "SIH26085",
                    "title": "Urban Flood Nowcasting System (Drainage and Rainfall Coupling)",
                    "description": "Ministry of Earth Sciences (MoES) - Urban Flood Nowcasting System (Drainage and Rainfall Coupling)",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-86",
                    "ps_id": "SIH26086",
                    "title": "Hyperlocal Monsoon Onset & Break Prediction System (Block/Village Scale)",
                    "description": "Ministry of Earth Sciences (MoES) - Hyperlocal Monsoon Onset & Break Prediction System (Block/Village Scale)",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-87",
                    "ps_id": "SIH26087",
                    "title": "AI & LMS - Enabled Cooperative Capacity Building, ERP & Employment Ecosystem",
                    "description": "Ministry of Cooperation - AI & LMS - Enabled Cooperative Capacity Building, ERP & Employment Ecosystem",
                    "theme": "Smart Education",
                    "category": "hardware"
            },
            {
                    "id": "ps-88",
                    "ps_id": "SIH26088",
                    "title": "Multilingual Cooperative Governance & Legal Assistance Chatbot",
                    "description": "Ministry of Cooperation - Multilingual Cooperative Governance & Legal Assistance Chatbot",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-89",
                    "ps_id": "SIH26089",
                    "title": "Cooperative Gig Services Platform for Household & Community Services",
                    "description": "Ministry of Cooperation - Cooperative Gig Services Platform for Household & Community Services",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-90",
                    "ps_id": "SIH26090",
                    "title": "AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans",
                    "theme": "Heritage & Culture",
                    "category": "software"
            },
            {
                    "id": "ps-91",
                    "ps_id": "SIH26091",
                    "title": "AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-92",
                    "ps_id": "SIH26092",
                    "title": "AI-Driven Scheme Matching for Marginalized Entrepreneurs",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Driven Scheme Matching for Marginalized Entrepreneurs",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-93",
                    "ps_id": "SIH26093",
                    "title": "AI-Based Real-Time Stress and Trauma Assessment Module for Victims/Complainants Accessing NHAA (14566) and Integrated Portal",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Based Real-Time Stress and Trauma Assessment Module for Victims/Complainants Accessing NHAA (14566) and Integrated Portal",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-94",
                    "ps_id": "SIH26094",
                    "title": "AI-Powered Dynamic Mental Health Monitoring and Distress Prediction System for Victims of Atrocities",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Powered Dynamic Mental Health Monitoring and Distress Prediction System for Victims of Atrocities",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-95",
                    "ps_id": "SIH26095",
                    "title": "Smart Real-Time Monitoring & Inspection Mobile App",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - Smart Real-Time Monitoring & Inspection Mobile App",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-96",
                    "ps_id": "SIH26096",
                    "title": "Digital Heritage Archive for Memorials, Manuscripts & Ambedkar: AI-Powered Institutional Archive and Audio-Visual Knowledge Platform",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - Digital Heritage Archive for Memorials, Manuscripts & Ambedkar: AI-Powered Institutional Archive and Audio-Visual Knowledge Platform",
                    "theme": "Smart Education",
                    "category": "hardware"
            },
            {
                    "id": "ps-97",
                    "ps_id": "SIH26097",
                    "title": "AI-Driven voice Assistant for livelihood Mapping and NSQF-Aligned Skilling Recommendations for SC Communities under GIA component of PM-AJAY",
                    "description": "Ministry of Social Justice and Empowerment (MoSJE) - AI-Driven voice Assistant for livelihood Mapping and NSQF-Aligned Skilling Recommendations for SC Communities under GIA component of PM-AJAY",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-98",
                    "ps_id": "SIH26098",
                    "title": "Development of a Low-Cost Precision Guidance and Smart Electronic Fuze System for a 155 mm Artillery Shell",
                    "description": "Ministry of Defence (MoD) - Development of a Low-Cost Precision Guidance and Smart Electronic Fuze System for a 155 mm Artillery Shell",
                    "theme": "Smart Vehicles",
                    "category": "hardware"
            },
            {
                    "id": "ps-99",
                    "ps_id": "SIH26099",
                    "title": "AI-Driven Standardization and Harmonization of Material Codes Across CPSEs",
                    "description": "Ministry of Petroleum & Natural Gas - AI-Driven Standardization and Harmonization of Material Codes Across CPSEs",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-100",
                    "ps_id": "SIH26100",
                    "title": "AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement",
                    "description": "Ministry of Petroleum & Natural Gas - AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-101",
                    "ps_id": "SIH26101",
                    "title": "Develop an AI enabled learning platform that identifies competency gaps, recommends personalized training through integration with the iGOT Karmayogi ecosystem, and capable of generating Quizzes and Multiple choice questions (MCQs) from uploaded learning materials to strengthen capacity building in India's Official Statistical System.",
                    "description": "MoSPI - Develop an AI enabled learning platform that identifies competency gaps, recommends personalized training through integration with the iGOT Karmayogi ecosystem, and capable of generating Quizzes and Multiple choice questions (MCQs) from uploaded learning materials to strengthen capacity building in India's Official Statistical System.",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-102",
                    "ps_id": "SIH26102",
                    "title": "Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation regd.",
                    "description": "MoSPI - Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation regd.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-103",
                    "ps_id": "SIH26103",
                    "title": "Use case on web-based integrated project-monitoring platform",
                    "description": "MoSPI - Use case on web-based integrated project-monitoring platform",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-104",
                    "ps_id": "SIH26104",
                    "title": "AI-Powered Real-Time Detection and Prevention of Voice Cloning Impersonation Attacks",
                    "description": "All India Council for Technical Education (Cyber Security Cell) - AI-Powered Real-Time Detection and Prevention of Voice Cloning Impersonation Attacks",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-105",
                    "ps_id": "SIH26105",
                    "title": "AI-Powered Continuous Cyber Risk Quantification and Investment Optimization Platform",
                    "description": "All India Council for Technical Education (Cyber Security Cell) - AI-Powered Continuous Cyber Risk Quantification and Investment Optimization Platform",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-106",
                    "ps_id": "SIH26106",
                    "title": "AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform",
                    "description": "All India Council for Technical Education (Cyber Security Cell) - AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-107",
                    "ps_id": "SIH26107",
                    "title": "Al-powered Intelligent Assistant for Indian Standards and BIS Services for Industries and Consumers",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - Al-powered Intelligent Assistant for Indian Standards and BIS Services for Industries and Consumers",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-108",
                    "ps_id": "SIH26108",
                    "title": "AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications",
                    "description": "Ministry of Consumer Affairs, Food & Public Distribution - AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-109",
                    "ps_id": "SIH26109",
                    "title": "Al-Based Predictive Modelling for Early Forecasting of Bovine Mastitis in lndian Dairy Farms",
                    "description": "Ministry of Fisheries, Animal Husbandry & Dairying - Al-Based Predictive Modelling for Early Forecasting of Bovine Mastitis in lndian Dairy Farms",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-110",
                    "ps_id": "SIH26110",
                    "title": "Development of a Low-Cost Light-weight Milk Chilling Can for Small-Scale Dairy Farmers",
                    "description": "Ministry of Fisheries, Animal Husbandry & Dairying - Development of a Low-Cost Light-weight Milk Chilling Can for Small-Scale Dairy Farmers",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-111",
                    "ps_id": "SIH26111",
                    "title": "Smart Al-Enabled Rapid Feed and Silage Quality Testing System for Dairy Farmers",
                    "description": "Ministry of Fisheries, Animal Husbandry & Dairying - Smart Al-Enabled Rapid Feed and Silage Quality Testing System for Dairy Farmers",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-112",
                    "ps_id": "SIH26112",
                    "title": "Design and Develop a Modular Autonomous Mobile Robot (AMR) Platform for Smart Warehouse Automation",
                    "description": "Autodesk - Design and Develop a Modular Autonomous Mobile Robot (AMR) Platform for Smart Warehouse Automation",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-113",
                    "ps_id": "SIH26113",
                    "title": "Human augmentation technologies are transforming healthcare,rehabilitation, industrial ergonomics, assistive living, sports, and personal mobility by improving human capabilities and enhancing quality of life.",
                    "description": "Autodesk - Human augmentation technologies are transforming healthcare,rehabilitation, industrial ergonomics, assistive living, sports, and personal mobility by improving human capabilities and enhancing quality of life.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-114",
                    "ps_id": "SIH26114",
                    "title": "Smart City Site Planning using Autodesk Forma Site Design",
                    "description": "Autodesk - Smart City Site Planning using Autodesk Forma Site Design",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-115",
                    "ps_id": "SIH26115",
                    "title": "Design and Develop a Smart Mobile Medical-Waste Collection and Segregation System",
                    "description": "Autodesk - Design and Develop a Smart Mobile Medical-Waste Collection and Segregation System",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-116",
                    "ps_id": "SIH26116",
                    "title": "Urban Mixed-Use Design Challenge-Design a centrally located mixed-use building in Autodesk Revit with commercial spaces (Ground + 1st floor) and residential units (up to 8 floors). 1 Level of Basement (Car Parking + EV Charging), Total (B+G+9)(Note: Plot size and all required dimensions may be assumed by students (in mm units).",
                    "description": "Autodesk - Urban Mixed-Use Design Challenge-Design a centrally located mixed-use building in Autodesk Revit with commercial spaces (Ground + 1st floor) and residential units (up to 8 floors). 1 Level of Basement (Car Parking + EV Charging), Total (B+G+9)(Note: Plot size and all required dimensions may be assumed by students (in mm units).",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-117",
                    "ps_id": "SIH26117",
                    "title": "Sovereign On-Premise Agentic AI Workbench using Open-Weight Multimodal LLMs for Confidential Industrial Work",
                    "description": "Mangalore Refinery and Petrochemicals Limited (MRPL) - Sovereign On-Premise Agentic AI Workbench using Open-Weight Multimodal LLMs for Confidential Industrial Work",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-118",
                    "ps_id": "SIH26118",
                    "title": "Passive Colorimetric H2S Exposure-Dosimeter Wristband with AI-Based Quantitative Reading",
                    "description": "Mangalore Refinery and Petrochemicals Limited (MRPL) - Passive Colorimetric H2S Exposure-Dosimeter Wristband with AI-Based Quantitative Reading",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-119",
                    "ps_id": "SIH26119",
                    "title": "Indigenous GPU-Accelerated Optimization Solver (Sovereign Alternative to Express / CEPLEX)",
                    "description": "Mangalore Refinery and Petrochemicals Limited (MRPL) - Indigenous GPU-Accelerated Optimization Solver (Sovereign Alternative to Express / CEPLEX)",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-120",
                    "ps_id": "SIH26120",
                    "title": "Digital Twin for Well-to-Surface Optimization of Cyclic Steam Stimulation (CSS) and Sucker Rod Pump (SRP) Operations for Heavy Oil Wells of Baghewala Field.",
                    "description": "Oil India Limited - Digital Twin for Well-to-Surface Optimization of Cyclic Steam Stimulation (CSS) and Sucker Rod Pump (SRP) Operations for Heavy Oil Wells of Baghewala Field.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-121",
                    "ps_id": "SIH26121",
                    "title": "eRTMAC-NWIS (Nearby Wells Intelligence System): An AI-Powered Offset Well Knowledge and Decision Support Platform for Drilling Operations",
                    "description": "Oil India Limited - eRTMAC-NWIS (Nearby Wells Intelligence System): An AI-Powered Offset Well Knowledge and Decision Support Platform for Drilling Operations",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-122",
                    "ps_id": "SIH26122",
                    "title": "Intelligent Data Capture & Schedule-Linking Layer for Infrastructure Project Management: Real-Time Actual Progress Tracking (Planning-to-Execution Bridge)",
                    "description": "Oil India Limited - Intelligent Data Capture & Schedule-Linking Layer for Infrastructure Project Management: Real-Time Actual Progress Tracking (Planning-to-Execution Bridge)",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-123",
                    "ps_id": "SIH26123",
                    "title": "Edge-AI Based Distributed Fleet Coordination for Autonomous Mobile Robots (AMRs) in Smart Warehouses",
                    "description": "Bharat Electronics Limited - Edge-AI Based Distributed Fleet Coordination for Autonomous Mobile Robots (AMRs) in Smart Warehouses",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-124",
                    "ps_id": "SIH26124",
                    "title": "AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet",
                    "description": "Bharat Electronics Limited - AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-125",
                    "ps_id": "SIH26125",
                    "title": "Blockchain-Based Secure Platform for Identity,Access Control, and Digital Asset Management",
                    "description": "Bharat Electronics Limited - Blockchain-Based Secure Platform for Identity,Access Control, and Digital Asset Management",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-126",
                    "ps_id": "SIH26126",
                    "title": "Vision Based Autonomous Navigation for Unmanned Ground Vehicle for Outdoor environment",
                    "description": "Bharat Electronics Limited - Vision Based Autonomous Navigation for Unmanned Ground Vehicle for Outdoor environment",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-127",
                    "ps_id": "SIH26127",
                    "title": "City-Wide AI Engine for Multi-Camera ANPR Trajectory Tracking and Urban Traffic Analytics",
                    "description": "Bharat Electronics Limited - City-Wide AI Engine for Multi-Camera ANPR Trajectory Tracking and Urban Traffic Analytics",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-128",
                    "ps_id": "SIH26128",
                    "title": "Efficient systems for early detection,prevention,and management of livestock diseases and animal health issues",
                    "description": "Government Of Maharashtra - Efficient systems for early detection,prevention,and management of livestock diseases and animal health issues",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-129",
                    "ps_id": "SIH26129",
                    "title": "System integration and interoperability among government digital platforms,resulting in fragmented service delivery",
                    "description": "Government Of Maharashtra - System integration and interoperability among government digital platforms,resulting in fragmented service delivery",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-130",
                    "ps_id": "SIH26130",
                    "title": "Efficiency in streamlining industrial approvals,compliance processes,and access to government support services",
                    "description": "Government Of Maharashtra - Efficiency in streamlining industrial approvals,compliance processes,and access to government support services",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-131",
                    "ps_id": "SIH26131",
                    "title": "Early detection and management of crop diseases and pest infestations",
                    "description": "Government Of Maharashtra - Early detection and management of crop diseases and pest infestations",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-132",
                    "ps_id": "SIH26132",
                    "title": "Strengthening market linkages and price discovery for farmers",
                    "description": "Government Of Maharashtra - Strengthening market linkages and price discovery for farmers",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-133",
                    "ps_id": "SIH26133",
                    "title": "Accessibility and quality of public healthcare services,particularly in rural and underserved areas",
                    "description": "Government Of Maharashtra - Accessibility and quality of public healthcare services,particularly in rural and underserved areas",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-134",
                    "ps_id": "SIH26134",
                    "title": "Challenges in aligning skill development programs with industry requirements and emerging job market demands",
                    "description": "Government Of Maharashtra - Challenges in aligning skill development programs with industry requirements and emerging job market demands",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-135",
                    "ps_id": "SIH26135",
                    "title": "Difficulties in tracking employment outcomes,skill gaps, and the impact of skilling initiatives",
                    "description": "Government Of Maharashtra - Difficulties in tracking employment outcomes,skill gaps, and the impact of skilling initiatives",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-136",
                    "ps_id": "SIH26136",
                    "title": "Startup friendly public procurement mechanism that enables government departments to identify,pilot, procure,and scale innovative solutions from eligible startups",
                    "description": "Government Of Maharashtra - Startup friendly public procurement mechanism that enables government departments to identify,pilot, procure,and scale innovative solutions from eligible startups",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-137",
                    "ps_id": "SIH26137",
                    "title": "Quantum-Inspired Intelligent Traffic Route Optimization in Transportation Systems Using Metaheuristic Optimization",
                    "description": "Egreen Quanta - Quantum-Inspired Intelligent Traffic Route Optimization in Transportation Systems Using Metaheuristic Optimization",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-138",
                    "ps_id": "SIH26138",
                    "title": "Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization",
                    "description": "Egreen Quanta - Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization",
                    "theme": "Clean & Green Technology",
                    "category": "software"
            },
            {
                    "id": "ps-139",
                    "ps_id": "SIH26139",
                    "title": "Hybrid Quantum Machine Learning Platform for Early Disease Detection",
                    "description": "Egreen Quanta - Hybrid Quantum Machine Learning Platform for Early Disease Detection",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-140",
                    "ps_id": "SIH26140",
                    "title": "AI-Based Interactive Quantum Algorithm Learning Platform",
                    "description": "Egreen Quanta - AI-Based Interactive Quantum Algorithm Learning Platform",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-141",
                    "ps_id": "SIH26141",
                    "title": "Quantum-Inspired Cyber Threat Detection for Digital Signature Security",
                    "description": "Egreen Quanta - Quantum-Inspired Cyber Threat Detection for Digital Signature Security",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-142",
                    "ps_id": "SIH26142",
                    "title": "Deep Learning Based Super Resolution Mapping (SRM) from Medium Resolution Satellite Imageries",
                    "description": "National Technical Research Organisation (NTRO) - Deep Learning Based Super Resolution Mapping (SRM) from Medium Resolution Satellite Imageries",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-143",
                    "ps_id": "SIH26143",
                    "title": "Leveraging satellite imagery to determine Oil spills at sea along with AIS data correlations to identify vessel responsible for the spill.",
                    "description": "National Technical Research Organisation (NTRO) - Leveraging satellite imagery to determine Oil spills at sea along with AIS data correlations to identify vessel responsible for the spill.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-144",
                    "ps_id": "SIH26144",
                    "title": "Design & Development of a High-Sensitivity Micro barometer Infrasound sensor",
                    "description": "National Technical Research Organisation (NTRO) - Design & Development of a High-Sensitivity Micro barometer Infrasound sensor",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-145",
                    "ps_id": "SIH26145",
                    "title": "AI-Based Detection of Cyber Threats in Unidirectional IP Traffic",
                    "description": "National Technical Research Organisation (NTRO) - AI-Based Detection of Cyber Threats in Unidirectional IP Traffic",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-146",
                    "ps_id": "SIH26146",
                    "title": "AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic",
                    "description": "National Technical Research Organisation (NTRO) - AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-147",
                    "ps_id": "SIH26147",
                    "title": "Automated model for analysis of .IQ and .wav files along with signal parameter extraction",
                    "description": "National Technical Research Organisation (NTRO) - Automated model for analysis of .IQ and .wav files along with signal parameter extraction",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-148",
                    "ps_id": "SIH26148",
                    "title": "Creation of scripts/functions with new programming language to commence Computer & Network forensic analysis without triggering security solutions",
                    "description": "National Technical Research Organisation (NTRO) - Creation of scripts/functions with new programming language to commence Computer & Network forensic analysis without triggering security solutions",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-149",
                    "ps_id": "SIH26149",
                    "title": "Design and Development of an Integrated Secure Data Erasure and Advanced File Recovery Tool for Digital Forensics and Data Sanitization",
                    "description": "National Technical Research Organisation (NTRO) - Design and Development of an Integrated Secure Data Erasure and Advanced File Recovery Tool for Digital Forensics and Data Sanitization",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-150",
                    "ps_id": "SIH26150",
                    "title": "Development of a Multi-Vendor DVR/NVR Forensic Analysis Tool for Standardized Acquisition, Recovery, and Analysis of Surveillance Evidence.",
                    "description": "National Technical Research Organisation (NTRO) - Development of a Multi-Vendor DVR/NVR Forensic Analysis Tool for Standardized Acquisition, Recovery, and Analysis of Surveillance Evidence.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-151",
                    "ps_id": "SIH26151",
                    "title": "Dark web threat actor de-anonymization",
                    "description": "National Technical Research Organisation (NTRO) - Dark web threat actor de-anonymization",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-152",
                    "ps_id": "SIH26152",
                    "title": "Social Media Analytics",
                    "description": "National Technical Research Organisation (NTRO) - Social Media Analytics",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-153",
                    "ps_id": "SIH26153",
                    "title": "AI based Network Attack Forecasting from Network Traffic Data",
                    "description": "National Technical Research Organisation (NTRO) - AI based Network Attack Forecasting from Network Traffic Data",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-154",
                    "ps_id": "SIH26154",
                    "title": "Gen AI Platform for Automated Content Transformation",
                    "description": "National Technical Research Organisation (NTRO) - Gen AI Platform for Automated Content Transformation",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-155",
                    "ps_id": "SIH26155",
                    "title": "AI-Driven Multi-Vendor Network Security Compliance Auditor",
                    "description": "National Technical Research Organisation (NTRO) - AI-Driven Multi-Vendor Network Security Compliance Auditor",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-156",
                    "ps_id": "SIH26156",
                    "title": "Universal Log Pre-processing Framework",
                    "description": "National Technical Research Organisation (NTRO) - Universal Log Pre-processing Framework",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-157",
                    "ps_id": "SIH26157",
                    "title": "Supervisory Analytics Tool for SOC Assessment (SAT-SA)",
                    "description": "National Technical Research Organisation (NTRO) - Supervisory Analytics Tool for SOC Assessment (SAT-SA)",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-158",
                    "ps_id": "SIH26158",
                    "title": "Single-Pass Drone Video to Accurate 3D Model Generation System",
                    "description": "National Technical Research Organisation (NTRO) - Single-Pass Drone Video to Accurate 3D Model Generation System",
                    "theme": "Robotics and Drones",
                    "category": "software"
            },
            {
                    "id": "ps-159",
                    "ps_id": "SIH26159",
                    "title": "SecureMailScope: AI-Assisted Cryptographic Security Posture Assessment for Secure Email Communications",
                    "description": "National Technical Research Organisation (NTRO) - SecureMailScope: AI-Assisted Cryptographic Security Posture Assessment for Secure Email Communications",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-160",
                    "ps_id": "SIH26160",
                    "title": "AI-Powered IPsec VPN Protocol Analyzer and Security Assessment Framework",
                    "description": "National Technical Research Organisation (NTRO) - AI-Powered IPsec VPN Protocol Analyzer and Security Assessment Framework",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-161",
                    "ps_id": "SIH26161",
                    "title": "Dam Break Inundation Modelling Using Hydrodynamic Modelling of any River",
                    "description": "National Technical Research Organisation (NTRO) - Dam Break Inundation Modelling Using Hydrodynamic Modelling of any River",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-162",
                    "ps_id": "SIH26162",
                    "title": "AI-Based Detection and Classification of Industrial Fires and Persistent Thermal Sources Using NASA FIRMS, OSM & Satellite Data",
                    "description": "National Technical Research Organisation (NTRO) - AI-Based Detection and Classification of Industrial Fires and Persistent Thermal Sources Using NASA FIRMS, OSM & Satellite Data",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-163",
                    "ps_id": "SIH26163",
                    "title": "Security Assessment of the World Monitor application",
                    "description": "National Technical Research Organisation (NTRO) - Security Assessment of the World Monitor application",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-164",
                    "ps_id": "SIH26164",
                    "title": "Enterprise Cryptographic Discovery & Analysis Tool (ECDAT)",
                    "description": "National Technical Research Organisation (NTRO) - Enterprise Cryptographic Discovery & Analysis Tool (ECDAT)",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-165",
                    "ps_id": "SIH26165",
                    "title": "AI/NLP Engine to Detect Serious Injury & Fatality (SIF) Precursors in OIL's Unsafe-Act/Unsafe-Condition and Near-Miss Reports",
                    "description": "Oil India Limited - AI/NLP Engine to Detect Serious Injury & Fatality (SIF) Precursors in OIL's Unsafe-Act/Unsafe-Condition and Near-Miss Reports",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-166",
                    "ps_id": "SIH26166",
                    "title": "Multi-modal, Sun angle and scale invariant image correspondence using Chandrayaan-2 optical images (OHRC, TMC and IIRS)",
                    "description": "Indian Space Research Organisation(ISRO) - Multi-modal, Sun angle and scale invariant image correspondence using Chandrayaan-2 optical images (OHRC, TMC and IIRS)",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-167",
                    "ps_id": "SIH26167",
                    "title": "SatQuery AI - An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries",
                    "description": "Indian Space Research Organisation(ISRO) - SatQuery AI - An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-168",
                    "ps_id": "SIH26168",
                    "title": "AI-ML based Intelligent Dead Reckoning system for seamless navigation",
                    "description": "Indian Space Research Organisation(ISRO) - AI-ML based Intelligent Dead Reckoning system for seamless navigation",
                    "theme": "Smart Vehicles",
                    "category": "software"
            },
            {
                    "id": "ps-169",
                    "ps_id": "SIH26169",
                    "title": "Development of an AI-Based Virtual Camera Tracking System for Coarse Alignment of Mobile Free Space Optical Communication (FSOC) Terminals",
                    "description": "Indian Space Research Organisation(ISRO) - Development of an AI-Based Virtual Camera Tracking System for Coarse Alignment of Mobile Free Space Optical Communication (FSOC) Terminals",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-170",
                    "ps_id": "SIH26170",
                    "title": "AI-Driven Anomaly Detection in Component Burn-In & Screening",
                    "description": "Indian Space Research Organisation(ISRO) - AI-Driven Anomaly Detection in Component Burn-In & Screening",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-171",
                    "ps_id": "SIH26171",
                    "title": "On-device Visual Perception for Light-weight Browser Agents",
                    "description": "Indian Space Research Organisation(ISRO) - On-device Visual Perception for Light-weight Browser Agents",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-172",
                    "ps_id": "SIH26172",
                    "title": "Low Latency and Efficient Voice Activator for Edge Devices",
                    "description": "Indian Space Research Organisation(ISRO) - Low Latency and Efficient Voice Activator for Edge Devices",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-173",
                    "ps_id": "SIH26173",
                    "title": "iTantra -Indian Multilingual TTS & STT Aided Neural Transceiver Radio Access for low bitrate links",
                    "description": "Indian Space Research Organisation(ISRO) - iTantra -Indian Multilingual TTS & STT Aided Neural Transceiver Radio Access for low bitrate links",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-174",
                    "ps_id": "SIH26174",
                    "title": "AI Human Activity Recognition for On-board BAS Experiments",
                    "description": "Indian Space Research Organisation(ISRO) - AI Human Activity Recognition for On-board BAS Experiments",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-175",
                    "ps_id": "SIH26175",
                    "title": "DepthWizard - Single-View Height Estimation and 3D Flythrough",
                    "description": "Indian Space Research Organisation(ISRO) - DepthWizard - Single-View Height Estimation and 3D Flythrough",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-176",
                    "ps_id": "SIH26176",
                    "title": "ORCA Marine EcOsystem Reasoning with Collaborative Agents",
                    "description": "Indian Space Research Organisation(ISRO) - ORCA Marine EcOsystem Reasoning with Collaborative Agents",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-177",
                    "ps_id": "SIH26177",
                    "title": "A deployable AI-powered autonomous drone that aids search-and-rescue operations by detecting people and hazards, thereby improving responder safety and reducing victim discovery time.",
                    "description": "Qualcomm Inc - A deployable AI-powered autonomous drone that aids search-and-rescue operations by detecting people and hazards, thereby improving responder safety and reducing victim discovery time.",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-178",
                    "ps_id": "SIH26178",
                    "title": "A resilient, AI-powered environmental monitoring network that provides early detection, localized intelligence, and actionable alerts for floods, forest fires, pollution events, and other environmental hazards common in India, enabling authorities and communities to shift from reactive disaster response to proactive risk prevention.",
                    "description": "Qualcomm Inc - A resilient, AI-powered environmental monitoring network that provides early detection, localized intelligence, and actionable alerts for floods, forest fires, pollution events, and other environmental hazards common in India, enabling authorities and communities to shift from reactive disaster response to proactive risk prevention.",
                    "theme": "Disaster Management",
                    "category": "hardware"
            },
            {
                    "id": "ps-179",
                    "ps_id": "SIH26179",
                    "title": "To build an AI-powered retail intelligence platform that delivers real-time shopper analytics, automated inventory visibility, and proactive queue management through on-device AI,enabling retailers to reduce stock-outs, improve customer experience, optimize staffing, and increase operational efficiency while maintaining privacy and minimizing cloud dependency.",
                    "description": "Qualcomm Inc - To build an AI-powered retail intelligence platform that delivers real-time shopper analytics, automated inventory visibility, and proactive queue management through on-device AI,enabling retailers to reduce stock-outs, improve customer experience, optimize staffing, and increase operational efficiency while maintaining privacy and minimizing cloud dependency.",
                    "theme": "Miscellaneous",
                    "category": "hardware"
            },
            {
                    "id": "ps-180",
                    "ps_id": "SIH26180",
                    "title": "A field-deployable AI-powered Smart Farming Assistant that helps farmers detect crop diseases, pests, nutrient deficiencies, and irrigation needs at an early stage, while improving resilience against droughts, floods, heat waves, and other agricultural risks common in India. The solution should enable higher yields, lower input costs, more efficient water usage, and faster response to emerging threats through real-time on-device intelligence.",
                    "description": "Qualcomm Inc - A field-deployable AI-powered Smart Farming Assistant that helps farmers detect crop diseases, pests, nutrient deficiencies, and irrigation needs at an early stage, while improving resilience against droughts, floods, heat waves, and other agricultural risks common in India. The solution should enable higher yields, lower input costs, more efficient water usage, and faster response to emerging threats through real-time on-device intelligence.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-181",
                    "ps_id": "SIH26181",
                    "title": "A secure, AI-powered Personal Health Companion that delivers real-time, privacy-preserving health monitoring and early warning capabilities, helping individuals recognize health risks before they become emergencies. The solution should improve resilience during heat waves, floods, pollution events, and other disasters common in India while enabling continuous health support through on-device intelligence.",
                    "description": "Qualcomm Inc - A secure, AI-powered Personal Health Companion that delivers real-time, privacy-preserving health monitoring and early warning capabilities, helping individuals recognize health risks before they become emergencies. The solution should improve resilience during heat waves, floods, pollution events, and other disasters common in India while enabling continuous health support through on-device intelligence.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-182",
                    "ps_id": "SIH26182",
                    "title": "Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs",
                    "description": "Ministry of Home Affairs - Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-183",
                    "ps_id": "SIH26183",
                    "title": "Real-Time Identification of Fraud-Linked Cryptocurrency Exchanges from Victim-Reported Suspect Wallet Addresses through Automated Blockchain Analytics",
                    "description": "Ministry of Home Affairs - Real-Time Identification of Fraud-Linked Cryptocurrency Exchanges from Victim-Reported Suspect Wallet Addresses through Automated Blockchain Analytics",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-184",
                    "ps_id": "SIH26184",
                    "title": "Development of a Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance, Enabling Generation of Actionable Intelligence for Timely and Proactive Cybercrime Intervention.",
                    "description": "Ministry of Home Affairs - Development of a Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance, Enabling Generation of Actionable Intelligence for Timely and Proactive Cybercrime Intervention.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-185",
                    "ps_id": "SIH26185",
                    "title": "Helmet mounted conformal antenna for tactical communications in urban CQB environments.",
                    "description": "Ministry of Home Affairs - Helmet mounted conformal antenna for tactical communications in urban CQB environments.",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-186",
                    "ps_id": "SIH26186",
                    "title": "AI-Based Predictive Personnel Stress and Welfare Monitoring System for Uniformed Forces",
                    "description": "Ministry of Home Affairs - AI-Based Predictive Personnel Stress and Welfare Monitoring System for Uniformed Forces",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-187",
                    "ps_id": "SIH26187",
                    "title": "AI-Based Intelligent Video Analytics Platform for Border Surveillance using existing CCTV Infrastructure.",
                    "description": "Ministry of Home Affairs - AI-Based Intelligent Video Analytics Platform for Border Surveillance using existing CCTV Infrastructure.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-188",
                    "ps_id": "SIH26188",
                    "title": "Al-Based Fake Identity & Document Screening System",
                    "description": "Ministry of Home Affairs - Al-Based Fake Identity & Document Screening System",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-189",
                    "ps_id": "SIH26189",
                    "title": "AI-Powered Criminal Network Analysis System",
                    "description": "Ministry of Home Affairs - AI-Powered Criminal Network Analysis System",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-190",
                    "ps_id": "SIH26190",
                    "title": "Secure Digital Document Management System for Legal and Investigation Documents",
                    "description": "Ministry of Home Affairs - Secure Digital Document Management System for Legal and Investigation Documents",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-191",
                    "ps_id": "SIH26191",
                    "title": "Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations",
                    "description": "Ministry of Home Affairs - Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-192",
                    "ps_id": "SIH26192",
                    "title": "Flash Flood Prediction System for Hilly Regions using Multi-Source Data Theme",
                    "description": "Ministry of Home Affairs - Flash Flood Prediction System for Hilly Regions using Multi-Source Data Theme",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-193",
                    "ps_id": "SIH26193",
                    "title": "Student Innovation-Developing solutions, keeping in mind the need to enhance the primary sector of India - Agriculture and to manage and process our agriculture produce.",
                    "description": "AICTE - Student Innovation-Developing solutions, keeping in mind the need to enhance the primary sector of India - Agriculture and to manage and process our agriculture produce.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-194",
                    "ps_id": "SIH26194",
                    "title": "Student Innovation-Provide ideas in a decentralized and distributed ledger technology used to store digital information that powers cryptocurrencies and NFTs and can radically change multiple sectors.",
                    "description": "AICTE - Student Innovation-Provide ideas in a decentralized and distributed ledger technology used to store digital information that powers cryptocurrencies and NFTs and can radically change multiple sectors.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-195",
                    "ps_id": "SIH26195",
                    "title": "Student Innovation-Solutions could be in the form of waste segregation, disposal, and improve sanitization system.",
                    "description": "AICTE - Student Innovation-Solutions could be in the form of waste segregation, disposal, and improve sanitization system.",
                    "theme": "Clean & Green Technology",
                    "category": "software"
            },
            {
                    "id": "ps-196",
                    "ps_id": "SIH26196",
                    "title": "Student Innovation-Ideas that can boost fitness activities and assist in keeping fit.",
                    "description": "AICTE - Student Innovation-Ideas that can boost fitness activities and assist in keeping fit.",
                    "theme": "Fitness & Sports",
                    "category": "software"
            },
            {
                    "id": "ps-197",
                    "ps_id": "SIH26197",
                    "title": "Student Innovation-Ideas that showcase the rich cultural heritage and traditions of India.",
                    "description": "AICTE - Student Innovation-Ideas that showcase the rich cultural heritage and traditions of India.",
                    "theme": "Heritage & Culture",
                    "category": "software"
            },
            {
                    "id": "ps-198",
                    "ps_id": "SIH26198",
                    "title": "Student Innovation-Cutting-edge technology in these sectors continues to be in demand. Recent shifts in healthcare trends, growing populations also present an array of opportunities for innovation.",
                    "description": "AICTE - Student Innovation-Cutting-edge technology in these sectors continues to be in demand. Recent shifts in healthcare trends, growing populations also present an array of opportunities for innovation.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-199",
                    "ps_id": "SIH26199",
                    "title": "Student Innovation-Technology ideas in tertiary sectors like Hospitality, Financial Services, Entertainment and Retail.",
                    "description": "AICTE - Student Innovation-Technology ideas in tertiary sectors like Hospitality, Financial Services, Entertainment and Retail.",
                    "theme": "Miscellaneous",
                    "category": "software"
            },
            {
                    "id": "ps-200",
                    "ps_id": "SIH26200",
                    "title": "Student Innovation-Innovative ideas that help manage and generate renewable /sustainable sources more efficiently",
                    "description": "AICTE - Student Innovation-Innovative ideas that help manage and generate renewable /sustainable sources more efficiently",
                    "theme": "Renewable / Sustainable Energy",
                    "category": "software"
            },
            {
                    "id": "ps-201",
                    "ps_id": "SIH26201",
                    "title": "Student Innovation-There is a need to design drones and robots that can solve some of the pressing challenges of India such as handling medical emergencies, search and rescue operations, etc.",
                    "description": "AICTE - Student Innovation-There is a need to design drones and robots that can solve some of the pressing challenges of India such as handling medical emergencies, search and rescue operations, etc.",
                    "theme": "Robotics and Drones",
                    "category": "software"
            },
            {
                    "id": "ps-202",
                    "ps_id": "SIH26202",
                    "title": "Student Innovation-Ideas focused on the intelligent use of resources for transforming and advancements of technology with combining the artificial intelligence to explore more various sources and get valuable insights.",
                    "description": "AICTE - Student Innovation-Ideas focused on the intelligent use of resources for transforming and advancements of technology with combining the artificial intelligence to explore more various sources and get valuable insights.",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-203",
                    "ps_id": "SIH26203",
                    "title": "Student Innovation-Creating intelligent devices to improve commutation sector.",
                    "description": "AICTE - Student Innovation-Creating intelligent devices to improve commutation sector.",
                    "theme": "Smart Vehicles",
                    "category": "software"
            },
            {
                    "id": "ps-204",
                    "ps_id": "SIH26204",
                    "title": "Student Innovation-A solution/idea that can boost the current situation of the tourism industries including hotels, travel and others.",
                    "description": "AICTE - Student Innovation-A solution/idea that can boost the current situation of the tourism industries including hotels, travel and others.",
                    "theme": "Travel & Tourism",
                    "category": "software"
            },
            {
                    "id": "ps-205",
                    "ps_id": "SIH26205",
                    "title": "Student Innovation-Submit your ideas to address the growing pressures on the city\u2019s resources, transport networks, and logistic infrastructure.",
                    "description": "AICTE - Student Innovation-Submit your ideas to address the growing pressures on the city\u2019s resources, transport networks, and logistic infrastructure.",
                    "theme": "Transportation & Logistics",
                    "category": "software"
            },
            {
                    "id": "ps-206",
                    "ps_id": "SIH26206",
                    "title": "Student Innovation-Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.",
                    "description": "AICTE - Student Innovation-Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.",
                    "theme": "Disaster Management",
                    "category": "software"
            },
            {
                    "id": "ps-207",
                    "ps_id": "SIH26207",
                    "title": "Student Innovation-Smart education,a concept that describes learning in digital age. It enables learners to learn more effectively, efficiently, flexibly and comfortably.",
                    "description": "AICTE - Student Innovation-Smart education,a concept that describes learning in digital age. It enables learners to learn more effectively, efficiently, flexibly and comfortably.",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-208",
                    "ps_id": "SIH26208",
                    "title": "Student Innovation-Challenge your creative mind to conceptualize and develop unique toys and games based on our civilization, history, and culture etc.",
                    "description": "AICTE - Student Innovation-Challenge your creative mind to conceptualize and develop unique toys and games based on our civilization, history, and culture etc.",
                    "theme": "Toys & Games",
                    "category": "software"
            },
            {
                    "id": "ps-209",
                    "ps_id": "SIH26209",
                    "title": "Student Innovation-Space technology refers to the application of engineering principles to the design, development, manufacture, and operation of devices and systems for space travel and exploration.",
                    "description": "AICTE - Student Innovation-Space technology refers to the application of engineering principles to the design, development, manufacture, and operation of devices and systems for space travel and exploration.",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-210",
                    "ps_id": "SIH26210",
                    "title": "Student Innovation-Developing solutions, keeping in mind the need to enhance the primary sector of India - Agriculture and to manage and process our agriculture produce.",
                    "description": "AICTE - Student Innovation-Developing solutions, keeping in mind the need to enhance the primary sector of India - Agriculture and to manage and process our agriculture produce.",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-211",
                    "ps_id": "SIH26211",
                    "title": "Student Innovation-Provide ideas in a decentralized and distributed ledger technology used to store digital information that powers cryptocurrencies and NFTs and can radically change multiple sectors.",
                    "description": "AICTE - Student Innovation-Provide ideas in a decentralized and distributed ledger technology used to store digital information that powers cryptocurrencies and NFTs and can radically change multiple sectors.",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "hardware"
            },
            {
                    "id": "ps-212",
                    "ps_id": "SIH26212",
                    "title": "Student Innovation-Solutions could be in the form of waste segregation, disposal, and improve sanitization system.",
                    "description": "AICTE - Student Innovation-Solutions could be in the form of waste segregation, disposal, and improve sanitization system.",
                    "theme": "Clean & Green Technology",
                    "category": "hardware"
            },
            {
                    "id": "ps-213",
                    "ps_id": "SIH26213",
                    "title": "Student Innovation-Ideas that can boost fitness activities and assist in keeping fit.",
                    "description": "AICTE - Student Innovation-Ideas that can boost fitness activities and assist in keeping fit.",
                    "theme": "Fitness & Sports",
                    "category": "hardware"
            },
            {
                    "id": "ps-214",
                    "ps_id": "SIH26214",
                    "title": "Student Innovation-Ideas that showcase the rich cultural heritage and traditions of India.",
                    "description": "AICTE - Student Innovation-Ideas that showcase the rich cultural heritage and traditions of India.",
                    "theme": "Heritage & Culture",
                    "category": "hardware"
            },
            {
                    "id": "ps-215",
                    "ps_id": "SIH26215",
                    "title": "Student Innovation-Cutting-edge technology in these sectors continues to be in demand. Recent shifts in healthcare trends, growing populations also present an array of opportunities for innovation.",
                    "description": "AICTE - Student Innovation-Cutting-edge technology in these sectors continues to be in demand. Recent shifts in healthcare trends, growing populations also present an array of opportunities for innovation.",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-216",
                    "ps_id": "SIH26216",
                    "title": "Student Innovation-Technology ideas in tertiary sectors like Hospitality, Financial Services, Entertainment and Retail.",
                    "description": "AICTE - Student Innovation-Technology ideas in tertiary sectors like Hospitality, Financial Services, Entertainment and Retail.",
                    "theme": "Miscellaneous",
                    "category": "hardware"
            },
            {
                    "id": "ps-217",
                    "ps_id": "SIH26217",
                    "title": "Student Innovation-Innovative ideas that help manage and generate renewable /sustainable sources more efficiently",
                    "description": "AICTE - Student Innovation-Innovative ideas that help manage and generate renewable /sustainable sources more efficiently",
                    "theme": "Renewable / Sustainable Energy",
                    "category": "hardware"
            },
            {
                    "id": "ps-218",
                    "ps_id": "SIH26218",
                    "title": "Student Innovation-There is a need to design drones and robots that can solve some of the pressing challenges of India such as handling medical emergencies, search and rescue operations, etc.",
                    "description": "AICTE - Student Innovation-There is a need to design drones and robots that can solve some of the pressing challenges of India such as handling medical emergencies, search and rescue operations, etc.",
                    "theme": "Robotics and Drones",
                    "category": "hardware"
            },
            {
                    "id": "ps-219",
                    "ps_id": "SIH26219",
                    "title": "Student Innovation-Ideas focused on the intelligent use of resources for transforming and advancements of technology with combining the artificial intelligence to explore more various sources and get valuable insights.",
                    "description": "AICTE - Student Innovation-Ideas focused on the intelligent use of resources for transforming and advancements of technology with combining the artificial intelligence to explore more various sources and get valuable insights.",
                    "theme": "Smart Automation",
                    "category": "hardware"
            },
            {
                    "id": "ps-220",
                    "ps_id": "SIH26220",
                    "title": "Student Innovation-Creating intelligent devices to improve commutation sector.",
                    "description": "AICTE - Student Innovation-Creating intelligent devices to improve commutation sector.",
                    "theme": "Smart Vehicles",
                    "category": "hardware"
            },
            {
                    "id": "ps-221",
                    "ps_id": "SIH26221",
                    "title": "Student Innovation-A solution/idea that can boost the current situation of the tourism industries including hotels, travel and others.",
                    "description": "AICTE - Student Innovation-A solution/idea that can boost the current situation of the tourism industries including hotels, travel and others.",
                    "theme": "Travel & Tourism",
                    "category": "hardware"
            },
            {
                    "id": "ps-222",
                    "ps_id": "SIH26222",
                    "title": "Student Innovation-Submit your ideas to address the growing pressures on the city\u2019s resources, transport networks, and logistic infrastructure.",
                    "description": "AICTE - Student Innovation-Submit your ideas to address the growing pressures on the city\u2019s resources, transport networks, and logistic infrastructure.",
                    "theme": "Transportation & Logistics",
                    "category": "hardware"
            },
            {
                    "id": "ps-223",
                    "ps_id": "SIH26223",
                    "title": "Student Innovation-Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.",
                    "description": "AICTE - Student Innovation-Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.",
                    "theme": "Disaster Management",
                    "category": "hardware"
            },
            {
                    "id": "ps-224",
                    "ps_id": "SIH26224",
                    "title": "Student Innovation-Smart education,a concept that describes learning in digital age. It enables learners to learn more effectively, efficiently, flexibly and comfortably.",
                    "description": "AICTE - Student Innovation-Smart education,a concept that describes learning in digital age. It enables learners to learn more effectively, efficiently, flexibly and comfortably.",
                    "theme": "Smart Education",
                    "category": "hardware"
            },
            {
                    "id": "ps-225",
                    "ps_id": "SIH26225",
                    "title": "Student Innovation-Challenge your creative mind to conceptualize and develop unique toys and games based on our civilization, history, and culture etc.",
                    "description": "AICTE - Student Innovation-Challenge your creative mind to conceptualize and develop unique toys and games based on our civilization, history, and culture etc.",
                    "theme": "Toys & Games",
                    "category": "hardware"
            },
            {
                    "id": "ps-226",
                    "ps_id": "SIH26226",
                    "title": "Student Innovation-Space technology refers to the application of engineering principles to the design, development, manufacture, and operation of devices and systems for space travel and exploration.",
                    "description": "AICTE - Student Innovation-Space technology refers to the application of engineering principles to the design, development, manufacture, and operation of devices and systems for space travel and exploration.",
                    "theme": "Space Technology",
                    "category": "hardware"
            },
            {
                    "id": "ps-227",
                    "ps_id": "SIH26227",
                    "title": "Semantic Retrieval and Multi-Temporal Change Analysis of Satellite lmagery.",
                    "description": "Ministry of defence (MoD) - Semantic Retrieval and Multi-Temporal Change Analysis of Satellite lmagery.",
                    "theme": "Space Technology",
                    "category": "software"
            },
            {
                    "id": "ps-228",
                    "ps_id": "SIH26228",
                    "title": "Trustworthy Computer Vision Integrity Assurance for Data, Models and Inference Outputs in Multi-Contributor Pipelines",
                    "description": "Ministry of defence (MoD) - Trustworthy Computer Vision Integrity Assurance for Data, Models and Inference Outputs in Multi-Contributor Pipelines",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-229",
                    "ps_id": "SIH26229",
                    "title": "Kabadiwala Connect \u2013 Bringing the Informal Collector into the Formal Recycling Chain",
                    "description": "Ministry of Mines (MoM) - Kabadiwala Connect \u2013 Bringing the Informal Collector into the Formal Recycling Chain",
                    "theme": "Clean & Green Technology",
                    "category": "software"
            },
            {
                    "id": "ps-230",
                    "ps_id": "SIH26230",
                    "title": "Breath-Based Detection Device for Drug Consumption",
                    "description": "Ministry of Home Affairs - Breath-Based Detection Device for Drug Consumption",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "hardware"
            },
            {
                    "id": "ps-231",
                    "ps_id": "SIH26231",
                    "title": "Digital Companion for Field Drug Testing",
                    "description": "Ministry of Home Affairs - Digital Companion for Field Drug Testing",
                    "theme": "MedTech / BioTech / HealthTech",
                    "category": "software"
            },
            {
                    "id": "ps-232",
                    "ps_id": "SIH26232",
                    "title": "Low-Cost loT Block chain Nodes for Farm-to-Fork Traceability",
                    "description": "Ministry of Food Processing Industries (MoFPI) - Low-Cost loT Block chain Nodes for Farm-to-Fork Traceability",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-233",
                    "ps_id": "SIH26233",
                    "title": "Inline Microbial Contamination Detection Using Hyperspectral Edge Sensors",
                    "description": "Ministry of Food Processing Industries (MoFPI) - Inline Microbial Contamination Detection Using Hyperspectral Edge Sensors",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-234",
                    "ps_id": "SIH26234",
                    "title": "Al-Powered Smart Food Waste Reduction and Sustainable Redistribution Ecosystem for Institutional Kitchens and Food Processing Units",
                    "description": "Ministry of Food Processing Industries (MoFPI) - Al-Powered Smart Food Waste Reduction and Sustainable Redistribution Ecosystem for Institutional Kitchens and Food Processing Units",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-235",
                    "ps_id": "SIH26235",
                    "title": "Development of a Portable Nano engineered Rapid Food Testing Kit for On-Site Detection of Food Adulterants and Contaminants",
                    "description": "Ministry of Food Processing Industries (MoFPI) - Development of a Portable Nano engineered Rapid Food Testing Kit for On-Site Detection of Food Adulterants and Contaminants",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "hardware"
            },
            {
                    "id": "ps-236",
                    "ps_id": "SIH26236",
                    "title": "Al-Based Intelligent Food Packaging Material Recommendation System for Food Commodities",
                    "description": "Ministry of Food Processing Industries (MoFPI) - Al-Based Intelligent Food Packaging Material Recommendation System for Food Commodities",
                    "theme": "Agriculture, FoodTech & Rural Development",
                    "category": "software"
            },
            {
                    "id": "ps-237",
                    "ps_id": "SIH26237",
                    "title": "Cryptographic Attribution and Immutable Decryption Provenance for Multi-Recipient Encrypted Document Distribution",
                    "description": "Ministry of Defence - Cryptographic Attribution and Immutable Decryption Provenance for Multi-Recipient Encrypted Document Distribution",
                    "theme": "Blockchain & Cybersecurity",
                    "category": "software"
            },
            {
                    "id": "ps-238",
                    "ps_id": "SIH26238",
                    "title": "Unified Scholarship Mobile Application for Tribal Students",
                    "description": "Ministry of Tribal Affairs - Unified Scholarship Mobile Application for Tribal Students",
                    "theme": "Smart Automation",
                    "category": "software"
            },
            {
                    "id": "ps-239",
                    "ps_id": "SIH26239",
                    "title": "AI-Enabled Scholarship and Fellowship Management System for Scheduled Tribes",
                    "description": "Ministry of Tribal Affairs - AI-Enabled Scholarship and Fellowship Management System for Scheduled Tribes",
                    "theme": "Smart Education",
                    "category": "software"
            },
            {
                    "id": "ps-240",
                    "ps_id": "SIH26240",
                    "title": "AI-Based Spring Revival and Recharge Planning for Tribal Areas",
                    "description": "Ministry of Tribal Affairs - AI-Based Spring Revival and Recharge Planning for Tribal Areas",
                    "theme": "Agriculture, FoodTech & Rural Development",
            }
    ],
    "submissions": {},
    "reports": {}
}

class DBManager:
    @classmethod
    def get_problem_statements(cls, query: Optional[str] = None) -> List[Dict[str, Any]]:
        ps_list = IN_MEMORY_DB["problem_statements"]
        if query:
            q = query.lower()
            return [
                ps for ps in ps_list 
                if q in ps["ps_id"].lower() or q in ps["title"].lower() or q in ps["theme"].lower()
            ]
        return ps_list

    @classmethod
    def get_problem_statement_by_id(cls, ps_id: str) -> Optional[Dict[str, Any]]:
        for ps in IN_MEMORY_DB["problem_statements"]:
            if ps["id"] == ps_id or ps["ps_id"].lower() == ps_id.lower():
                return ps
        return None

    @classmethod
    def create_submission(cls, file_name: str, file_type: str, ps_id: Optional[str]) -> Dict[str, Any]:
        sub_id = str(uuid.uuid4())
        record = {
            "id": sub_id,
            "file_name": file_name,
            "file_type": file_type,
            "ps_id": ps_id,
            "status": "queued",
            "progress_step": "Queued for parsing...",
            "progress_pct": 10,
            "created_at": datetime.now().isoformat()
        }
        IN_MEMORY_DB["submissions"][sub_id] = record
        return record

    @classmethod
    def update_submission_status(cls, sub_id: str, status: str, step: str, pct: int):
        if sub_id in IN_MEMORY_DB["submissions"]:
            IN_MEMORY_DB["submissions"][sub_id]["status"] = status
            IN_MEMORY_DB["submissions"][sub_id]["progress_step"] = step
            IN_MEMORY_DB["submissions"][sub_id]["progress_pct"] = pct

    @classmethod
    def save_report(cls, sub_id: str, report_data: Dict[str, Any]):
        IN_MEMORY_DB["reports"][sub_id] = report_data
        cls.update_submission_status(sub_id, "completed", "Report finalized", 100)

    @classmethod
    def get_submission(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        return IN_MEMORY_DB["submissions"].get(sub_id)

    @classmethod
    def get_report(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        return IN_MEMORY_DB["reports"].get(sub_id)

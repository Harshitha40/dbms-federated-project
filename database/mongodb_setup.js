// ========================================
// FEDERATED ENVIRONMENTAL INTELLIGENCE PLATFORM
// MongoDB Collections Setup
// ========================================

// Switch to environmental_db database
//use environmental_db;

// ========================================
// COLLECTION 1: Biodiversity_Data
// Purpose: Store species diversity information per region
// ========================================
db.Biodiversity_Data.insertMany([
    {
        biodiversity_id: "BIO001",
        region_id: 1,
        region_name: "Amazon Basin",
        species_count: 40000,
        endangered_species: ["Jaguar", "Harpy Eagle", "Giant Otter"],
        dominant_flora: ["Brazil Nut Tree", "Kapok Tree", "Rubber Tree"],
        conservation_status: "Critical",
        last_survey_date: new Date("2024-01-10")
    },
    {
        biodiversity_id: "BIO002",
        region_id: 2,
        region_name: "Great Barrier Reef",
        species_count: 9000,
        endangered_species: ["Green Sea Turtle", "Dugong", "Whale Shark"],
        dominant_flora: ["Hard Coral", "Soft Coral", "Seagrass"],
        conservation_status: "Endangered",
        last_survey_date: new Date("2024-01-15")
    },
    {
        biodiversity_id: "BIO003",
        region_id: 5,
        region_name: "Congo Rainforest",
        species_count: 10000,
        endangered_species: ["Mountain Gorilla", "Forest Elephant", "Okapi"],
        dominant_flora: ["African Mahogany", "Ebony Tree", "Teak"],
        conservation_status: "Critical",
        last_survey_date: new Date("2023-12-20")
    },
    {
        biodiversity_id: "BIO004",
        region_id: 8,
        region_name: "Madagascar",
        species_count: 12000,
        endangered_species: ["Lemur", "Fossa", "Madagascar Fish Eagle"],
        dominant_flora: ["Baobab Tree", "Traveller's Palm", "Octopus Tree"],
        conservation_status: "Critical",
        last_survey_date: new Date("2024-02-01")
    }
]);

// ========================================
// COLLECTION 2: Sensor_Logs
// Purpose: Real-time sensor event logs
// ========================================
db.Sensor_Logs.insertMany([
    {
        log_id: "LOG001",
        sensor_id: "SENS_001",
        region_id: 1,
        event_type: "temperature_spike",
        severity: "warning",
        message: "Temperature exceeded threshold by 2.5°C",
        timestamp: new Date("2024-03-15T14:23:45Z")
    },
    {
        log_id: "LOG002",
        sensor_id: "SENS_003",
        region_id: 3,
        event_type: "humidity_drop",
        severity: "critical",
        message: "Humidity dropped below 10%",
        timestamp: new Date("2024-03-15T16:45:22Z")
    },
    {
        log_id: "LOG003",
        sensor_id: "SENS_005",
        region_id: 5,
        event_type: "rainfall_heavy",
        severity: "info",
        message: "Heavy rainfall detected: 150mm in 24hrs",
        timestamp: new Date("2024-03-16T08:12:33Z")
    },
    {
        log_id: "LOG004",
        sensor_id: "SENS_007",
        region_id: 7,
        event_type: "air_quality_degraded",
        severity: "warning",
        message: "PM2.5 levels increased by 40%",
        timestamp: new Date("2024-03-16T11:30:15Z")
    },
    {
        log_id: "LOG005",
        sensor_id: "SENS_002",
        region_id: 2,
        event_type: "water_temperature_change",
        severity: "warning",
        message: "Ocean temperature rising - coral bleaching risk",
        timestamp: new Date("2024-03-16T13:22:50Z")
    }
]);

// ========================================
// COLLECTION 3: Air_Quality_History
// Purpose: Historical air quality measurements
// ========================================
db.Air_Quality_History.insertMany([
    {
        reading_id: "AQ001",
        region_id: 1,
        aqi: 45,
        pollutants: {
            co2: 410,
            pm2_5: 12.3,
            pm10: 25.8,
            no2: 15.2,
            so2: 8.5,
            o3: 55.3
        },
        air_quality_level: "Good",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ002",
        region_id: 3,
        aqi: 180,
        pollutants: {
            co2: 450,
            pm2_5: 85.6,
            pm10: 120.4,
            no2: 42.1,
            so2: 35.8,
            o3: 95.2
        },
        air_quality_level: "Unhealthy",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ003",
        region_id: 7,
        aqi: 95,
        pollutants: {
            co2: 425,
            pm2_5: 35.2,
            pm10: 58.9,
            no2: 28.5,
            so2: 18.3,
            o3: 72.1
        },
        air_quality_level: "Moderate",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ004",
        region_id: 4,
        aqi: 25,
        pollutants: {
            co2: 390,
            pm2_5: 5.2,
            pm10: 12.1,
            no2: 6.8,
            so2: 3.2,
            o3: 42.5
        },
        air_quality_level: "Excellent",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ005",
        region_id: 9,   // Patagonia
        aqi: 32,
        pollutants: {
            co2: 395,
            pm2_5: 6.8,
            pm10: 14.5,
            no2: 7.2,
            so2: 4.1,
            o3: 48.9
        },
        air_quality_level: "Excellent",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ006",
        region_id: 13,  // Sundarbans
        aqi: 115,
        pollutants: {
            co2: 430,
            pm2_5: 42.7,
            pm10: 65.3,
            no2: 30.6,
            so2: 22.8,
            o3: 78.4
        },
        air_quality_level: "Moderate",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ007",
        region_id: 14,  // Borneo Rainforest
        aqi: 58,
        pollutants: {
            co2: 405,
            pm2_5: 14.9,
            pm10: 28.6,
            no2: 12.4,
            so2: 9.6,
            o3: 60.7
        },
        air_quality_level: "Good",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ008",
        region_id: 16,  // Atacama Desert
        aqi: 22,
        pollutants: {
            co2: 385,
            pm2_5: 4.1,
            pm10: 9.8,
            no2: 5.3,
            so2: 2.6,
            o3: 40.2
        },
        air_quality_level: "Excellent",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    },
    {
        reading_id: "AQ009",
        region_id: 20,  // Okavango Delta
        aqi: 78,
        pollutants: {
            co2: 420,
            pm2_5: 26.4,
            pm10: 44.9,
            no2: 20.1,
            so2: 14.7,
            o3: 69.3
        },
        air_quality_level: "Good",
        recorded_at: new Date("2024-03-01T00:00:00Z")
    }
]);

// ========================================
// COLLECTION 4: Species_Details
// Purpose: Detailed information about specific species
// ========================================
db.Species_Details.insertMany([
    {
        species_id: "SP001",
        common_name: "Jaguar",
        scientific_name: "Panthera onca",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Mammalia",
            order: "Carnivora",
            family: "Felidae"
        },
        habitat_regions: [1, 5],
        population_estimate: 64000,
        conservation_status: "Near Threatened",
        threats: ["Habitat Loss", "Poaching", "Human Conflict"],
        diet: "Carnivore",
        lifespan_years: 15
    },
    {
        species_id: "SP002",
        common_name: "Green Sea Turtle",
        scientific_name: "Chelonia mydas",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Reptilia",
            order: "Testudines",
            family: "Cheloniidae"
        },
        habitat_regions: [2],
        population_estimate: 85000,
        conservation_status: "Endangered",
        threats: ["Climate Change", "Pollution", "Fishing Nets"],
        diet: "Herbivore",
        lifespan_years: 80
    },
    {
        species_id: "SP003",
        common_name: "Mountain Gorilla",
        scientific_name: "Gorilla beringei beringei",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Mammalia",
            order: "Primates",
            family: "Hominidae"
        },
        habitat_regions: [5],
        population_estimate: 1063,
        conservation_status: "Endangered",
        threats: ["Habitat Loss", "Disease", "Poaching"],
        diet: "Herbivore",
        lifespan_years: 40
    },
    {
        species_id: "SP004",
        common_name: "Lemur",
        scientific_name: "Lemur catta",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Mammalia",
            order: "Primates",
            family: "Lemuridae"
        },
        habitat_regions: [8],
        population_estimate: 2000,
        conservation_status: "Endangered",
        threats: ["Deforestation", "Hunting", "Pet Trade"],
        diet: "Omnivore",
        lifespan_years: 18
    },
    {
        species_id: "SP005",
        common_name: "Andean Condor",
        scientific_name: "Vultur gryphus",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Aves",
            order: "Cathartiformes",
            family: "Cathartidae"
        },
        habitat_regions: [10, 19],
        population_estimate: 6700,
        conservation_status: "Vulnerable",
        threats: ["Poisoning", "Habitat Degradation", "Human Conflict"],
        diet: "Carnivore",
        lifespan_years: 50
    },
    {
        species_id: "SP006",
        common_name: "Snow Leopard",
        scientific_name: "Panthera uncia",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Mammalia",
            order: "Carnivora",
            family: "Felidae"
        },
        habitat_regions: [6, 19],
        population_estimate: 4500,
        conservation_status: "Vulnerable",
        threats: ["Poaching", "Climate Change", "Prey Loss"],
        diet: "Carnivore",
        lifespan_years: 20
    },
    {
        species_id: "SP007",
        common_name: "African Wild Dog",
        scientific_name: "Lycaon pictus",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Mammalia",
            order: "Carnivora",
            family: "Canidae"
        },
        habitat_regions: [20],
        population_estimate: 6600,
        conservation_status: "Endangered",
        threats: ["Habitat Fragmentation", "Disease", "Human Conflict"],
        diet: "Carnivore",
        lifespan_years: 11
    },
    {
        species_id: "SP008",
        common_name: "Siberian Crane",
        scientific_name: "Leucogeranus leucogeranus",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Aves",
            order: "Gruiformes",
            family: "Gruidae"
        },
        habitat_regions: [15],
        population_estimate: 4000,
        conservation_status: "Critically Endangered",
        threats: ["Wetland Loss", "Climate Change", "Pollution"],
        diet: "Omnivore",
        lifespan_years: 30
    },
    {
        species_id: "SP009",
        common_name: "Galápagos Giant Tortoise",
        scientific_name: "Chelonoidis nigra",
        classification: {
            kingdom: "Animalia",
            phylum: "Chordata",
            class: "Reptilia",
            order: "Testudines",
            family: "Testudinidae"
        },
        habitat_regions: [17],
        population_estimate: 15000,
        conservation_status: "Vulnerable",
        threats: ["Invasive Species", "Habitat Loss", "Climate Change"],
        diet: "Herbivore",
        lifespan_years: 100
    }
]);

// ========================================
// COLLECTION 5: Sensor_Metadata
// Purpose: Information about sensor devices
// ========================================
db.Sensor_Metadata.insertMany([
    {
        sensor_id: "SENS_001",
        sensor_type: "Climate Monitor",
        region_id: 1,
        region_name: "Amazon Basin",
        manufacturer: "EnviroTech",
        model: "ET-CM-500",
        installation_date: new Date("2022-06-15"),
        last_maintenance: new Date("2024-01-10"),
        status: "active",
        measurements: ["temperature", "humidity", "rainfall"],
        accuracy_rating: 0.98,
        coordinates: {
            latitude: -3.4653,
            longitude: -62.2159
        }
    },
    {
        sensor_id: "SENS_002",
        sensor_type: "Water Quality Monitor",
        region_id: 2,
        region_name: "Great Barrier Reef",
        manufacturer: "OceanSense",
        model: "OS-WQ-750",
        installation_date: new Date("2022-08-20"),
        last_maintenance: new Date("2024-02-05"),
        status: "active",
        measurements: ["water_temperature", "salinity", "pH", "dissolved_oxygen"],
        accuracy_rating: 0.96,
        coordinates: {
            latitude: -18.2871,
            longitude: 147.6992
        }
    },
    {
        sensor_id: "SENS_003",
        sensor_type: "Air Quality Monitor",
        region_id: 3,
        region_name: "Sahara Desert",
        manufacturer: "AirWatch",
        model: "AW-AQ-300",
        installation_date: new Date("2023-01-10"),
        last_maintenance: new Date("2024-01-20"),
        status: "active",
        measurements: ["PM2.5", "PM10", "CO2", "NO2", "SO2"],
        accuracy_rating: 0.95,
        coordinates: {
            latitude: 23.8859,
            longitude: 8.0817
        }
    },
    {
        sensor_id: "SENS_005",
        sensor_type: "Climate Monitor",
        region_id: 5,
        region_name: "Congo Rainforest",
        manufacturer: "EnviroTech",
        model: "ET-CM-500",
        installation_date: new Date("2022-09-05"),
        last_maintenance: new Date("2023-12-15"),
        status: "active",
        measurements: ["temperature", "humidity", "rainfall"],
        accuracy_rating: 0.97,
        coordinates: {
            latitude: -0.2280,
            longitude: 15.8277
        }
    },
    {
        sensor_id: "SENS_007",
        sensor_type: "Air Quality Monitor",
        region_id: 7,
        region_name: "Great Plains",
        manufacturer: "AirWatch",
        model: "AW-AQ-300",
        installation_date: new Date("2023-03-12"),
        last_maintenance: new Date("2024-02-28"),
        status: "active",
        measurements: ["PM2.5", "PM10", "CO2", "NO2", "SO2"],
        accuracy_rating: 0.94,
        coordinates: {
            latitude: 41.4925,
            longitude: -99.9018
        }
    },
    {
        sensor_id: "SENS_009",
        sensor_type: "Climate Monitor",
        region_id: 9,
        region_name: "Patagonia",
        manufacturer: "EnviroTech",
        model: "ET-CM-700",
        installation_date: new Date("2022-11-18"),
        last_maintenance: new Date("2024-01-25"),
        status: "active",
        measurements: ["temperature", "humidity", "wind_speed"],
        accuracy_rating: 0.96,
        coordinates: {
            latitude: -49.3315,
            longitude: -72.8860
        }
    },
    {
        sensor_id: "SENS_010",
        sensor_type: "Atmospheric Monitor",
        region_id: 10,
        region_name: "Andes Mountains",
        manufacturer: "SkyMetrics",
        model: "SM-ATM-410",
        installation_date: new Date("2023-02-14"),
        last_maintenance: new Date("2024-02-02"),
        status: "active",
        measurements: ["temperature", "pressure", "ozone"],
        accuracy_rating: 0.95,
        coordinates: {
            latitude: -13.1631,
            longitude: -72.5450
        }
    },
    {
        sensor_id: "SENS_013",
        sensor_type: "Hydro-Climate Monitor",
        region_id: 13,
        region_name: "Sundarbans Mangrove Forest",
        manufacturer: "EcoHydro",
        model: "EH-HC-880",
        installation_date: new Date("2022-07-09"),
        last_maintenance: new Date("2024-01-30"),
        status: "active",
        measurements: ["rainfall", "humidity", "soil_moisture", "salinity"],
        accuracy_rating: 0.97,
        coordinates: {
            latitude: 21.9497,
            longitude: 89.1833
        }
    },
    {
        sensor_id: "SENS_016",
        sensor_type: "Air Quality Monitor",
        region_id: 16,
        region_name: "Atacama Desert",
        manufacturer: "AirWatch",
        model: "AW-AQ-450",
        installation_date: new Date("2023-05-21"),
        last_maintenance: new Date("2024-02-18"),
        status: "active",
        measurements: ["PM2.5", "PM10", "CO2", "NO2"],
        accuracy_rating: 0.93,
        coordinates: {
            latitude: -23.8634,
            longitude: -69.1328
        }
    },
    {
        sensor_id: "SENS_020",
        sensor_type: "Wildlife Climate Monitor",
        region_id: 20,
        region_name: "Okavango Delta",
        manufacturer: "BioTrack",
        model: "BT-WC-300",
        installation_date: new Date("2022-10-03"),
        last_maintenance: new Date("2024-01-12"),
        status: "active",
        measurements: ["temperature", "humidity", "water_level"],
        accuracy_rating: 0.96,
        coordinates: {
            latitude: -19.2870,
            longitude: 22.4430
        }
    }
]);

// ========================================
// CREATE INDEXES FOR BETTER QUERY PERFORMANCE
// ========================================
db.Biodiversity_Data.createIndex({ region_id: 1 });
db.Sensor_Logs.createIndex({ sensor_id: 1, timestamp: -1 });
db.Air_Quality_History.createIndex({ region_id: 1, recorded_at: -1 });
db.Species_Details.createIndex({ habitat_regions: 1 });
db.Sensor_Metadata.createIndex({ sensor_id: 1 });

// ========================================
// VERIFICATION QUERIES
// ========================================
// db.Biodiversity_Data.find().pretty();
// db.Sensor_Logs.find().pretty();
// db.Air_Quality_History.find().pretty();
// db.Species_Details.find().pretty();
// db.Sensor_Metadata.find().pretty();

printjson("MongoDB collections created successfully!");
printjson("Total documents:");
printjson("- Biodiversity_Data: " + db.Biodiversity_Data.countDocuments());
printjson("- Sensor_Logs: " + db.Sensor_Logs.countDocuments());
printjson("- Air_Quality_History: " + db.Air_Quality_History.countDocuments());
printjson("- Species_Details: " + db.Species_Details.countDocuments());
printjson("- Sensor_Metadata: " + db.Sensor_Metadata.countDocuments());

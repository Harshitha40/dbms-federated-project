# ========================================
# LLM-Powered Natural Language to SQL Converter
# Uses Groq Qwen for intelligent query generation
# ========================================

import os
import json
from groq import Groq
from config import GROQ_API_KEY

class LLMQueryConverter:
    """
    Converts natural language to SQL using Groq's Qwen models.
    Provides context-aware query generation with schema understanding.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the LLM converter.
        
        Args:
            api_key (str): Groq API key. If None, reads from config.
        """
        self.api_key = api_key or GROQ_API_KEY
        self.client = None
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        
        # Database schema context
        self.schema_context = self._build_schema_context()
    
    def _build_schema_context(self):
        """Build comprehensive schema context for the LLM"""
        return """
# FEDERATED DATABASE SCHEMA

## Data Sources:
1. **PostgreSQL** (relational database)
2. **MongoDB** (NoSQL document database)  
3. **CSV Files** (flat file storage)

## PostgreSQL Tables (prefix: postgres.public.`table_name`):

### 1. region_info
Columns: region_id (INT), region_name (VARCHAR), latitude (DECIMAL), longitude (DECIMAL)
Description: Geographic regions for environmental monitoring
Example: Amazon Basin, Great Barrier Reef, Sahara Desert, Arctic Tundra, Congo Rainforest, Himalayas, Great Plains, Madagascar

### 2. climate_data
Columns: climate_id (INT), region_id (INT FK→region_info), temperature (DECIMAL °C), rainfall (DECIMAL mm), humidity (DECIMAL %), timestamp (TIMESTAMP)
Description: Climate measurements per region
Temperature Range: -25°C to 40°C (avg: 18°C). Consider "high" as >25°C, "low" as <10°C
Rainfall Range: 0-500mm. Consider "high" as >200mm, "low" as <50mm
Humidity Range: 20-95%. Consider "high" as >70%, "low" as <40%
Join: climate_data.region_id = region_info.region_id

### 3. agriculture_data
Columns: agri_id (INT), region_id (INT FK→region_info), crop_type (VARCHAR), yield (DECIMAL tons), season (VARCHAR), year (INT)
Description: Agricultural production data
Seasons: Spring, Summer, Fall, Winter
Crops: Cassava, Cocoa, Wheat, Corn, Soybean, Rice, Vanilla, Barley, Plantain

### 4. user_info
Columns: user_id (INT), name (VARCHAR), email (VARCHAR), password_hash (VARCHAR), role (VARCHAR), created_at (TIMESTAMP)
Roles: Researcher, Data Provider, Administrator
Description: System users with authentication

### 5. query_log
Columns: query_id (INT), user_id (INT FK→user_info), query_text (TEXT), executed_at (TIMESTAMP)
Description: Audit trail of executed queries

## MongoDB Collections (prefix: mongo.environmental_db.`CollectionName`):

### 1. Biodiversity_Data
Fields: biodiversity_id, region_id (INT), region_name, species_count (INT), endangered_species (Array), dominant_flora (Array), conservation_status (String), last_survey_date (Date)
Conservation Status: Critical, Endangered, Vulnerable
Description: Species diversity and conservation data
**IMPORTANT**: endangered_species and dominant_flora are ARRAYS. To count array elements, just return the array and count on client side, or use species_count (INT) field which already contains the count.

### 2. Sensor_Logs
Fields: log_id, sensor_id, region_id (INT), event_type, severity (warning/critical/info), message, timestamp (Date)
Description: Real-time sensor event logs

### 3. Air_Quality_History
Fields: air_quality_id, region_id (INT), region_name, aqi (INT), air_quality_level, pollutants (Object: pm2_5, pm10, o3, no2, so2), recorded_date (Date)
Description: Historical air quality measurements

### 4. Species_Details
Fields: species_id, species_name, scientific_name, classification (Object: kingdom, phylum, class, order, family, genus), habitat, conservation_status, population_estimate (INT)
Description: Detailed species information

### 5. Sensor_Metadata
Fields: sensor_id, sensor_type, location_name, region_id (INT), installation_date (Date), status, last_maintenance (Date)
Description: IoT sensor device information

## CSV Files (prefix: dfs.data.`filename.csv`):

### 1. sensor_readings.csv
Columns: timestamp (String), region_id (String), co2_level (String), pm2_5 (String)
Description: Real-time CO2 and particulate matter readings
Note: Cast region_id to INT, co2_level and pm2_5 to FLOAT for calculations
Example: CAST(s.region_id AS INT), CAST(s.co2_level AS FLOAT)

## Query Syntax Rules:

1. **Table References**: Use backticks around table/collection names
   - PostgreSQL: postgres.public.`table_name`
   - MongoDB: mongo.environmental_db.`CollectionName`
   - CSV: dfs.data.`filename.csv`

2. **Joins**: Use ON clause with matching IDs
   ```sql
   FROM postgres.public.`climate_data` c
   JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
   ```

3. **Federated Joins** (across different databases):
   ```sql
   FROM postgres.public.`region_info` r
   JOIN postgres.public.`climate_data` c ON r.region_id = c.region_id
   JOIN mongo.environmental_db.`Biodiversity_Data` b ON r.region_id = b.region_id
   JOIN dfs.data.`sensor_readings.csv` s ON CAST(s.region_id AS INT) = r.region_id
   ```

4. **Aggregations**: Use GROUP BY with aggregate functions (AVG, SUM, COUNT, MAX, MIN)

5. **Filtering**: Use WHERE clause (avoid ORDER BY timestamp as it can cause issues)
   - For "high temperature": WHERE temperature > 25
   - For "low temperature": WHERE temperature < 10
   - For "high rainfall": WHERE rainfall > 200
   - For "high humidity": WHERE humidity > 70
   - For qualitative terms (high/low/hot/cold), use the ranges specified in table descriptions

6. **Limits**: Always add LIMIT clause to prevent large result sets (typically LIMIT 10-20)

## Common Query Patterns:

- List all regions: `SELECT * FROM postgres.public.`region_info` LIMIT 10`
- Climate with regions: Join climate_data + region_info
- Biodiversity analysis: Join MongoDB Biodiversity_Data + PostgreSQL region_info
- Sensor analysis: Join CSV sensor_readings + PostgreSQL region_info (remember to CAST)
- Complete view: Join all 3 sources using region_id as the common key
"""
    
    def convert(self, natural_query, use_llm=True):
        """
        Convert natural language to SQL using LLM only.
        
        Args:
            natural_query (str): User's question in natural language
            use_llm (bool): Whether to use LLM (True) or fallback pattern matching (False)
            
        Returns:
            dict: {
                'sql': generated SQL query,
                'confidence': confidence score (0-1),
                'interpretation': what the system understood,
                'method': 'llm' or 'error'
            }
        """
        if not self.client:
            return {
                'sql': '',
                'confidence': 0.0,
                'interpretation': 'LLM not available. Please configure GROQ_API_KEY.',
                'method': 'error'
            }
        
        return self._convert_with_llm(natural_query)
    
    def _convert_with_llm(self, natural_query):
        """Use Groq Qwen to convert natural language to SQL"""
        try:
            prompt = f"""You are a SQL expert specializing in federated database queries using Apache Drill.

{self.schema_context}

USER QUESTION: "{natural_query}"

Generate a valid SQL query that answers the user's question. Follow these guidelines:

IMPORTANT: Return ONLY the SQL query. Do NOT include any thinking process, explanations, or tags like <think>.

1. Use the correct table/collection prefixes and backticks
2. For FEDERATED queries joining PostgreSQL and MongoDB:
   - MUST use CTEs (WITH clause) to separate data sources
   - Example: WITH pg_data AS (SELECT ... FROM postgres...), mongo_data AS (SELECT ... FROM mongo...)
   - Then JOIN the CTEs: SELECT * FROM pg_data JOIN mongo_data ON ...
   - Do NOT use table aliases (like 'c.column') inside CTE SELECT clauses
   - AVOID selecting 'timestamp' column in CTEs (reserved keyword, causes parse errors)
3. For single-database queries, use direct JOINs as normal
4. MongoDB array fields (endangered_species, dominant_flora):
   - Do NOT use COUNT(DISTINCT array_field) or aggregate functions on arrays
   - Simply SELECT the array field and return it as-is
   - For counting: use the species_count field (already computed) instead of counting endangered_species array
5. Add LIMIT 10 to prevent large result sets
6. For CSV files, remember to CAST string columns to appropriate types
7. Do NOT include semicolons at the end
7. Return only the SQL query, no explanations

SQL Query:"""

            completion = self.client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Generate only valid SQL queries without explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_completion_tokens=4096,
                top_p=0.95,
                reasoning_effort="default",
                stream=True,
                stop=None
            )
            
            # Collect streaming response
            sql_query = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    sql_query += chunk.choices[0].delta.content
            
            sql_query = sql_query.strip()
            
            # Remove <think> tags if present (reasoning artifacts)
            import re
            if '<think>' in sql_query:
                # Extract content after </think>
                think_pattern = r'<think>.*?</think>\s*'
                sql_query = re.sub(think_pattern, '', sql_query, flags=re.DOTALL)
                sql_query = sql_query.strip()
            
            # Remove markdown code blocks if present (handle both ``` and ```sql formats)
            import re
            # Remove any markdown code block wrappers
            sql_query = re.sub(r'```sql\s*', '', sql_query)
            sql_query = re.sub(r'```\s*', '', sql_query)
            sql_query = sql_query.strip()
            
            # Remove any "SQL Query:" prefix
            if sql_query.lower().startswith('sql query:'):
                sql_query = sql_query[10:].strip()
            
            # Clean up any remaining whitespace/newlines
            sql_query = ' '.join(sql_query.split())
            
            # Remove trailing semicolon (Drill REST API doesn't accept it)
            if sql_query.endswith(';'):
                sql_query = sql_query[:-1].strip()
            
            # Generate interpretation
            interpretation = self._generate_interpretation(natural_query, sql_query)
            
            return {
                'sql': sql_query,
                'confidence': 0.95,
                'interpretation': interpretation,
                'method': 'llm'
            }
            
        except Exception as e:
            print(f"LLM conversion error: {e}")
            return {
                'sql': '',
                'confidence': 0.0,
                'interpretation': f'Error processing query: {str(e)}',
                'method': 'error'
            }
    
    def _convert_with_patterns(self, natural_query):
        """Fallback pattern-based conversion"""
        query_lower = natural_query.lower().strip()
        
        # Simple pattern matching (from original nlp_query.py)
        if 'region' in query_lower:
            if 'climate' in query_lower:
                return {
                    'sql': '''SELECT r.region_name, c.temperature, c.rainfall, c.humidity
                    FROM postgres.public.`climate_data` c
                    JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                    LIMIT 10''',
                    'confidence': 0.7,
                    'interpretation': 'Showing climate data by region',
                    'method': 'pattern'
                }
            else:
                return {
                    'sql': 'SELECT * FROM postgres.public.`region_info` LIMIT 10',
                    'confidence': 0.8,
                    'interpretation': 'Listing all regions',
                    'method': 'pattern'
                }
        
        if 'climate' in query_lower or 'temperature' in query_lower:
            return {
                'sql': 'SELECT * FROM postgres.public.`climate_data` LIMIT 10',
                'confidence': 0.7,
                'interpretation': 'Showing climate data',
                'method': 'pattern'
            }
        
        if 'species' in query_lower or 'biodiversity' in query_lower:
            return {
                'sql': 'SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 10',
                'confidence': 0.7,
                'interpretation': 'Showing biodiversity data',
                'method': 'pattern'
            }
        
        if 'sensor' in query_lower or 'co2' in query_lower:
            return {
                'sql': 'SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 10',
                'confidence': 0.7,
                'interpretation': 'Showing sensor readings',
                'method': 'pattern'
            }
        
        # Default
        return {
            'sql': 'SELECT * FROM postgres.public.`region_info` LIMIT 10',
            'confidence': 0.4,
            'interpretation': 'Unable to parse query. Showing regions as default.',
            'method': 'pattern'
        }
    
    def _generate_interpretation(self, natural_query, sql_query):
        """Generate human-readable interpretation of the query"""
        interpretation = f"Converting '{natural_query}' to SQL query"
        
        if 'JOIN' in sql_query.upper():
            sources = []
            if 'postgres' in sql_query.lower():
                sources.append('PostgreSQL')
            if 'mongo' in sql_query.lower():
                sources.append('MongoDB')
            if 'dfs' in sql_query.lower() or '.csv' in sql_query.lower():
                sources.append('CSV')
            
            if len(sources) > 1:
                interpretation = f"Federated query across {', '.join(sources)}"
            else:
                interpretation = f"Joining tables in {sources[0]}"
        
        if 'AVG' in sql_query.upper() or 'SUM' in sql_query.upper() or 'COUNT' in sql_query.upper():
            interpretation += " with aggregation"
        
        if 'WHERE' in sql_query.upper():
            interpretation += " with filtering"
        
        return interpretation
    
    def is_available(self):
        """Check if LLM is available"""
        return self.client is not None


# Example usage
if __name__ == "__main__":
    # Test with API key from environment
    converter = LLMQueryConverter()
    
    if converter.is_available():
        print("✓ LLM is available")
    else:
        print("✗ LLM not available (no API key). Using pattern matching fallback.")
    
    test_queries = [
        "Show me all regions with their climate data",
        "What is the average CO2 level by region?",
        "Find regions with high biodiversity and their temperature",
        "List all crop types and their yields",
        "Which regions have the most endangered species?"
    ]
    
    for query in test_queries:
        result = converter.convert(query)
        print(f"\n{'='*60}")
        print(f"Natural Query: {query}")
        print(f"Method: {result['method']}")
        print(f"Interpretation: {result['interpretation']}")
        print(f"Confidence: {result['confidence']}")
        print(f"SQL:\n{result['sql']}")

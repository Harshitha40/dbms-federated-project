# ========================================
# Natural Language to SQL Query Converter
# ========================================

import re

class NLPQueryConverter:
    """
    Converts natural language queries to SQL for federated database querying.
    Uses pattern matching and keyword detection.
    """
    
    def __init__(self):
        # Define table mappings
        self.tables = {
            'region': 'postgres.public.`region_info`',
            'regions': 'postgres.public.`region_info`',
            'climate': 'postgres.public.`climate_data`',
            'temperature': 'postgres.public.`climate_data`',
            'weather': 'postgres.public.`climate_data`',
            'agriculture': 'postgres.public.`agriculture_data`',
            'crops': 'postgres.public.`agriculture_data`',
            'farming': 'postgres.public.`agriculture_data`',
            'biodiversity': 'mongo.environmental_db.`Biodiversity_Data`',
            'species': 'mongo.environmental_db.`Biodiversity_Data`',
            'animals': 'mongo.environmental_db.`Biodiversity_Data`',
            'sensor': 'dfs.data.`sensor_readings.csv`',
            'sensors': 'dfs.data.`sensor_readings.csv`',
            'co2': 'dfs.data.`sensor_readings.csv`',
            'air quality': 'mongo.environmental_db.`Air_Quality_History`',
            'pollution': 'mongo.environmental_db.`Air_Quality_History`'
        }
        
        # Define column mappings
        self.columns = {
            'name': 'region_name',
            'names': 'region_name',
            'temp': 'temperature',
            'hot': 'temperature',
            'cold': 'temperature',
            'rain': 'rainfall',
            'humid': 'humidity',
            'moisture': 'humidity',
            'crop': 'crop_type',
            'yield': 'yield',
            'production': 'yield',
            'season': 'season',
            'year': 'year',
            'count': 'species_count',
            'number': 'species_count',
            'endangered': 'conservation_status',
            'carbon': 'co2_level',
            'co2': 'co2_level',
            'pm': 'pm2_5',
            'particulate': 'pm2_5'
        }
    
    def convert(self, natural_query):
        """
        Convert natural language query to SQL.
        
        Args:
            natural_query (str): Natural language query
            
        Returns:
            dict: {
                'sql': generated SQL query,
                'confidence': confidence score (0-1),
                'interpretation': what the system understood
            }
        """
        query_lower = natural_query.lower().strip()
        
        # Try different patterns
        patterns = [
            self._pattern_show_all,
            self._pattern_show_regions,
            self._pattern_show_with_condition,
            self._pattern_count_query,
            self._pattern_join_query,
            self._pattern_aggregation,
            self._pattern_comparison,
            self._pattern_high_low
        ]
        
        for pattern_func in patterns:
            result = pattern_func(query_lower)
            if result:
                return result
        
        # Default: try to extract keywords
        return self._fallback_query(query_lower)
    
    def _pattern_show_all(self, query):
        """Pattern: 'show all [table]' or 'list all [table]' or 'get [table]'"""
        patterns = [
            r'(?:show|list|get|display|find)\s+(?:all\s+)?(\w+)',
            r'(?:what|which)\s+(?:are|is)\s+(?:all\s+)?(?:the\s+)?(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                entity = match.group(1)
                table = self._find_table(entity)
                if table:
                    return {
                        'sql': f'SELECT * FROM {table} LIMIT 10',
                        'confidence': 0.9,
                        'interpretation': f'Retrieving all {entity} records'
                    }
        return None
    
    def _pattern_show_regions(self, query):
        """Pattern: region-specific queries"""
        if 'region' in query and ('name' in query or 'list' in query or 'show' in query):
            return {
                'sql': 'SELECT * FROM postgres.public.`region_info` LIMIT 10',
                'confidence': 0.95,
                'interpretation': 'Listing all regions'
            }
        return None
    
    def _pattern_show_with_condition(self, query):
        """Pattern: 'show [table] where [condition]'"""
        if 'where' in query or 'with' in query:
            parts = re.split(r'\s+(?:where|with)\s+', query)
            if len(parts) == 2:
                entity = parts[0].replace('show', '').replace('list', '').replace('get', '').strip()
                condition = parts[1]
                
                table = self._find_table(entity)
                if table:
                    sql_condition = self._parse_condition(condition)
                    if sql_condition:
                        return {
                            'sql': f'SELECT * FROM {table} WHERE {sql_condition} LIMIT 10',
                            'confidence': 0.8,
                            'interpretation': f'Finding {entity} matching condition: {condition}'
                        }
        return None
    
    def _pattern_count_query(self, query):
        """Pattern: 'how many [table]' or 'count [table]'"""
        patterns = [
            r'(?:how\s+many|count|number\s+of)\s+(\w+)',
            r'total\s+(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                entity = match.group(1)
                table = self._find_table(entity)
                if table:
                    return {
                        'sql': f'SELECT COUNT(*) as total FROM {table}',
                        'confidence': 0.9,
                        'interpretation': f'Counting total number of {entity}'
                    }
        return None
    
    def _pattern_join_query(self, query):
        """Pattern: queries that need joins"""
        # Climate + Regions
        if ('climate' in query or 'temperature' in query) and 'region' in query:
            return {
                'sql': '''SELECT r.region_name, c.temperature, c.rainfall, c.humidity
                FROM postgres.public.`climate_data` c
                JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                LIMIT 10''',
                'confidence': 0.85,
                'interpretation': 'Showing climate data with region names'
            }
        
        # Biodiversity + Climate
        if ('species' in query or 'biodiversity' in query) and ('climate' in query or 'temperature' in query):
            return {
                'sql': '''SELECT r.region_name, c.temperature, b.species_count, b.conservation_status
                FROM postgres.public.`region_info` r
                JOIN postgres.public.`climate_data` c ON r.region_id = c.region_id
                JOIN mongo.environmental_db.`Biodiversity_Data` b ON r.region_id = b.region_id
                LIMIT 10''',
                'confidence': 0.8,
                'interpretation': 'Correlating species diversity with climate conditions'
            }
        
        # Sensors + Regions
        if ('sensor' in query or 'co2' in query) and 'region' in query:
            return {
                'sql': '''SELECT r.region_name, s.co2_level, s.pm2_5
                FROM dfs.data.`sensor_readings.csv` s
                JOIN postgres.public.`region_info` r ON CAST(s.region_id AS INT) = r.region_id
                LIMIT 10''',
                'confidence': 0.85,
                'interpretation': 'Showing sensor readings with region names'
            }
        
        # Agriculture + Regions
        if ('crop' in query or 'agriculture' in query or 'farming' in query) and 'region' in query:
            return {
                'sql': '''SELECT r.region_name, a.crop_type, a.yield, a.season
                FROM postgres.public.`agriculture_data` a
                JOIN postgres.public.`region_info` r ON a.region_id = r.region_id
                LIMIT 10''',
                'confidence': 0.85,
                'interpretation': 'Showing crop production by region'
            }
        
        return None
    
    def _pattern_aggregation(self, query):
        """Pattern: aggregation queries (average, sum, max, min)"""
        agg_functions = {
            'average': 'AVG',
            'avg': 'AVG',
            'mean': 'AVG',
            'total': 'SUM',
            'sum': 'SUM',
            'maximum': 'MAX',
            'max': 'MAX',
            'highest': 'MAX',
            'minimum': 'MIN',
            'min': 'MIN',
            'lowest': 'MIN'
        }
        
        for keyword, sql_func in agg_functions.items():
            if keyword in query:
                # Temperature average
                if 'temperature' in query or 'temp' in query:
                    return {
                        'sql': f'''SELECT r.region_name, {sql_func}(c.temperature) as value
                        FROM postgres.public.`climate_data` c
                        JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                        GROUP BY r.region_name
                        LIMIT 10''',
                        'confidence': 0.85,
                        'interpretation': f'Calculating {keyword} temperature by region'
                    }
                
                # CO2 levels
                if 'co2' in query or 'carbon' in query:
                    return {
                        'sql': f'''SELECT r.region_name, {sql_func}(CAST(s.co2_level AS FLOAT)) as value
                        FROM dfs.data.`sensor_readings.csv` s
                        JOIN postgres.public.`region_info` r ON CAST(s.region_id AS INT) = r.region_id
                        GROUP BY r.region_name
                        LIMIT 10''',
                        'confidence': 0.85,
                        'interpretation': f'Calculating {keyword} CO2 levels by region'
                    }
                
                # Crop yield
                if 'yield' in query or 'production' in query or 'crop' in query:
                    return {
                        'sql': f'''SELECT r.region_name, {sql_func}(a.yield) as value
                        FROM postgres.public.`agriculture_data` a
                        JOIN postgres.public.`region_info` r ON a.region_id = r.region_id
                        GROUP BY r.region_name
                        LIMIT 10''',
                        'confidence': 0.85,
                        'interpretation': f'Calculating {keyword} crop yield by region'
                    }
        
        return None
    
    def _pattern_comparison(self, query):
        """Pattern: comparison queries (greater than, less than)"""
        # High temperature
        if any(word in query for word in ['hot', 'warm', 'high temp', 'above']):
            threshold = self._extract_number(query) or 25
            return {
                'sql': f'''SELECT r.region_name, c.temperature
                FROM postgres.public.`climate_data` c
                JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                WHERE c.temperature > {threshold}
                LIMIT 10''',
                'confidence': 0.8,
                'interpretation': f'Finding regions with temperature above {threshold}°C'
            }
        
        # High CO2
        if any(word in query for word in ['high co2', 'carbon dioxide', 'pollution']):
            threshold = self._extract_number(query) or 420
            return {
                'sql': f'''SELECT r.region_name, s.co2_level
                FROM dfs.data.`sensor_readings.csv` s
                JOIN postgres.public.`region_info` r ON CAST(s.region_id AS INT) = r.region_id
                WHERE CAST(s.co2_level AS FLOAT) > {threshold}
                LIMIT 10''',
                'confidence': 0.8,
                'interpretation': f'Finding regions with CO2 above {threshold} ppm'
            }
        
        return None
    
    def _pattern_high_low(self, query):
        """Pattern: queries for highest/lowest values"""
        if 'highest' in query or 'top' in query or 'maximum' in query:
            if 'temperature' in query:
                return {
                    'sql': '''SELECT r.region_name, c.temperature
                    FROM postgres.public.`climate_data` c
                    JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                    ORDER BY c.temperature DESC
                    LIMIT 5''',
                    'confidence': 0.9,
                    'interpretation': 'Finding regions with highest temperatures'
                }
            
            if 'species' in query or 'biodiversity' in query:
                return {
                    'sql': '''SELECT r.region_name, b.species_count
                    FROM mongo.environmental_db.`Biodiversity_Data` b
                    JOIN postgres.public.`region_info` r ON b.region_id = r.region_id
                    ORDER BY b.species_count DESC
                    LIMIT 5''',
                    'confidence': 0.9,
                    'interpretation': 'Finding regions with most species diversity'
                }
        
        if 'lowest' in query or 'bottom' in query or 'minimum' in query:
            if 'temperature' in query:
                return {
                    'sql': '''SELECT r.region_name, c.temperature
                    FROM postgres.public.`climate_data` c
                    JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
                    ORDER BY c.temperature ASC
                    LIMIT 5''',
                    'confidence': 0.9,
                    'interpretation': 'Finding regions with lowest temperatures'
                }
        
        return None
    
    def _fallback_query(self, query):
        """Fallback: try to generate query from keywords"""
        # Find potential tables
        found_tables = []
        for keyword, table in self.tables.items():
            if keyword in query:
                found_tables.append(table)
        
        if found_tables:
            # Use the first found table
            return {
                'sql': f'SELECT * FROM {found_tables[0]} LIMIT 10',
                'confidence': 0.5,
                'interpretation': f'Showing data based on keyword match (low confidence)'
            }
        
        # Ultimate fallback: show regions
        return {
            'sql': 'SELECT * FROM postgres.public.`region_info` LIMIT 10',
            'confidence': 0.3,
            'interpretation': 'Unable to parse query clearly. Showing regions as default.'
        }
    
    def _find_table(self, entity):
        """Find the appropriate table for an entity"""
        entity = entity.lower().strip()
        return self.tables.get(entity)
    
    def _parse_condition(self, condition):
        """Parse a natural language condition into SQL"""
        # Simple conditions for now
        if '>' in condition or 'greater' in condition or 'more than' in condition:
            number = self._extract_number(condition)
            if number:
                column = self._find_column_in_text(condition)
                if column:
                    return f"{column} > {number}"
        
        if '<' in condition or 'less' in condition or 'below' in condition:
            number = self._extract_number(condition)
            if number:
                column = self._find_column_in_text(condition)
                if column:
                    return f"{column} < {number}"
        
        return None
    
    def _find_column_in_text(self, text):
        """Find column name in text"""
        for keyword, column in self.columns.items():
            if keyword in text:
                return column
        return None
    
    def _extract_number(self, text):
        """Extract number from text"""
        match = re.search(r'\d+(?:\.\d+)?', text)
        if match:
            return float(match.group(0))
        return None


# Example usage
if __name__ == "__main__":
    converter = NLPQueryConverter()
    
    test_queries = [
        "show all regions",
        "list climate data",
        "how many species are there",
        "show regions with climate",
        "what is the average temperature by region",
        "find regions with high CO2 levels",
        "show the hottest regions",
        "which regions have crops"
    ]
    
    for query in test_queries:
        result = converter.convert(query)
        print(f"\nNatural: {query}")
        print(f"SQL: {result['sql']}")
        print(f"Confidence: {result['confidence']}")

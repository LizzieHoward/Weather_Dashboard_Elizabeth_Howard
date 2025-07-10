"""
Error handling utilities for Weather Dashboard
- Handles common typing errors (e.g., capitalization, whitespace)
- Maps shorthand city names to full names
"""

class CityNameHandler:
    CITY_SHORTHANDS = {
        "nyc": "New York",
        "sf": "San Francisco",
        "la": "Los Angeles",
        "dc": "Washington",
        "phx": "Phoenix",
        "chi": "Chicago",
        "bos": "Boston",
        "dal": "Dallas",
        "phl": "Philadelphia",
        "sea": "Seattle",
        "lv": "Las Vegas",
        "mia": "Miami",
        # Add more as needed
    }

    @classmethod
    def normalize_city_name(cls, city: str) -> str:
        """
        Normalize city name input:
        - Strips whitespace
        - Converts to title case
        - Expands common shorthands
        """
        if not isinstance(city, str):
            raise TypeError("City name must be a string.")
        city_clean = city.strip().lower()
        # Expand shorthand if present
        city_full = cls.CITY_SHORTHANDS.get(city_clean, city_clean)
        # Title case for API
        return city_full.title()

    @staticmethod
    def validate_city_name(city: str) -> bool:
        """
        Checks if the city name is valid (non-empty, only letters and spaces)
        """
        if not isinstance(city, str):
            return False
        city = city.strip()
        return bool(city) and all(c.isalpha() or c.isspace() for c in city)

if __name__ == "__main__":
    # Example usage
    test_inputs = ["nyc", "  sf  ", "miami", "bos", "123", "", None]
    for inp in test_inputs:
        try:
            norm = CityNameHandler.normalize_city_name(inp)
            valid = CityNameHandler.validate_city_name(norm)
            print(f"Input: {inp!r} -> Normalized: {norm!r}, Valid: {valid}")
        except Exception as e:
            print(f"Input: {inp!r} -> Error: {e}")

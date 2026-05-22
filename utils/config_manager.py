import os
import json
from dotenv import load_dotenv

load_dotenv()


class ConfigManager:
    """Manage configuration from environment variables and config files"""
    
    @staticmethod
    def get_config(key, default=None):
        """Get configuration value from environment"""
        return os.getenv(key, default)
    
    @staticmethod
    def load_config_from_json(filepath):
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {filepath}")
            return {}
    
    @staticmethod
    def save_config_to_json(filepath, config_dict):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=4)


class TestData:
    """Manage test data"""
    
    @staticmethod
    def load_test_data(filename):
        """Load test data from JSON file"""
        filepath = f"data/{filename}.json"
        return ConfigManager.load_config_from_json(filepath)
    
    @staticmethod
    def get_test_user(user_type="valid"):
        """Get test user credentials"""
        test_data = TestData.load_test_data("users")
        return test_data.get(user_type, {})

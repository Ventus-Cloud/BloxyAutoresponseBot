import json
import logging
import re
import random
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class ResponseHandler:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.triggers = {}
        self.load_config()
        
    def load_config(self):
        """Load trigger words and responses from config file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.triggers = config.get('triggers', {})
                logger.info(f'Loaded {len(self.triggers)} trigger configurations')
        except FileNotFoundError:
            logger.warning(f'Config file {self.config_file} not found. Creating default config.')
            self.create_default_config()
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in config file: {e}')
            self.create_default_config()
        except Exception as e:
            logger.error(f'Error loading config: {e}')
            self.create_default_config()
            
    def create_default_config(self):
        """Create a default configuration file"""
        default_config = {
            "triggers": {
                "ventus": {
                    "responses": [
                        "Mejor hazle ping <@866749277966565426>"
                    ],
                    "match_type": "contains",
                    "enabled": True
                },
                "lau": {
                    "responses": [
                        "Mejor hazle ping <@643114684177711123>"
                    ],
                    "match_type": "contains",
                    "enabled": True
                },
                "clara": {
                    "responses": [
                        "Mejor hazle ping <@1333869783359160341>"
                    ],
                    "match_type": "contains",
                    "enabled": True
                },
             
             
            },
            "settings": {
                "case_sensitive": False,
                "cooldown_seconds": 3,
                "max_response_length": 2000
            }
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            self.triggers = default_config['triggers']
            logger.info('Created default config file')
        except Exception as e:
            logger.error(f'Failed to create default config: {e}')
            
    def reload_config(self):
        """Reload configuration from file"""
        self.load_config()
        
    async def check_triggers(self, message_content: str) -> Optional[str]:
        """Check if message contains any trigger words and return appropriate response"""
        if not message_content:
            return None
            
        for trigger, config in self.triggers.items():
            if not config.get('enabled', True):
                continue
                
            match_type = config.get('match_type', 'contains')
            responses = config.get('responses', [])
            
            if not responses:
                continue
                
            # Check for trigger match based on match type
            if self._is_trigger_match(message_content, trigger, match_type):
                response = random.choice(responses)
                logger.info(f'Trigger matched: "{trigger}" -> "{response[:50]}..."')
                return response
                
        return None
        
    def _is_trigger_match(self, message: str, trigger: str, match_type: str) -> bool:
        """Check if trigger matches message based on match type"""
        try:
            if match_type == 'exact':
                return message.strip() == trigger
            elif match_type == 'starts_with':
                return message.startswith(trigger)
            elif match_type == 'ends_with':
                return message.endswith(trigger)
            elif match_type == 'regex':
                return bool(re.search(trigger, message, re.IGNORECASE))
            elif match_type == 'word':
                # Match whole word only
                pattern = r'\b' + re.escape(trigger) + r'\b'
                return bool(re.search(pattern, message, re.IGNORECASE))
            else:  # default to 'contains'
                return trigger in message
        except re.error as e:
            logger.error(f'Regex error for trigger "{trigger}": {e}')
            return False
        except Exception as e:
            logger.error(f'Error matching trigger "{trigger}": {e}')
            return False
            
    def add_trigger(self, trigger: str, responses: List[str], match_type: str = 'contains') -> bool:
        """Add a new trigger configuration"""
        try:
            self.triggers[trigger] = {
                'responses': responses,
                'match_type': match_type,
                'enabled': True
            }
            self._save_config()
            logger.info(f'Added trigger: {trigger}')
            return True
        except Exception as e:
            logger.error(f'Failed to add trigger: {e}')
            return False
            
    def remove_trigger(self, trigger: str) -> bool:
        """Remove a trigger configuration"""
        try:
            if trigger in self.triggers:
                del self.triggers[trigger]
                self._save_config()
                logger.info(f'Removed trigger: {trigger}')
                return True
            return False
        except Exception as e:
            logger.error(f'Failed to remove trigger: {e}')
            return False
            
    def _save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['triggers'] = self.triggers
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f'Failed to save config: {e}')

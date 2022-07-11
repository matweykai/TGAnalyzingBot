import os


class BotConfig:
    """Stores bot configuration"""
    api_id = None
    api_hash = None
    db_str = None

    def __setattr__(self, key: str, value: any):
        """Checks if attribute exists and sets it"""
        key = key.strip().lower()
        value = value.strip()

        if hasattr(self, key):
            self.__dict__[key] = value
        else:
            raise AttributeError(f"Wrong configuration attribute!({key})")

    def __repr__(self):
        """Object string representation"""
        result = 'BotConfig('

        for (key, value) in self.__dict__.items():
            result += f'{key}={value}, '

        return result[:-2] + ')'


bot_config = BotConfig()
# Reading .env file
with open(os.path.join(os.path.join(os.getcwd(), os.pardir), '.env'), 'rt', encoding='utf8') as env_file:
    for line in env_file:
        # Getting configuration attribute and it's value
        key, value = line.split('=')
        bot_config.__setattr__(key, value)

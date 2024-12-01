import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    TWITTER_BEARER_TOKEN: str
    TWITTER_API_KEY: str
    TWITTER_API_KEY_SECRET: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN_SECRET: str
    OPENAI_API_KEY: str
    MAX_TWEET_LENGTH: int = 280
    DEFAULT_TWEET_COUNT: int = 5

def load_config() -> Config:
    load_dotenv()
    
    return Config(
        TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN"),
        TWITTER_API_KEY=os.getenv("TWITTER_API_KEY"),
        TWITTER_API_KEY_SECRET=os.getenv("TWITTER_API_KEY_SECRET"),
        TWITTER_ACCESS_TOKEN=os.getenv("TWITTER_ACCESS_TOKEN"),
        TWITTER_ACCESS_TOKEN_SECRET=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    ) 
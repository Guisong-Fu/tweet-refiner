from typing import List, Optional
import tweepy
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from .config import Config
from prompt import SYSTEM_MESSAGE, TWEET_PROMPT


class TweetRefiner:
    def __init__(self, twitter_client: tweepy.Client, llm: ChatOpenAI, config: Config):
        self.twitter_client = twitter_client
        self.llm = llm
        self.config = config

    def get_recent_tweets(self, count: Optional[int] = None) -> List[str]:
        """Fetch recent original tweets for style examples."""
        if count is None:
            count = self.config.DEFAULT_TWEET_COUNT
            
        user = self.twitter_client.get_me()
        tweets = self.twitter_client.get_users_tweets(
            id=user.data.id,
            max_results=count,
            exclude=['retweets', 'replies']
        )
        return [tweet.text for tweet in tweets.data] if tweets.data else []

    def refine_tweet(self, text: str, style_examples: List[str], additional_instructions: Optional[str] = None) -> str:
        """Refine the input text using the LLM."""
        prompt = ChatPromptTemplate(
            [
                ("system", SYSTEM_MESSAGE),
                ("human", TWEET_PROMPT),
                MessagesPlaceholder("additional_instructions")
            ]
        )

        chain = prompt | self.llm

        formatted_prompt = prompt.format(
            original_tweet=text,
            previous_tweets=[],
            additional_instructions=["Additional instructions"],
            max_length=self.config.MAX_TWEET_LENGTH  # Use config value
        )
        print("Final Prompt:")
        print(formatted_prompt)

        response = chain.invoke({
            "original_tweet": text, 
            "previous_tweets": [], 
            "additional_instructions": [],
            "max_length": self.config.MAX_TWEET_LENGTH  # Use config value
        })

        return response.content

    def post_tweet(self, text: str) -> bool:
        """Post the refined tweet to Twitter."""
        if len(text) > self.config.MAX_TWEET_LENGTH:  # Use config value
            print(f"Tweet exceeds maximum length of {self.config.MAX_TWEET_LENGTH} characters")
            return False
            
        try:
            self.twitter_client.create_tweet(text=text)
            return True
        except Exception as e:
            print(f"Error posting tweet: {str(e)}")
            return False
from typing import List, Optional
import tweepy
from langchain.prompts import ChatPromptTemplate
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

    def refine_tweet(self, text: str, previous_tweets: List[str], additional_instructions: Optional[str] = None) -> str:
        """Refine the input text using the LLM."""
        # Create base messages without the placeholder
        messages = [
            ("system", SYSTEM_MESSAGE),
            ("human", TWEET_PROMPT),
        ]
        
        # Add additional instructions as a separate human message if provided
        if additional_instructions:
            messages.append(("human", additional_instructions))
            
        prompt = ChatPromptTemplate(messages)

        chain = prompt | self.llm

        formatted_prompt = prompt.format(
            original_tweet=text,
            previous_tweets=previous_tweets,
            max_length=self.config.MAX_TWEET_LENGTH  # Use config value
        )
        print("Final Prompt:")
        print(formatted_prompt)


        response = chain.invoke({
            "original_tweet": text, 
            "previous_tweets": previous_tweets, 
            "max_length": self.config.MAX_TWEET_LENGTH  # Use config value
        })

        return response.content

    def _create_thread_chunks(self, text: str) -> List[str]:
        """Split text into chunks suitable for a thread."""
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            thread_suffix_space = len(f" ({len(chunks) + 1} of X)")
            new_length = current_length + len(word) + (1 if current_chunk else 0)
            
            if new_length + thread_suffix_space <= self.config.MAX_TWEET_LENGTH:
                if current_chunk:
                    current_length += 1
                current_chunk.append(word)
                current_length += len(word)
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

    def post_tweet(self, text: str) -> bool:
        """
        Post text to Twitter, automatically handling single tweets and threads.
        Returns True if successful, False otherwise.
        """
        try:
            # Single tweet case
            if len(text) <= self.config.MAX_TWEET_LENGTH:
                self.twitter_client.create_tweet(text=text)
                print(f"Posting single tweet: {text}")
                return True
                
            # Thread case
            chunks = self._create_thread_chunks(text)
            
            for chunk in chunks:
                print(f"Posting chunk: {chunk}")

            # Post first tweet
            first_tweet = chunks[0] + f" (1 of {len(chunks)})"
            response = self.twitter_client.create_tweet(text=first_tweet)
            previous_tweet_id = response.data['id']
            
            # Post replies
            for i, chunk in enumerate(chunks[1:], 2):
                tweet_text = chunk + f" ({i} of {len(chunks)})"
                response = self.twitter_client.create_tweet(
                    text=tweet_text,
                    in_reply_to_tweet_id=previous_tweet_id
                )
                previous_tweet_id = response.data['id']
                
            return True
            
        except Exception as e:
            print(f"Error posting tweet/thread: {str(e)}")
            return False
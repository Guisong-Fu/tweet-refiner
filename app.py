import streamlit as st
from langchain_openai import ChatOpenAI
import tweepy
from src.tweet_refiner import TweetRefiner
from src.config import load_config

def initialize_clients():
    """Initialize Twitter and OpenAI clients."""
    config = load_config()
    
    # Twitter client
    twitter_client = tweepy.Client(
        bearer_token=config.TWITTER_BEARER_TOKEN,
        consumer_key=config.TWITTER_API_KEY,
        consumer_secret=config.TWITTER_API_KEY_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
    )
    
    # OpenAI client
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        api_key=config.OPENAI_API_KEY
    )
    
    return TweetRefiner(twitter_client, llm, config)

def main():
    st.title("Tweet Refiner")
    
    # Initialize the refiner
    refiner = initialize_clients()
    
    # Initialize session state variables if they don't exist
    if "previous_tweets" not in st.session_state:
        st.session_state["previous_tweets"] = [""]
    if "refined_results" not in st.session_state:
        st.session_state["refined_results"] = []
    if "show_refine_button" not in st.session_state:
        st.session_state["show_refine_button"] = True
    
    # Input area for original text
    original_text = st.text_area("Enter your text:", height=100)
    
    # Show Refine button only if it hasn't been clicked yet
    if st.session_state["show_refine_button"]:
        if st.button("Refine"):
            if original_text:
                with st.spinner('Refining your tweet...'):
                    refined_text = refiner.refine_tweet(
                        original_text,
                        st.session_state["previous_tweets"],
                        None
                    )
                    st.session_state["refined_results"].append(refined_text)
                    st.session_state["show_refine_button"] = False
                st.rerun()
    
    # Display all refined results
    for i, result in enumerate(st.session_state["refined_results"]):
        st.subheader(f"Refined Tweet {i+1}:")
        st.write(result)
        
        # Show additional refinement options only for the latest result
        if i == len(st.session_state["refined_results"]) - 1:
            additional_instructions = st.text_input(
                "Additional refinement instructions (optional):",
                key=f"additional_instructions_{i}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Refine Again", key=f"refine_again_{i}"):
                    with st.spinner('Refining your tweet...'):
                        refined_text = refiner.refine_tweet(
                            result,
                            st.session_state["previous_tweets"],
                            additional_instructions
                        )
                        st.session_state["refined_results"].append(refined_text)
                    st.rerun()
            
            with col2:
                if st.button("Approve and Post", key=f"approve_{i}"):
                    refiner.post_tweet(result)
                    # Reset the state after approval
                    st.session_state["refined_results"] = []
                    st.session_state["show_refine_button"] = True
                    st.rerun()

if __name__ == "__main__":
    main() 
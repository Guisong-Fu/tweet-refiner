# Tweet Refiner

Tweet Refiner is a Streamlit application that helps users refine and improve their tweets using OpenAI's GPT-4 model before posting them to Twitter. The app provides an intuitive interface for iterative refinement and maintains the user's writing style.

## Features

- Simple text input interface for drafting tweets
- AI-powered tweet refinement using GPT-4
- Interactive refinement process with optional additional instructions
- Multiple refinement iterations supported
- Direct posting to Twitter (after user approval)
- Character limit validation (280 characters)
- Maintains writing style consistency

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)
- Twitter Developer Account with API credentials
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Guisong-Fu/tweet-refiner.git
cd tweet-refiner
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Copy the `.env.example` file to `.env` and fill in your API credentials:
```env
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_KEY_SECRET=your_api_key_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the Streamlit application:
```bash
poetry run streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Using the application:
   - Enter your tweet text in the input area
   - Click "Refine" to get an AI-improved version
   - Review the refined tweet
   - Optionally add specific instructions and click "Refine Again" for further improvements
   - Click "Approve and Post" when satisfied to post the tweet

## Project Structure

```
tweet-refiner/
├── app.py              # Main Streamlit application
├── src/
│   ├── tweet_refiner.py    # Core refinement logic
│   ├── config.py           # Configuration management
│   └── prompt.py           # LLM prompt templates
├── pyproject.toml      # Poetry project configuration
├── .env               # Environment variables (not in repo)
└── README.md          # Project documentation
```

## Configuration

The application uses a configuration system that allows customization of various parameters:

- Maximum tweet length (default: 280 characters)
- Default number of example tweets to fetch (default: 5)
- API credentials (via environment variables)

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Testing

To run the test suite:
```bash
poetry run pytest
```

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by OpenAI's GPT-4o-mini
- Uses Twitter API v2 via [Tweepy](https://www.tweepy.org/)
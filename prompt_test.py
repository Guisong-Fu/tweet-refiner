from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_MESSAGE, TWEET_PROMPT

load_dotenv()

# examples = "\n".join([f"- {tweet}" for tweet in style_examples])

# if additional_instructions:
#     user_prompt += f"\nAdditional instructions: {additional_instructions}"


tweet = "Hello hello, I'm excited to announce that I'm launching a new product today!"

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


# prompt_template = ChatPromptTemplate(
#     [("system", "You are a helpful assistant"), MessagesPlaceholder("msgs")]
# )

# prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})


prompt = ChatPromptTemplate(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", TWEET_PROMPT),
        # MessagesPlaceholder("previous_tweets"),
        MessagesPlaceholder("additional_instructions")
    ]
)


# chain = prompt | llm.with_structured_output(ContentSummaryResponse)

chain = prompt | llm

# Before invoking the chain, print the formatted prompt
formatted_prompt = prompt.format(
    original_tweet=tweet,
    previous_tweets=[],
    additional_instructions=["Additional instructions"]
)
print("Final Prompt:")
print(formatted_prompt)

response = chain.invoke({"original_tweet": tweet, "previous_tweets": [], "additional_instructions": []})

print(response.content)

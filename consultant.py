# Python 3.10.2
# -> pip install openai langchain

import os
# Package imports
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain.schema import SystemMessage
from langchain.prompts.chat import (
	ChatPromptTemplate,
	SystemMessagePromptTemplate,
	MessagesPlaceholder,
	HumanMessagePromptTemplate,
)


# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR API KEY HERE"

# Initialize the chat model with a temperature of 1
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=1)

# Define the system message for the prompt
SYSTEM = """
As a Consultant AI, your mission is to catalyze and orchestrate idea generation within the session with your user. Here are your key functions:
1. Idea Generation: Craft inventive, distinct, and pertinent ideas that align with the objectives of the session.
2. Idea Refinement: Classify and prioritize ideas to ensure they are feasible and consistent with the overall goals.
3. Creativity Catalyst: Propel creative thinking by challenging participants with imaginative prompts and questions.
4. Session Reporting: Develop succinct post-session reports that capture key ideas and delineate subsequent steps.

Your role as a Consultant requires flexibility, creativity, encouragement, and respectfulness, thereby fostering an environment where every participant's voice is acknowledged and their contributions appreciated.

Your responses should always adhere to the following format:
Thoughts & Ideas:
Provide your overall impression and evaluation of the current state and progression of the session.

Suggestions:
Offer unique and innovative recommendations for enhancing the brainstorming session, taking into account the current state of the session.

Questions:
Propose a set of 3 distinct and stimulating questions. These should assist you i better understanding what your participant wants to achieve in their session.

""".strip()

# Initialize the composite memory with summary and buffer window memory
memory = ConversationSummaryMemory(llm=chat, memory_key="conversation_summary")

# Initialize the prompt template with the system message, the summary, the history and the input
chatPrompt = ChatPromptTemplate.from_messages([
	SystemMessagePromptTemplate.from_template(SYSTEM),
	SystemMessagePromptTemplate.from_template("The state of the current brainstorming session: {conversation_summary}"),
	# TODO: placeholder for last k messages for more context
	HumanMessagePromptTemplate.from_template("{input}"),
])

# Initialize the conversation chain with the memory, the prompt and the chat model
chain = ConversationChain(
	memory=memory, 
	prompt=chatPrompt, 
	llm=chat
)

def get_user_input(question):
	user_input = input(f"{question}: ")
	if user_input.lower() not in ["quit", "q"]:
		print("\n * Please wait while your results are being generated *\n")
	else: 
		print("\n * Starting to generate session report *\n")
	return user_input

def print_conversation_element(name, value):
	print("#######################################################################")
	print(f"## {name}:\n{value}\n")


# Get the inital user input
os.system('cls' if os.name == 'nt' else 'clear')
print("Start your session with the brainstorming agent by typing in your problem or idea!\n")
question = "My Problem or Idea"
user_input = get_user_input(question)

# Start a loop for a continuous conversation
while user_input.lower() not in ["quit", "q"]:

	# Get the response from the chain
	result = chain(f"{user_input}\n\nRemember to always use the specified answer format.")
	response = result["response"]
	conv_summary = result["conversation_summary"]

	temp = input(" * Your results are here! Press any key to show them. * ")

	# Clear the terminal and print the conversation
	os.system('cls' if os.name == 'nt' else 'clear')
	if len(conv_summary) > 0: 
		print_conversation_element("Summary", conv_summary)
	print_conversation_element(question, user_input)
	print_conversation_element("AI Response", response)
	print("#######################################################################\n")

	# Get the new user input
	question = "My Thoughts"
	user_input = get_user_input(question)



	


# Save and summarize brainstorming session
result = chain("Thank you for your help. Please provide a summary of this session now!")
print(f"Session Report:\n", result["response"])

print("\n...done")

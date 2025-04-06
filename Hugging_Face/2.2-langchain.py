import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
#from langchain.llms import HuggingFacePipeline <--deprecated
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load the model and tokenizer locally
model_name = "google/flan-t5-large"  # You can also use "google/flan-t5-xl"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create a text generation pipeline
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,  # Uses lower precision for efficiency
    device=0 if torch.cuda.is_available() else -1  # Use GPU if available
)

llm = HuggingFacePipeline(pipeline=pipe)

# Define prompt template
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Example questions
questions = [
    "Explain the concept of black holes in simple terms.",
    "What are the main causes of climate change, and how can we address them?",
    "Provide a brief overview of the history of artificial intelligence."
]

# Run model for each question
for question in questions:
    response = llm_chain.run(question)
    print(f"Q: {question}\nA: {response}\n")


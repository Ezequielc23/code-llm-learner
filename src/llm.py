from langchain.llms import HuggingFacePipeline
from transformers import pipeline

def setup_llm(model_name="codellama/CodeLlama-13b-hf"):
    """Set up an LLM for code tasks."""
    hf_pipeline = pipeline("text-generation", model=model_name, device=0)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return llm

def modify_code(llm, context, instruction):
    """Ask LLM to suggest code changes based on context."""
    prompt = f"Given the following code context:\n{context}\n\nInstruction: {instruction}\n\nSuggest modifications:"
    response = llm(prompt, max_length=500)
    return response

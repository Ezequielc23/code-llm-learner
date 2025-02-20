import os
from openai import OpenAI

def setup_llm(api_key, model_name="grok-2-latest"):  # Default to grok-2-latest until Grok 3 is available
    """Set up the xAI API client."""
    os.environ["XAI_API_KEY"] = api_key
    client = OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1"
    )
    return client, model_name

def modify_code(client, model_name, context, instruction):
    """Ask the xAI API to suggest code changes based on context."""
    prompt = f"Given the following code context:\n{context}\n\nInstruction: {instruction}\n\nSuggest modifications:"
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Adjust as needed
        max_tokens=500,   # Adjust based on desired output length
        stream=False
    )
    return response.choices[0].message.content

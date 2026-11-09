import litellm

response = litellm.completion(
    model="ollama_chat/llama3.2:3b",
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    api_base="http://localhost:11434",
)
print(response.choices[0].message.content)
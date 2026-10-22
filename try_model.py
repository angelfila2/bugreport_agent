from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3.2",
    temperature=0,
)

response = model.invoke("Explain HTTP error 500 in one sentence.")
print(response.content)
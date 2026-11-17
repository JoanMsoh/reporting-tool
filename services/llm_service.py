from llama_index.llms.ollama import Ollama

llm = Ollama(
    model="qwen2.5:7b",
    request_timeout=120.0
)
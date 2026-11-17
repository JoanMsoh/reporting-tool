from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import PromptTemplate
from qdrant_client import QdrantClient
from llama_index.llms.ollama import Ollama

qa_prompt = PromptTemplate("""
You are Mwalimu Assist, an AI Policy Assistant for Mwalimu National DT Sacco.

You must answer ONLY using information contained in the supplied context.

Question:
{query_str}

Context:
{context_str}

Instructions:

1. Use ONLY the information contained in the Context section.

2. Do NOT use external knowledge, assumptions, or general information.

3. If the answer is not explicitly supported by the context, respond exactly with:

I could not find relevant information from existing policy documents please contact hr@

4. For definition or factual questions:
   - Provide a short direct answer in prose.
   - Do not use headings.
   - Do not use bullet points unless required.

5. For policy questions:
   - Provide a concise explanation.
   - Use bullet points only for important requirements, conditions, or restrictions.

6. For process, workflow, onboarding, procedure, application, or "how do I" questions:
   - Create a short bold heading.
   - Present the answer as numbered steps.
   - Each step must appear on its own line.

7. For requirement or eligibility questions:
   - Use bullet points.
   - Each requirement must appear on its own line.

8. Keep answers concise and professional.

9. Do not include source citations in the answer.
   Sources will be added by the application.

10. If the context contains only partial information:
    - Answer only using the information available.
    - Clearly state if further information is not available.

Answer:
""")

client = QdrantClient(
    url="http://localhost:6333"
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="company_policies"
)

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model,
)

llm = Ollama(
    model="qwen2.5:7b",
    request_timeout=300.0
)

query_engine = index.as_query_engine(
    similarity_top_k=2,
    llm=llm,
    text_qa_template = qa_prompt,
)
from pathlib import Path
import re

from pypdf import PdfReader

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Document
)

from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding
)

from llama_index.vector_stores.qdrant import (
    QdrantVectorStore
)

from qdrant_client import QdrantClient

BASE_DIR = Path(__file__).resolve().parents[2]

DOCS_DIR = BASE_DIR / "documents"

COLLECTION_NAME = "company_policies"

print(f"Scanning: {DOCS_DIR}")


documents = []

for pdf_file in DOCS_DIR.rglob("*.pdf"):

    print(f"\nProcessing: {pdf_file.name}")

    try:

        reader = PdfReader(str(pdf_file))

        full_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                full_text += page_text + "\n"

        print(
            f"Extracted {len(full_text)} characters"
        )

        # Split FAQ documents by question

        chunks = re.split(
            r'(?=Q:)',
             full_text
        )

        department = (
            pdf_file.parent.name
            if pdf_file.parent != DOCS_DIR
            else "General"
        )

        document_name = pdf_file.stem

        for chunk in chunks:

            chunk = chunk.strip()

            if not chunk:
                continue

            documents.append(
                Document(
                    text=chunk,

                    metadata={
                        "document_name":
                            document_name,

                        "department":
                            department,

                        "version":
                            "1.0",

                        "access_level":
                            "employee",

                        "source_file":
                            pdf_file.name,
                    }
                )
            )

    except Exception as e:

        print(
            f"Error reading {pdf_file.name}: {e}"
        )

print(
    f"\nTotal chunks created: {len(documents)}"
)

for doc in documents[:3]:

    print("\n" + "=" * 60)

    print(doc.metadata)

    print(doc.text[:500])


embed_model = HuggingFaceEmbedding(
    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)



client = QdrantClient(
    url="http://localhost:6333"
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME
)

storage_context = (
    StorageContext.from_defaults(
        vector_store=vector_store
    )
)

index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model,
    storage_context=storage_context
)

print(
    f"\nSuccessfully indexed "
    f"{len(documents)} chunks."
)
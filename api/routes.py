from fastapi import APIRouter
from app.models.schemas import QueryRequest
from app.rag.query_engine import query_engine

router = APIRouter()


@router.post("/ask")
def ask_question(payload: QueryRequest):

    # DETERMINE QUESTION TYPE

    question = payload.question.lower()

    process_keywords = [
        "how do",
        "how to",
        "steps",
        "process",
        "procedure",
        "workflow",
        "onboarding",
        "apply"
    ]

    question_type = "general"

    if any(
        keyword in question
        for keyword in process_keywords
    ):
        question_type = "process"

    # QUERY ENGINE


    response = query_engine.query(
        f"""
        Question Type: {question_type}

        Question:
        {payload.question}
        """
    )

    # EXTRACT SOURCES

    sources = []
    top_nodes = sorted(
    response.source_nodes,
    key=lambda x: x.score or 0,
    reverse=True
    )[:2]   

    for node in top_nodes:
        node.metadata.get("document_name")

        source = {
            "document": node.metadata.get(
                "document_name",
                "Unknown Document"
            ),
            "department": node.metadata.get(
                "department",
                ""
            ),
            "version": node.metadata.get(
                "version",
                ""
            )
        }

        if source not in sources:
            sources.append(source)

 
    # CALCULATE CONFIDENCE
 

    confidence = "Low"

    if response.source_nodes:

        scores = [
            node.score
            for node in response.source_nodes
            if node.score is not None
        ]

        if scores:

            max_score = max(scores)

            if max_score >= 0.85:
                confidence = "High"

            elif max_score >= 0.65:
                confidence = "Medium"

   # Response

    return {
        "answer": str(response),
        "confidence": confidence,
        "sources": sources
    }
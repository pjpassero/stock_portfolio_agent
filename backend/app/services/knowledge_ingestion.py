from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.database_connector import get_connection


load_dotenv()


client = OpenAI()

KNOWLEDGE_PATH = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

def load_knowledge():
    documents = []
    for file_path in KNOWLEDGE_PATH.glob("*.md"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        chunks = text_splitter.split_text(content)

        for chunk in chunks:
            documents.append({
                "content": chunk,
                "source": file_path.name
            })

    return documents



def create_embedding(text:str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def ingest_knowledge():

    documents = load_knowledge()

    print(f"Found {len(documents)} chunks")

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                DELETE FROM knowledge_chunks
            """)

            for document in documents:

                embedding = create_embedding(
                    document["content"]
                )

                cur.execute(
                    """
                    INSERT INTO knowledge_chunks (
                        content,
                        source,
                        embedding
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        document["content"],
                        document["source"],
                        embedding
                    )
                )

                print(
                    f"Ingested chunk from {document['source']}"
                )

    documents = load_knowledge()

    print(f"Found {len(documents)} chunks")

    for document in documents:

        embedding = create_embedding(
            document["content"]
        )

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO knowledge_chunk (
                        content,
                        source,
                        embedding
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        document["content"],
                        document["source"],
                        embedding
                    )
                )

        print(
            f"Ingested chunk from {document['source']}"
        )



if __name__ == "__main__":
    ingest_knowledge()
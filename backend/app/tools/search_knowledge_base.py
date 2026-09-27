from app.services.database_connector import get_connection
from langchain_core.tools import tool
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()



@tool
def search_knowledge(query:str):
    """
        Search Fintel's knowledge base to get better answers for the user. The internal documentation
        includes infromation about the scoring algorithm, calcualtion, and technology.
    
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    query_knowledge_base = """

        SELECT content FROM knowledge_chunk ORDER BY embedding <=> %s::vector LIMIT 2

    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query_knowledge_base,
                (query_embedding,)
            )

            results = cur.fetchall()

    return "\n\n".join(
        result[0]
        for result in results
    )
   
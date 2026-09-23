from app.states.fin_state import FinState
from app.services.database_connector import get_connection
from app.services.openai_chat_service import ask_fin

def chat_with_fin(state:FinState):
    message_history = []
    messages_query = """
        SELECT chat_id, created_at, content, role FROM message WHERE portfolio_id=%s ORDER BY created_at ASC
        """
    values = (state["portfolioId"],)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(messages_query, values)
            result = cur.fetchall()
        for row in result:
            message_history.append({
                "role": row[3],
                "content": row[2]
            })

    response = ask_fin(
        portfolio=state["portfolio"],
        level = state["interpretation_level"],
        metrics=state["metrics"],
        history=message_history,
        question=state["current_question"],
        portfolioId=state["portfolioId"]
    )      

    

   
    return {
        "newest_response":response
    }

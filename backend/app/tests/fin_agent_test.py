from app.agents.fin import app_fin_graph

result = app_fin_graph.invoke({
    "portfolioId":"a22d756b-df64-4380-a2f7-179f48179568",
    "current_question":"What is my portfolio_value?"
})


print(result)
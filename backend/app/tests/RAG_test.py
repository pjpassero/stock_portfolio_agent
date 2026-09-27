from app.tools.search_knowledge_base import search_knowledge

result = search_knowledge.invoke({
    "query":"How is Fintel Score calculated?"
})


print(result)
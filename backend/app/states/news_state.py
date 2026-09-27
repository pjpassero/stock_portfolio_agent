from typing import TypedDict


class NewsStates(TypedDict):
    portfolioId:str
    tickerList:list[str]
    news_summaries:dict[str, str] #ticker to summary
    sentiment_score:dict[str, float] #ticker to score

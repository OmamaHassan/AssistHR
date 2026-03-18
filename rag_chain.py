import os
from functools import lru_cache
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)
from chat_store import load_history, save_message


answer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are AssistHR, an intelligent HR assistant.
Answer ONLY from the context below.
If not found say: 'I could not find that information
in the uploaded documents.'
Always cite source and page number as given to you.

Context: {context}"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])


def format_docs(docs):
    if not docs:
        return "NO_RELEVANT_CONTEXT"
    return "\n\n".join(
        f"[Source: {doc.metadata.get('filename', 'unknown')} | "
        f"Page: {doc.metadata.get('page', 'N/A')}]\n"
        f"{doc.page_content}"
        for doc in docs
    )


def get_llm(model: str = "llama-3.1-8b-instant"):
    from langchain_groq import ChatGroq
    return ChatGroq(
        model      = model,
        api_key    = os.getenv("GROQ_API_KEY"),
        temperature= 0.2
    )

@lru_cache(maxsize=1)
def get_cached_retriever():
    from retriever import get_retriever
    return get_retriever(k=4)


def get_chain(model: str = "llama-3.1-8b-instant"):
    llm       = get_llm(model)
    retriever = get_cached_retriever()

    return (
        RunnablePassthrough.assign(
            context=RunnableLambda(
                lambda x: format_docs(
                    retriever.invoke(x["question"])
                )
            )
        )
        | answer_prompt
        | llm
        | StrOutputParser()
    )

def ask(
    question  : str,
    session_id: str,
    model     : str = "llama-3.1-8b-instant"
) -> str:
    try:
        response = get_chain(model).invoke({
            "question"    : question,
            "chat_history": load_history(session_id)
        })
        save_message(session_id, "human", question)
        save_message(session_id, "ai",    response)
        return response
    except Exception as e:
        return f"❌ Error getting answer: {str(e)}"

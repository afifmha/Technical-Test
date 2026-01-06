import random
from langgraph.graph import StateGraph, END
from app.core.interfaces import VectorStoreInterface as VectorStore

class RAGService:
    def __init__(self, store: VectorStore):
        self.store = store 
        self.workflow = self.build_graph() 

    def fake_embed(self, text: str):
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]

    def retrieve_document(self, state):
        query = state["question"]
        emb = self.fake_embed(query)
        results = self.store.search(emb)

        if not results:
             results = []
             
        state["context"] = results
        return state

    def answer_query(self, state):
        ctx = state["context"]
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state

    def build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self.retrieve_document)
        workflow.add_node("answer", self.answer_query)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def process_question(self, question: str):
        return self.workflow.invoke({"question": question})

    def add_document(self, text: str):
        emb = self.fake_embed(text)
        self.store.add_documents(text, emb)
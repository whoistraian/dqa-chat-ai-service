import os
from glob import glob
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class ChatService:
    def __init__(self) -> None:
        self.pdf_files = glob('app/uploads/*.pdf')
        self.pdfs = [
            PyPDFLoader(file).load_and_split()
            for file in self.pdf_files
        ]
        self.embedding_function = OllamaEmbeddings(
            model=os.getenv('EMBEDDING_MODEL')
        )
        self.vectorstore: Chroma = Chroma.from_documents(
            *self.pdfs, self.embedding_function
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 1})
        self.prompt = hub.pull(os.getenv('PROMPT'))
        self.llm = ChatOllama(model=os.getenv('CHAT_MODEL'), temperature=0)
        self.rag_chain = (
            {
                "context": self.retriever | self.__format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def __format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_rag_chain(self):
        return self.rag_chain

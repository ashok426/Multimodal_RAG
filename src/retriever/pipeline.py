from typing import List, Dict, Any

class RetrieverPipeline:
    def __init__(self, embedding_model, vectorstore, docstore, id_key="doc_id"):
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        self.docstore = docstore
        self.id_key = id_key

    def add_documents(self, summaries: List[str], contents: List[Any]):
        import uuid
        from langchain_core.documents import Document
        doc_ids = [str(uuid.uuid4()) for _ in contents]
        summary_docs = [
            Document(page_content=summary, metadata={self.id_key: doc_ids[i]})
            for i, summary in enumerate(summaries)
        ]
        self.vectorstore.add_documents(summary_docs)
        self.docstore.mset(list(zip(doc_ids, contents)))

    def create_multi_vector_retriever(self, text_summaries, texts, table_summaries, tables, image_summaries, images):
        from langchain.retrievers.multi_vector import MultiVectorRetriever
        retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.docstore,
            id_key=self.id_key,
        )
        if text_summaries:
            self.add_documents(text_summaries, texts)
        if table_summaries:
            self.add_documents(table_summaries, tables)
        if image_summaries:
            self.add_documents(image_summaries, images)
        return retriever
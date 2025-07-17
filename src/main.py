from ingestion.pipeline import IngestionPipeline
from retriever.pipeline import RetrieverPipeline
from image_processing.pipeline import ImageProcessor
from llm_output.pipeline import LLMOutputGenerator

def main():
    # Ingestion
    source_pdf = "/home/ashok/Multimodal_RAG/multimodal-rag-project/data/Bajaj-Finance-Ltd. - -Annual-Report-Analysis - -11072025_removed.pdf"
    ingestion = IngestionPipeline(source_pdf)
    ingestion.load_data()
    ingestion.process_data()
    data = ingestion.get_processed_data()

    # Embedding and Vectorstore setup
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.storage import InMemoryStore

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=512)
    vectorstore = Chroma(collection_name="MMRAG", embedding_function=embedding_model)
    docstore = InMemoryStore()

    # Retriever
    retriever_pipeline = RetrieverPipeline(embedding_model, vectorstore, docstore)
    retriever = retriever_pipeline.create_multi_vector_retriever(
        text_summaries=data["NarrativeText"] + data["ListItem"],
        texts=data["NarrativeText"] + data["ListItem"],
        table_summaries=[],  # Add your table summaries here
        tables=data["Table"],
        image_summaries=[],  # Add your image summaries here
        images=data["Image"]
    )

    # Example query
    query = "Can you give me a relative performance between bajfinance and sensex for the past one year between Jan-24 to May-25?"
    relevant_docs = retriever.invoke(query)
    print(relevant_docs)

    # Image Processing
    img_processor = ImageProcessor("/content/extracted_data/")
    img_base64_list, image_summaries = img_processor.generate_img_summaries(image_summarize_func, prompt)

    # LLM Output Generation
    llm_output = LLMOutputGenerator.img_prompt_func(data_dict)

if __name__ == "__main__":
    main()
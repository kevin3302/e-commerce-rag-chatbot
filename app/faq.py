import os
from dotenv import load_dotenv
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from groq import Groq

load_dotenv()

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
collection_name_faq = 'faqs'
chroma_client = chromadb.Client()
EF_MODEL = os.environ['EF_MODEL_NAME']
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EF_MODEL
)
groq_client = Groq()

def ingest_faq_data(path):
    '''
    This function ingests the csv data into the vector db
    Question is stored as vector embedding and answer as its metadata
    '''
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into Chromadb...")
        collection = chroma_client.create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{'answer':ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs, 
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ Data Successfully ingested into Chroma Collection: {collection_name_faq}")
    else:
        print(f"Collection: {collection_name_faq} already exist")

def get_relevant_qa(query):
    '''
    This function gets the relevant question embedding from the vector db
    The question is the embedding and the answer is present as metadata
    '''
    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def generate_answer(query, context):
    prompt = f"""
    Given the following question and context, generate answer based on the context only.
    If the answer is not found in the context. Kindly state "I don't know". Don't try to make up an answer.

    CONTEXT: {context}
    QUESTION: {query}
    """
    completion = groq_client.chat.completions.create(
        model = os.environ['GROQ_MODEL'],
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return completion.choices[0].message.content

def faq_chain(query):
    result = get_relevant_qa(query)
    context = "".join([r.get('answer') for r in result['metadatas'][0]])
    print(f"Context: {context}")
    answer = generate_answer(query, context)
    return answer

if __name__ == "__main__":
    # print(faqs_path)
    ingest_faq_data(faqs_path)
    query = "What's your policy on defective products?"
    answer = faq_chain(query)
    print("Answer: ", answer)
import streamlit as st
import fitz  
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone as PineconeVectorStore
import cohere
from uuid import uuid4
from langchain.document_loaders import PyPDFDirectoryLoader
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Set up API key
PINECONE_API_KEY = st.secrets["PINECONE"]["API_KEY"]
COHERE_API_KEY = st.secrets["COHERE"]["API_KEY"]


# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
embedder = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = 'qa-bot-index'
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
index = pc.Index(index_name)

# Create PineconeVectorStore
vector_store = PineconeVectorStore(index=index, embedding=embedder, text_key='page_content')

def load_pdf(file):
    """Load PDF content from a file-like object (BytesIO)."""
    documents = []
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page_num in range(pdf.page_count):
           page = pdf[page_num]
           text = page.get_text("text")
           metadata = {"page": page_num + 1}
           documents.append(Document(page_content=text, metadata=metadata))
    return documents

# Function to store PDFs in vector database
def store_pdfs_in_vectordatabase(files):
    text_doc = []
    documents=[]
    for file in files:
        documents.extend(load_pdf(file))

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    for doc in documents:
        chunks = text_splitter.split_text(doc.page_content)
        for chunk in chunks:
                new_doc = Document(page_content=str(chunk), metadata=doc.metadata)
                text_doc.append(new_doc)

    # Add the documents to the Pinecone vector store
    uuids = [str(uuid4()) for _ in range(len(text_doc))]
    vector_store.add_documents(documents=text_doc, ids=uuids)
    st.success(f"Files stored in Pinecone index: {index_name}")

def query_with_pdf(query):
    # Perform similarity search
    results = vector_store.similarity_search(query, k=1)

    # Combine the relevant documents into context
    context = "\n\n".join([result.page_content for result in results])
    
    # Initialize Cohere
    co = cohere.Client(COHERE_API_KEY)
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    response = co.generate(prompt=prompt, max_tokens=200, temperature=0.7)
    
    return response.generations[0].text.strip(), context

# Streamlit Interface
st.title("QA Bot 🤖 with PDF Upload")
st.subheader("Upload PDF Documents")

# File uploader for multiple PDF files
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if st.button("Upload and Process"):
    if uploaded_files:
        store_pdfs_in_vectordatabase(uploaded_files)
    else:
        st.warning("Please upload at least one PDF file.")

st.subheader("❓Ask a Question")
user_query = st.text_input("Enter your question here")

if st.button("🔍 Get Answer"):
    if user_query:
        answer,context = query_with_pdf(user_query)
        st.success('Retrieved Content:')
        st.write(context)
        st.success("Generated Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question to get an answer.")

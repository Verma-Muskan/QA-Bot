# QA Bot with Retrieval-Augmented Generation (RAG)

This project is a Question Answering (QA) bot developed using a Retrieval-Augmented Generation (RAG) approach. The bot is designed to retrieve relevant information from uploaded documents and provide coherent answers based on the content. The system is built with Python, leveraging a vector database (Pinecone) for efficient document embedding retrieval, and a generative model (e.g., Cohere API) to generate answers.

## Features

- **Document Upload**: Users can upload PDF documents for the bot to process.
- **Real-Time Query**: The bot can handle real-time questions based on the uploaded documents.
- **Interactive Interface**: Built using Streamlit, allowing users to interact with the bot easily.
- **Deployment with Docker**: Containerized for easy deployment.
- **Continuous Integration**: Configured with GitHub Actions for automated build and deployment.

## Getting Started

### Prerequisites

- **Docker**: Install Docker from [Docker's official website](https://docs.docker.com/get-docker/).
- **GitHub Account**: Required for GitHub Actions.
- **API Keys**: You will need API keys for Pinecone and Cohere. These can be added as secrets in GitHub.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Verma-Muskan/QA-Bot.git
   cd QA-Bot

2. **Build the Docker Image**:
   ```bash
   docker build -t qa-bot .

4. **Run the Docker Container**:
   ```bash
   docker run -p 8501:8501 qa-bot
   
5. **Deployment on Render**:
- **a.	Upload to GitHub**:
   
*	Push the code and Dockerfile to a GitHub repository.
- **b.	Render Deployment**:

* Create a new Web Service on Render, linking to the GitHub repository.
*	Choose Docker as the environment, and set environment variables for API keys.
*	Render automatically builds and deploys the Docker container from the Dockerfile.
*	After deployment, Render provides a URL where the bot can be accessed.


6. **Access the Application**:
Open a browser and go to https://qa-bot-371e.onrender.com/ to interact with the QA bot.


## Usage
* Upload a PDF document using the upload button.
* Enter your query in the input box.
* The bot will display the retrieved document content and generate an answer based on the query.

## Technologies Used
* Python: For backend processing.
* Pinecone: For vector storage and retrieval.
* Cohere API: For generating natural language answers.
* Streamlit: For building the interactive interface.
* Docker: For containerization.
* GitHub Actions: For CI/CD.

## Contributing
For major changes, please open an issue to discuss what you would like to change.

## Acknowledgments
Pinecone for providing vector search capabilities.
Cohere for natural language processing support.
Streamlit for the easy-to-use web interface.

## Contact
For any questions or issues, please open an issue in this repository or contact the maintainer at vmuskan.2303@gmail.com.

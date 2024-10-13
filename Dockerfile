# Start with the official Python image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirement.txt /app/requirement.txt
RUN pip install --no-cache-dir -r requirement.txt

RUN pip install --no-cache-dir langchain-community 

# Install PyMuPDF specifically (if not listed in requirements.txt)
RUN pip install PyMuPDF

# Copy the rest of the application code to the working directory
COPY . /app

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]

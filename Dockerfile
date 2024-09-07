# Dockerfile

# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Set the OpenAI API Key environment variable (not recommended for production)
ENV OPENAI_API_KEY=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

# Expose the Streamlit default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]

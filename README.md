# IRS Project - Information Retrieval System

This project is an Information Retrieval System that includes a web crawler, an indexing system, a search engine (fuzzy and semantic), and a RAG (Retrieval-Augmented Generation) component using Google Gemini.

## Features

- **Web Crawler:** Crawls specified seed URLs to build a document database.
- **Fuzzy Search:** Uses an inverted index stored in MongoDB.
- **Semantic Search:** Uses vector embeddings stored in Qdrant.
- **RAG:** Enhances search results with AI-generated responses using Google Gemini.
- **Web GUI:** A modern web interface to interact with the system.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- A Google API Key for Gemini. You can get one from the [Google AI Studio](https://aistudio.google.com/).

## Setup and Running

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd IRSProject
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

### Important Note on Startup

When you run the system for the first time, it will perform the following steps:
1. Initialize the MongoDB and Qdrant databases.
2. **Start the Crawler Pipeline:** The crawler is configured to fetch **2500 pages** by default.
3. **Wait for Completion:** You will need to wait until the crawler finishes processing all pages before the web application becomes accessible. This process can take a significant amount of time depending on your network speed and the sites being crawled.

The console will show "Crawler finished. Starting Web Application..." when it's ready.

4. **Access the Web GUI:**
   Once the crawler finishes, open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

- `crawler_pipeline.py`: The main entry point for the crawling and indexing process.
- `main.py`: The entry point for the web application.
- `Scripts/`: Database initialization scripts.
- `web_gui/`: Frontend and backend logic for the web interface.
- `contracts/`: Data models and shared interfaces.
- `rag/`: RAG system implementation.

## Tech Stack

- **Python 3.13**
- **MongoDB**: Stores documents and inverted index.
- **Qdrant**: Stores document embeddings for semantic search.
- **Google Gemini**: Powers the RAG and query improvement features.
- **Flask**: Serves the web interface.

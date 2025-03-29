# Hotel Booking Analytics and RAG System

## Overview
This project provides an analytical and retrieval-augmented generation (RAG) system for hotel bookings. It includes data collection, preprocessing, analytics, reporting, and a question-answering system powered by an open-source LLM.

## Features
- Data Collection & Preprocessing: Cleaning and structuring hotel booking datasets.
- Analytics & Reporting: Visualizing revenue trends, cancellation rates, lead times, and geographical distribution.
- Retrieval-Augmented Question Answering: Using FAISS, ChromaDB, or Weaviate for vector embeddings with an LLM backend.
- API Development: FastAPI-based endpoints for analytics and Q&A.
- Performance Evaluation: Measuring Q&A accuracy and API response times.
- Deployment: Packaged solution with documentation and test queries.

## Installation

### Prerequisites
- Python 3.11.9
- Virtual environment setup (optional but recommended)
- Dependencies listed in `requirements.txt`

### Steps
1. Clone the repository:

   git clone https://github.com/yourusername/hotel-booking-analytics.git
   cd hotel-booking-analytics

2. Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:

   pip install -r requirements.txt
 
4. Run the API:

   uvicorn api:app --reload


## Usage

### API Endpoints
- Analytics
  - `GET /analytics/revenue-trends`
  - `GET /analytics/cancellation-rates`
  - `GET /analytics/geographical-distribution`
- Q&A System
  - `POST /query` with JSON payload:

    { "question": "What is the average booking lead time?" }
    

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make changes and commit.
4. Open a pull request.

## License
This project is licensed under the MIT License.


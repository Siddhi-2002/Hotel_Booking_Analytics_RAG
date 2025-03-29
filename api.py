from fastapi import FastAPI, HTTPException, Query
from retrieval import query_system  # Make sure this matches exactly
import uvicorn

app = FastAPI()

@app.post("/ask")
async def ask_question(
    question: str = Query(..., description="The question to answer")  # Now accepts ?question= in POST
):

    return {
        "question": question,
        "answer": f"Processed: {question}",
        "status": "success"
    }

@app.get("/ask")
async def ask_question(question: str): 
    return {"question": question, "answer": "Test response", "status": "success"}

@app.get("/")
def home():
    return {"message": "Hotel Booking API is running"}

@app.get("/analytics")
async def get_analytics():
    """Get basic dataset analytics"""
    try:
        from hotel_bookings import HotelBookingAnalyzer
        analyzer = HotelBookingAnalyzer()
        
        if not analyzer.prepared_data:
            raise HTTPException(status_code=503, detail="Data not loaded properly")
        
        return {
            "status": "success",
            "data": {
                "total_bookings": len(analyzer.df),
                "insights": analyzer.data_insights.split('\n')
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(question: str):
    """Answer questions about hotel bookings"""
    try:
        answer = query_system(question)
        return {
            "question": question,
            "answer": answer,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
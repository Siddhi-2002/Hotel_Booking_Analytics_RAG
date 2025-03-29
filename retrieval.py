import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_community.llms import Ollama
from hotel_bookings import HotelBookingAnalyzer

# Initialize analyzer instance
analyzer = HotelBookingAnalyzer()
llm = Ollama(model="mistral")
# retrieval.py
from langchain_community.llms import Ollama
from hotel_bookings import HotelBookingAnalyzer

# Initialize the analyzer and LLM
analyzer = HotelBookingAnalyzer()
llm = Ollama(model="mistral")

def query_system(question: str):
    try:
        # First try direct data answer
        data_answer = analyzer.get_data_answer(question)
        if data_answer:
            return data_answer
        
        # Fall back to LLM
        prompt = f"""Hotel Bookings Data Insights:
        {analyzer.data_insights}
        
        Question: {question}
        
        Answer based on the data."""
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error: {str(e)}"
    
class HotelBookingAnalyzer:
    def __init__(self, file_path="cleaned_hotel_bookings.csv"):
        self.file_path = file_path
        self.df = self.load_data()
        self.llm = OllamaLLM(model="mistral")
        self.prepared_data = False
        
        if self.df is not None:
            self.prepare_data()
            self.data_insights = self.generate_insights()
            self.prepared_data = True

    def load_data(self):
        """Load the CSV data into a DataFrame"""
        try:
            return pd.read_csv(self.file_path)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def prepare_data(self):
        """Prepare the data by converting dates and creating useful columns"""
        if 'arrival_date' in self.df.columns:
            self.df['arrival_date'] = pd.to_datetime(self.df['arrival_date'])
            self.df['arrival_year'] = self.df['arrival_date'].dt.year
            self.df['arrival_month'] = self.df['arrival_date'].dt.month
            self.df['arrival_day'] = self.df['arrival_date'].dt.day

    def generate_insights(self):
        """Generate key insights about the data"""
        insights = []
        
        # Basic info
        insights.append(f"Dataset contains {len(self.df)} hotel bookings.")
        
        # Date range
        if 'arrival_date' in self.df.columns:
            date_range = f"Date range: {self.df['arrival_date'].min().strftime('%Y-%m-%d')} to {self.df['arrival_date'].max().strftime('%Y-%m-%d')}"
            insights.append(date_range)
        
        # Revenue stats
        if 'revenue' in self.df.columns:
            total_rev = f"Total revenue: ${self.df['revenue'].sum():,.2f}"
            avg_rev = f"Average booking revenue: ${self.df['revenue'].mean():,.2f}"
            insights.extend([total_rev, avg_rev])
        
        # Guest statistics
        guest_stats = []
        if 'adults' in self.df.columns:
            guest_stats.append(f"{self.df['adults'].sum()} adults")
        if 'children' in self.df.columns:
            guest_stats.append(f"{self.df['children'].sum()} children")
        if 'babies' in self.df.columns:
            guest_stats.append(f"{self.df['babies'].sum()} babies")
        
        if guest_stats:
            insights.append("Total guests: " + ", ".join(guest_stats))
        
        return "\n".join(insights)

    def get_data_answer(self, question):
        """Try to answer the question directly from the data"""
        question_lower = question.lower()
        
        # Booking count questions
        if any(phrase in question_lower for phrase in ["how many bookings", "number of bookings", "total bookings"]):
            return f"There are {len(self.df)} bookings in the dataset."
        
        # Revenue questions
        if 'revenue' in question_lower:
            if 'revenue' not in self.df.columns:
                return "Revenue data is not available in the dataset."
            
            # Time-specific revenue
            if 'july 2017' in question_lower and 'arrival_year' in self.df.columns:
                july_2017 = self.df[(self.df['arrival_year'] == 2017) & (self.df['arrival_month'] == 7)]
                total = july_2017['revenue'].sum()
                return f"The total revenue for July 2017 was ${total:,.2f}."
            
            # General revenue
            total = self.df['revenue'].sum()
            avg = self.df['revenue'].mean()
            return f"Total revenue: ${total:,.2f}. Average per booking: ${avg:,.2f}."
        
        # Date range questions
        if any(phrase in question_lower for phrase in ["date range", "time period", "when are the bookings"]):
            if 'arrival_date' in self.df.columns:
                min_date = self.df['arrival_date'].min().strftime('%Y-%m-%d')
                max_date = self.df['arrival_date'].max().strftime('%Y-%m-%d')
                return f"Bookings range from {min_date} to {max_date}."
            return "Date information is not available."
        
        # Guest questions
        if any(phrase in question_lower for phrase in ["how many guests", "number of guests", "total guests"]):
            guest_parts = []
            if 'adults' in self.df.columns:
                guest_parts.append(f"{self.df['adults'].sum()} adults")
            if 'children' in self.df.columns:
                guest_parts.append(f"{self.df['children'].sum()} children")
            if 'babies' in self.df.columns:
                guest_parts.append(f"{self.df['babies'].sum()} babies")
            
            if guest_parts:
                return "Total guests: " + ", ".join(guest_parts)
            return "Guest information is not available."
        
        return None

    def ask_question(self, question):
        """Answer a question about the hotel bookings data"""
        if not self.prepared_data:
            return "Data not properly loaded. Cannot answer questions."
        
        print(f"\nQuestion: {question}")
        
        # First try to get a direct data answer
        data_answer = self.get_data_answer(question)
        if data_answer is not None:
            print("Answer from data:", data_answer)
            return data_answer
        
        # If no direct answer, use the LLM with context
        prompt = f"""Hotel Bookings Data Insights:
        {self.data_insights}
        
        Question: {question}
        
        Answer the question based on the data above. If you don't know or the information isn't available, say so.
        Provide concise, factual answers and mention if you're making any assumptions."""
        
        llm_answer = self.llm.invoke(prompt)
        print("Answer from LLM:", llm_answer)
        return llm_answer

def main():
    analyzer = HotelBookingAnalyzer()
    
    if not analyzer.prepared_data:
        print("Failed to initialize analyzer. Check your data file.")
        return
    
    print("Hotel Booking Data Analyzer")
    print("Type 'exit' to quit\n")
    print("Some questions you might ask:")
    print("- What's the total revenue?")
    print("- How many bookings are there for July 2017?")
    print("- What's the average revenue per booking?")
    print("- How many guests are there in total?")
    print("- What date range does the data cover?\n")
    
    while True:
        question = input("\nWhat would you like to know?")
        
        if question.lower() in ['exit', 'quit']:
            break
        
        analyzer.ask_question(question)

if __name__ == "__main__":
    main()
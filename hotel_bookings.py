import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from langchain_community.llms import Ollama  # Use only one Ollama import

class HotelBookingAnalyzer:
    def __init__(self, file_path="cleaned_hotel_bookings.csv"):
        self.file_path = file_path
        self.df = self.load_data()
        self.llm = Ollama(model="mistral")  
        self.prepared_data = False
        
        if self.df is not None:
            self.prepare_data()
            self.data_insights = self.generate_insights()
            self.prepared_data = True
            
    def load_data(self):
        try:
            return pd.read_csv(self.file_path)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    def prepare_data(self):
        if 'arrival_date' in self.df.columns:
            self.df['arrival_date'] = pd.to_datetime(self.df['arrival_date'])
            self.df['arrival_year'] = self.df['arrival_date'].dt.year
            self.df['arrival_month'] = self.df['arrival_date'].dt.month

    def generate_insights(self):
        insights = []
        insights.append(f"Dataset contains {len(self.df)} hotel bookings.")
        return "\n".join(insights)

    def get_data_answer(self, question):
        question_lower = question.lower()
        if any(phrase in question_lower for phrase in ["how many bookings", "total bookings"]):
            return f"There are {len(self.df)} bookings in the dataset."
        return None


    # ... [keep all your existing methods unchanged] ...
def get_analytics():
    df = pd.read_csv("cleaned_hotel_bookings.csv")

    revenue_trend = df.groupby("arrival_date_month")["adr"].sum().to_dict()
    cancellation_rate = (df["is_canceled"].sum() / len(df)) * 100
    lead_time_distribution = df["lead_time"].describe().to_dict()

    return {
        "revenue_trend": revenue_trend,
        "cancellation_rate": cancellation_rate,
        "lead_time_distribution": lead_time_distribution,
    }

# Specify the CSV filename
csv_file = "hotel_bookings.csv"  # Ensure the file is in the same directory as this script

# Load dataset
df = pd.read_csv(csv_file)

# Display first few rows
print("First 5 rows of the dataset:")
print(df.head())

print("\nColumns in CSV file:")
print(df.columns.tolist())

# Data Cleaning
df.drop_duplicates(inplace=True)

# Check for missing values before cleaning
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Fill missing numerical values with the median
num_cols = df.select_dtypes(include=['number']).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill missing categorical values with the mode
cat_cols = df.select_dtypes(include=['object']).columns
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

# Verify missing values are handled
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Trim extra spaces from column names
df.columns = df.columns.str.strip()

# Convert categorical fields to lowercase
for col in cat_cols:
    df[col] = df[col].str.lower().str.strip()

# Save cleaned dataset for analysis
cleaned_csv_file = "cleaned_hotel_bookings.csv"
df.to_csv(cleaned_csv_file, index=False)
print(f"\nCleaned data saved successfully as {cleaned_csv_file}")

# Load cleaned dataset
df = pd.read_csv(cleaned_csv_file)

# Revenue Trends Over Time
df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
df["year_month"] = df["reservation_status_date"].dt.to_period("M")
revenue_trends = df.groupby("year_month")["adr"].sum()

# Plot revenue trends
plt.figure(figsize=(12, 5))
revenue_trends.plot(kind="line", marker="o", color="b")
plt.title("Revenue Trends Over Time")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Cancellation rate
cancellation_rate = df["is_canceled"].mean() * 100
print(f"\nCancellation Rate: {cancellation_rate:.2f}%")

# Geographical Distribution of Users
plt.figure(figsize=(12, 6))
sns.countplot(y=df["country"], order=df["country"].value_counts().index[:10], palette="coolwarm")
plt.title("Top 10 Countries by Booking Volume")
plt.xlabel("Number of Bookings")
plt.ylabel("Country")
plt.show()

# Booking Lead Time Distribution
plt.figure(figsize=(10, 5))
plt.hist(df["lead_time"], bins=30, color="skyblue", edgecolor="black")
plt.title("Booking Lead Time Distribution")
plt.xlabel("Days Before Arrival")
plt.ylabel("Number of Bookings")
plt.grid(True)
plt.show()

# Average Stay Duration
df["total_nights"] = df["stays_in_week_nights"] + df["stays_in_weekend_nights"]
avg_stay = df.groupby("customer_type")["total_nights"].mean()

plt.figure(figsize=(8, 5))
avg_stay.plot(kind="bar", color=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"])
plt.title("Average Stay Duration by Customer Type")
plt.xlabel("Customer Type")
plt.ylabel("Average Stay (Nights)")
plt.xticks(rotation=45)
plt.show()

# Seasonal Booking Trends
df["month"] = df["reservation_status_date"].dt.month
monthly_bookings = df["month"].value_counts().sort_index()

plt.figure(figsize=(10, 5))
monthly_bookings.plot(kind="bar", color="orange", edgecolor="black")
plt.title("Seasonal Booking Trends")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
plt.show()

# Save extended analytics
analytics = {
    "Most Popular Hotel Type": df["hotel"].value_counts().to_dict(),
    "Average Stay Duration": avg_stay.to_dict(),
    "Seasonal Trends": monthly_bookings.to_dict(),
    "Most Common Market Segment": df["market_segment"].value_counts().to_dict(),
    "Room Type Demand": df["assigned_room_type"].value_counts().to_dict(),
    "Cancellation Rate (%)": cancellation_rate,
    "Revenue Trends": {str(k): v for k, v in revenue_trends.items()}  # Convert Period to string
}

json_file = "hotel_analytics.json"
with open(json_file, "w") as f:
    json.dump(analytics, f, indent=4)

print(f"\nExtended Analytics saved successfully as {json_file}")


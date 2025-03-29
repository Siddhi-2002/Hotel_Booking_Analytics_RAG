import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load cleaned hotel data
df = pd.read_csv("cleaned_hotel_bookings.csv")

# Convert each row into a string format for embedding
df["text_data"] = df.apply(lambda row: f"Booking from {row['country']} for {row['hotel']} on {row['reservation_status_date']}. ADR: {row['adr']}, Canceled: {row['is_canceled']}", axis=1)

# Load a sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(df["text_data"].tolist())

# Create FAISS index
dimension = embeddings.shape[1]  # Number of features
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save FAISS index
faiss.write_index(index, "hotel_bookings.index")

# Save metadata (text data for retrieval)
df[["text_data"]].to_csv("hotel_metadata.csv", index=False)

print("Vector database created successfully!")

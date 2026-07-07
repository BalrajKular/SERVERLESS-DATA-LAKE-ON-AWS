import sys
import boto3
import pandas as pd
import io

# Configuration from job arguments
BUCKET = "serverless-project-bucket-balraj"
RAW_KEY = "raw/orders_raw.csv"
PROCESSED_KEY = "processed/orders_cleaned.csv"

s3 = boto3.client("s3")

# Extract: Read raw CSV from S3
response = s3.get_object(Bucket=BUCKET, Key=RAW_KEY)
df = pd.read_csv(io.BytesIO(response["Body"].read()))

print(f"Raw data: {len(df)} rows")

# Transform: Data quality checks
# 1. Remove rows with null values in critical columns
df = df.dropna(subset=["order_id", "customer_id", "quantity"])

# 2. Deduplicate by order_id (keep first occurrence)
df = df.drop_duplicates(subset=["order_id"], keep="first")

# 3. Ensure correct data types
df["order_id"] = df["order_id"].astype(int)
df["customer_id"] = df["customer_id"].astype(int)
df["quantity"] = df["quantity"].astype(int)
df["unit_price"] = df["unit_price"].astype(float)

# 4. Calculate derived column: revenue
df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)

print(f"Cleaned data: {len(df)} rows")
print(f"Removed {520 - len(df)} rows (nulls + duplicates)")

# Load: Write cleaned CSV back to S3
buffer = io.StringIO()
df.to_csv(buffer, index=False)
s3.put_object(Bucket=BUCKET, Key=PROCESSED_KEY, Body=buffer.getvalue())

print(f"Wrote cleaned data to s3://{BUCKET}/{PROCESSED_KEY}")
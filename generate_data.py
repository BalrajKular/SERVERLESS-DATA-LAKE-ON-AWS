import csv
import random
from datetime import datetime, timedelta

random.seed(42)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "USB Hub", "Desk Lamp"]
statuses = ["completed", "pending", "cancelled", "returned"]

rows = []
for i in range(1, 501):
    order_date = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 165))
    row = {
        "order_id": i,
        "customer_id": random.randint(1000, 1200),
        "product_name": random.choice(products),
        "quantity": random.randint(1, 5),
        "unit_price": round(random.uniform(9.99, 499.99), 2),
        "order_date": order_date.strftime("%Y-%m-%d"),
        "status": random.choice(statuses),
    }
    # Introduce nulls in ~5% of rows
    if random.random() < 0.05:
        row["quantity"] = ""
    if random.random() < 0.05:
        row["customer_id"] = ""
    rows.append(row)

# Introduce ~20 duplicate rows
for _ in range(20):
    rows.append(random.choice(rows[:480]).copy())

random.shuffle(rows)

with open("orders_raw.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "customer_id", "product_name", "quantity", "unit_price", "order_date", "status"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated orders_raw.csv with {len(rows)} rows (includes nulls and duplicates)")
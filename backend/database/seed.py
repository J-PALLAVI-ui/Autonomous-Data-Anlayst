import os
import json
import uuid
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.models import DatasetModel
from tools.dataset_profiler import profile_dataset
from tools.data_quality_checker import calculate_data_quality

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_sample_ecommerce():
    """Generate realistic E-Commerce sales dataset with trends, categories, and slight anomalies."""
    np.random.seed(42)
    n = 250
    
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=int(i * 1.4) + np.random.randint(0, 3)) for i in range(n)]
    
    categories = ["Technology", "Furniture", "Office Supplies", "Electronics"]
    sub_categories = {
        "Technology": ["Phones", "Accessories", "Laptops", "Software"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Art"],
        "Electronics": ["Monitors", "Audio", "Cameras", "Wearables"]
    }
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    segments = ["Consumer", "Corporate", "Home Office"]
    
    chosen_cat = np.random.choice(categories, n, p=[0.3, 0.25, 0.25, 0.2])
    chosen_sub = [np.random.choice(sub_categories[c]) for c in chosen_cat]
    chosen_regions = np.random.choice(regions, n, p=[0.4, 0.3, 0.2, 0.1])
    chosen_segments = np.random.choice(segments, n, p=[0.5, 0.3, 0.2])
    
    base_sales = {
        "Technology": 450,
        "Furniture": 320,
        "Office Supplies": 95,
        "Electronics": 280
    }
    
    quantities = np.random.randint(1, 10, n)
    discounts = np.random.choice([0.0, 0.1, 0.15, 0.2, 0.3], n, p=[0.4, 0.25, 0.15, 0.1, 0.1])
    
    sales = []
    profits = []
    for i in range(n):
        c = chosen_cat[i]
        q = quantities[i]
        d = discounts[i]
        unit_price = base_sales[c] * np.random.uniform(0.7, 1.4)
        s = round(unit_price * q * (1 - d), 2)
        # Margin roughly 15-30% minus discount impact
        margin = np.random.uniform(0.18, 0.32) - (d * 0.8)
        p = round(s * margin, 2)
        sales.append(s)
        profits.append(p)
        
    # Inject a couple realistic anomalies
    sales[12] = 9850.0  # Enterprise massive sale
    profits[12] = 3120.0
    sales[45] = 4200.0  # Heavy discount loss
    profits[45] = -1250.0
    
    df = pd.DataFrame({
        "Order_ID": [f"ORD-{2025000 + i}" for i in range(n)],
        "Order_Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Region": chosen_regions,
        "Category": chosen_cat,
        "Sub_Category": chosen_sub,
        "Customer_Segment": chosen_segments,
        "Quantity": quantities,
        "Discount": discounts,
        "Sales": sales,
        "Profit": profits
    })
    
    file_path = os.path.join(UPLOAD_DIR, "sample_ecommerce_sales.csv")
    df.to_csv(file_path, index=False)
    return file_path, "sample_ecommerce_sales.csv", df

def seed_sample_datasets():
    """Seed sample dataset in database if empty."""
    db: Session = SessionLocal()
    try:
        count = db.query(DatasetModel).count()
        if count == 0:
            file_path, filename, df = generate_sample_ecommerce()
            profile = profile_dataset(df)
            quality = calculate_data_quality(df)
            
            sample_dataset = DatasetModel(
                id=str(uuid.uuid4()),
                filename=filename,
                file_path=file_path,
                file_size_bytes=os.path.getsize(file_path),
                row_count=profile["row_count"],
                column_count=profile["column_count"],
                summary_json=json.dumps(profile),
                quality_score=quality["score"],
                quality_metrics_json=json.dumps(quality)
            )
            db.add(sample_dataset)
            db.commit()
            print("Successfully seeded sample dataset: 'sample_ecommerce_sales.csv'")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

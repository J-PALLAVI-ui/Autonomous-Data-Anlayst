import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATASETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_datasets")
os.makedirs(DATASETS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. E-Commerce Global Transactions (CSV)
# -------------------------------------------------------------
def generate_ecommerce_dataset(n=500):
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=int(i * 0.7) + np.random.randint(0, 3)) for i in range(n)]
    
    categories = ["Technology", "Furniture", "Office Supplies", "Electronics"]
    sub_categories = {
        "Technology": ["Laptops", "Smartphones", "Accessories", "Software", "Cloud Storage"],
        "Furniture": ["Ergonomic Chairs", "Executive Desks", "Bookcases", "Lamps", "Tables"],
        "Office Supplies": ["Paper", "Binders", "Envelopes", "Storage Boxes", "Pens"],
        "Electronics": ["4K Monitors", "Headphones", "Webcams", "Keyboards", "Microphones"]
    }
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    segments = ["Consumer", "Corporate", "Small Business"]
    priorities = ["Critical", "High", "Medium", "Low"]
    
    cat = np.random.choice(categories, n, p=[0.30, 0.25, 0.25, 0.20])
    sub = [np.random.choice(sub_categories[c]) for c in cat]
    reg = np.random.choice(regions, n, p=[0.40, 0.30, 0.20, 0.10])
    seg = np.random.choice(segments, n, p=[0.50, 0.30, 0.20])
    prio = np.random.choice(priorities, n, p=[0.15, 0.35, 0.35, 0.15])
    
    base_prices = {"Technology": 650, "Furniture": 380, "Office Supplies": 65, "Electronics": 240}
    quantities = np.random.randint(1, 12, n)
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30], n, p=[0.35, 0.25, 0.15, 0.10, 0.10, 0.05])
    
    sales, profits, shipping = [], [], []
    for i in range(n):
        c, q, d = cat[i], quantities[i], discounts[i]
        unit_price = base_prices[c] * np.random.uniform(0.75, 1.45)
        s = round(unit_price * q * (1 - d), 2)
        margin = np.random.uniform(0.18, 0.32) - (d * 0.85)
        p = round(s * margin, 2)
        ship = round(np.random.uniform(8.0, 45.0) + (q * 1.5), 2)
        sales.append(s)
        profits.append(p)
        shipping.append(ship)
        
    # Inject a few realistic outliers
    sales[14] = 14500.0   # Large enterprise server contract
    profits[14] = 4850.0
    sales[88] = 5200.0    # Bulk discount liquidation loss
    profits[88] = -1850.0
    
    df = pd.DataFrame({
        "Order_ID": [f"ORD-2025-{1000 + i}" for i in range(n)],
        "Order_Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Customer_ID": [f"CUST-{np.random.randint(100, 350)}" for _ in range(n)],
        "Customer_Segment": seg,
        "Region": reg,
        "Category": cat,
        "Sub_Category": sub,
        "Order_Priority": prio,
        "Quantity": quantities,
        "Discount": discounts,
        "Sales": sales,
        "Profit": profits,
        "Shipping_Cost": shipping
    })
    
    path = os.path.join(DATASETS_DIR, "ecommerce_transactions_2025.csv")
    df.to_csv(path, index=False)
    print("Created:", path, f"({len(df)} rows, {len(df.columns)} cols)")
    return path

# -------------------------------------------------------------
# 2. SaaS Customer Churn & Revenue (Excel .xlsx)
# -------------------------------------------------------------
def generate_saas_churn_excel(n=400):
    np.random.seed(101)
    start_date = datetime(2023, 6, 1)
    
    tiers = ["Starter", "Professional", "Business", "Enterprise"]
    contracts = ["Month-to-month", "One year", "Two year"]
    payments = ["Credit Card", "Bank Transfer", "Electronic Check"]
    
    chosen_tiers = np.random.choice(tiers, n, p=[0.40, 0.30, 0.20, 0.10])
    chosen_contracts = np.random.choice(contracts, n, p=[0.55, 0.25, 0.20])
    chosen_payments = np.random.choice(payments, n, p=[0.60, 0.25, 0.15])
    
    tenures = np.random.randint(1, 36, n)
    base_charges = {"Starter": 29.0, "Professional": 79.0, "Business": 199.0, "Enterprise": 499.0}
    
    monthly_charges = []
    total_spend = []
    support_tickets = []
    usage_hours = []
    adoption_scores = []
    churn = []
    
    for i in range(n):
        t = chosen_tiers[i]
        ten = tenures[i]
        c = chosen_contracts[i]
        
        charge = round(base_charges[t] + np.random.uniform(-5.0, 20.0), 2)
        monthly_charges.append(charge)
        total_spend.append(round(charge * ten * np.random.uniform(0.95, 1.05), 2))
        
        tickets = np.random.poisson(lam=2.0)
        support_tickets.append(tickets)
        
        usage = round(np.random.uniform(10.0, 120.0) + (ten * 1.5), 1)
        usage_hours.append(usage)
        
        adopt = round(np.random.uniform(40.0, 95.0), 1)
        adoption_scores.append(adopt)
        
        # Churn probability higher with high tickets, low tenure, and month-to-month
        p_churn = 0.20
        if c == "Month-to-month": p_churn += 0.20
        if tickets >= 4: p_churn += 0.25
        if ten < 6: p_churn += 0.15
        if adopt > 80: p_churn -= 0.25
        p_churn = max(0.05, min(0.90, p_churn))
        
        churn.append("Yes" if np.random.rand() < p_churn else "No")
        
    df = pd.DataFrame({
        "Customer_ID": [f"USR-{10000 + i}" for i in range(n)],
        "Subscription_Tier": chosen_tiers,
        "Contract_Type": chosen_contracts,
        "Payment_Method": chosen_payments,
        "Tenure_Months": tenures,
        "Monthly_Charges": monthly_charges,
        "Total_Spend": total_spend,
        "Support_Tickets": support_tickets,
        "Usage_Hours_Monthly": usage_hours,
        "Feature_Adoption_Score": adoption_scores,
        "Churn_Status": churn
    })
    
    path = os.path.join(DATASETS_DIR, "saas_churn_and_revenue.xlsx")
    df.to_excel(path, index=False, engine="openpyxl")
    print("Created:", path, f"({len(df)} rows, {len(df.columns)} cols)")
    return path

# -------------------------------------------------------------
# 3. Financial Loan Portfolio & Credit Risk (CSV)
# -------------------------------------------------------------
def generate_loan_dataset(n=450):
    np.random.seed(77)
    
    grades = ["Grade A", "Grade B", "Grade C", "Grade D", "Grade E"]
    home_ownership = ["MORTGAGE", "RENT", "OWN"]
    statuses = ["Fully Paid", "Current", "Charged Off"]
    
    ages = np.random.randint(22, 65, n)
    incomes = np.random.lognormal(mean=11.0, sigma=0.45, size=n).round(0)
    scores = np.random.normal(705, 50, n).astype(int)
    scores = np.clip(scores, 550, 850)
    
    loan_amounts = (np.random.uniform(5000, 35000, n) // 500) * 500
    emp_length = np.random.randint(0, 15, n)
    dti = np.random.uniform(5.0, 38.0, n).round(1)
    
    chosen_grades, interest_rates, loan_statuses = [], [], []
    for i in range(n):
        cs = scores[i]
        if cs >= 750: g, r = "Grade A", round(np.random.uniform(5.5, 8.5), 2)
        elif cs >= 700: g, r = "Grade B", round(np.random.uniform(8.5, 12.0), 2)
        elif cs >= 650: g, r = "Grade C", round(np.random.uniform(12.0, 16.5), 2)
        elif cs >= 600: g, r = "Grade D", round(np.random.uniform(16.5, 21.0), 2)
        else: g, r = "Grade E", round(np.random.uniform(21.0, 28.0), 2)
        
        chosen_grades.append(g)
        interest_rates.append(r)
        
        # Status
        p_default = 0.05 + (28.0 - r) * 0.005 if g in ["Grade D", "Grade E"] else 0.04
        loan_statuses.append("Charged Off" if np.random.rand() < p_default else np.random.choice(["Fully Paid", "Current"], p=[0.6, 0.4]))
        
    df = pd.DataFrame({
        "Loan_ID": [f"LN-2025-{5000 + i}" for i in range(n)],
        "Borrower_Age": ages,
        "Annual_Income": incomes,
        "Employment_Length_Years": emp_length,
        "Home_Ownership": np.random.choice(home_ownership, n, p=[0.50, 0.40, 0.10]),
        "Credit_Score": scores,
        "Loan_Amount": loan_amounts,
        "Interest_Rate": interest_rates,
        "Loan_Grade": chosen_grades,
        "Debt_To_Income_Ratio": dti,
        "Delinquencies_2Years": np.random.choice([0, 1, 2, 3], n, p=[0.82, 0.12, 0.04, 0.02]),
        "Loan_Status": loan_statuses
    })
    
    path = os.path.join(DATASETS_DIR, "financial_loan_portfolio.csv")
    df.to_csv(path, index=False)
    print("Created:", path, f"({len(df)} rows, {len(df.columns)} cols)")
    return path

# -------------------------------------------------------------
# 4. Healthcare Patient Vitals & Health Metrics (CSV)
# -------------------------------------------------------------
def generate_healthcare_dataset(n=350):
    np.random.seed(99)
    
    ages = np.random.randint(20, 80, n)
    gender = np.random.choice(["Male", "Female"], n)
    bmi = np.random.normal(27.5, 4.5, n).round(1)
    systolic = np.random.normal(125, 15, n).round(0)
    diastolic = np.random.normal(82, 10, n).round(0)
    glucose = np.random.normal(105, 25, n).round(0)
    cholesterol = np.random.normal(210, 35, n).round(0)
    smoking = np.random.choice(["Never", "Former", "Current"], n, p=[0.55, 0.25, 0.20])
    exercise_hours = np.random.uniform(0.0, 10.0, n).round(1)
    hospital_visits = np.random.choice([0, 1, 2, 3, 4], n, p=[0.60, 0.22, 0.10, 0.05, 0.03])
    
    # Risk
    risk = []
    for i in range(n):
        s_score = (systolic[i] - 120) / 15 + (glucose[i] - 100) / 25 + (ages[i] - 40) / 20
        risk.append("High" if s_score > 2.0 else ("Moderate" if s_score > 0.5 else "Low"))
        
    df = pd.DataFrame({
        "Patient_ID": [f"PAT-{8000 + i}" for i in range(n)],
        "Age": ages,
        "Gender": gender,
        "BMI": bmi,
        "Blood_Pressure_Systolic": systolic,
        "Blood_Pressure_Diastolic": diastolic,
        "Glucose_Level": glucose,
        "Cholesterol": cholesterol,
        "Smoking_Status": smoking,
        "Exercise_Hours_Weekly": exercise_hours,
        "Hospital_Visits_Past_Year": hospital_visits,
        "Cardiovascular_Risk": risk
    })
    
    path = os.path.join(DATASETS_DIR, "healthcare_patient_vitals.csv")
    df.to_csv(path, index=False)
    print("Created:", path, f"({len(df)} rows, {len(df.columns)} cols)")
    return path

if __name__ == "__main__":
    generate_ecommerce_dataset()
    generate_saas_churn_excel()
    generate_loan_dataset()
    generate_healthcare_dataset()

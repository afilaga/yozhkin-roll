
import pandas as pd
import re
from collections import Counter

# File paths
orders_file = '/Users/andreyfilatiev/Projects/Ёжкин ролл/Сайт/52b6fc490385d256aad5338ba8826e17.csv'
leads_file = '/Users/andreyfilatiev/Projects/Ёжкин ролл/Сайт/leads-b70a09ec02e2b95d5c890b74574e1e978225e2e9baf8c317071adf9c845fe252.csv'

def parse_orders(file_path):
    print(f"--- Analyzing Orders: {file_path} ---")
    try:
        df = pd.read_csv(file_path)
        
        # 1. Total Metrics
        total_revenue = df['amount'].sum()
        total_orders = len(df)
        aov = total_revenue / total_orders if total_orders > 0 else 0
        
        print(f"Total Revenue: {total_revenue:,.2f} RUB")
        print(f"Total Orders: {total_orders}")
        print(f"AOV: {aov:.2f} RUB")

        # 2. Delivery vs Pickup
        # Assuming 'delivery' column contains mode. Check unique values first in real run, but based on view_file:
        # Values like "Курьером", "улица ... = 0" (likely pickup or bug), "0"
        # Let's clean this up. If it contains "Курьером", it's delivery.
        
        def categorize_delivery(val):
            val = str(val).lower()
            if 'курьером' in val:
                return 'Delivery'
            return 'Pickup/Other'

        df['delivery_type'] = df['delivery'].apply(categorize_delivery)
        delivery_counts = df['delivery_type'].value_counts()
        print("\nDelivery Split:")
        print(delivery_counts)

        # 3. Top Products Parsing
        # Product string format: "Name - 1xPrice = Total; Name2..."
        all_products = []
        for prod_str in df['product'].dropna():
            # Split by semicolon for multiple items
            items = prod_str.split(';')
            for item in items:
                # Regex to extract name before " - "
                match = re.match(r'^\s*(.*?)\s-\s', item)
                if match:
                    product_name = match.group(1)
                    all_products.append(product_name)
        
        product_counts = Counter(all_products).most_common(10)
        print("\nTop 10 Products:")
        for rank, (name, count) in enumerate(product_counts, 1):
            print(f"{rank}. {name}: {count} orders")

        # 4. Repeat Customers (by Phone)
        repeat_customers = df['phone'].value_counts()
        print(f"\nRepeat Customers: {len(repeat_customers[repeat_customers > 1])} (out of {len(repeat_customers)} unique)")
        print("Top 5 Loyal Customers:")
        print(repeat_customers.head(5))

    except Exception as e:
        print(f"Error parsing orders: {e}")

def parse_leads(file_path):
    print(f"\n--- Analyzing Leads: {file_path} ---")
    try:
        # Using separator ';' based on file inspection
        df = pd.read_csv(file_path, sep=';')
        
        total_leads = len(df)
        print(f"Total Leads: {total_leads}")

        # 1. Payment Status (Conversion)
        # Column: "Статус оплаты"
        status_counts = df['Статус оплаты'].value_counts()
        print("\nPayment Status:")
        print(status_counts)
        
        paid_leads = df[df['Статус оплаты'].str.lower().isin(['оплачено', 'paid'])] 
        conversion_rate = (len(paid_leads) / total_leads) * 100 if total_leads > 0 else 0
        print(f"Calculated Paid Conversion Rate: {conversion_rate:.2f}%")

        # 2. UTM Sources
        if 'utm_source' in df.columns:
            utm_counts = df['utm_source'].value_counts()
            print("\nTop UTM Sources:")
            print(utm_counts.head(10))
        else:
            print("\nUTM Source column not found/empty.")

    except Exception as e:
        print(f"Error parsing leads: {e}")

if __name__ == "__main__":
    parse_orders(orders_file)
    parse_leads(leads_file)

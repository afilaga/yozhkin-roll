
import pandas as pd
import locale

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    pass

# File path
file_path = '/Users/andreyfilatiev/Projects/Ёжкин ролл/Сайт/52b6fc490385d256aad5338ba8826e17.csv'

def analyze_december():
    print("--- December 2025 Analysis ---")
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Convert date column
        df['created'] = pd.to_datetime(df['created'], errors='coerce')
        
        # Filter for December 2025
        start_date = '2025-12-01'
        end_date = '2025-12-31'
        mask = (df['created'] >= start_date) & (df['created'] <= end_date)
        dec_df = df.loc[mask].copy()
        
        # Basic Metrics
        total_orders = len(dec_df)
        total_revenue = dec_df['amount'].sum()
        
        if total_orders == 0:
            print("No orders found for December 2025.")
            return

        print(f"Total Orders (Dec): {total_orders}")
        print(f"Total Revenue (Dec): {total_revenue:,.2f} RUB")
        
        # Daily breakdown (to see if weekends are busier)
        dec_df['day_name'] = dec_df['created'].dt.day_name()
        day_counts = dec_df['day_name'].value_counts()
        
        print("\nOrders by Day of Week:")
        print(day_counts)
        
        # Peak Date
        dec_df['date_only'] = dec_df['created'].dt.date
        peak_date = dec_df['date_only'].value_counts().idxmax()
        peak_count = dec_df['date_only'].value_counts().max()
        print(f"\nPeak Date: {peak_date} ({peak_count} orders)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_december()


import pandas as pd
import locale

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    pass

file_path = '/Users/andreyfilatiev/Projects/Ёжкин ролл/Сайт/52b6fc490385d256aad5338ba8826e17.csv'

def analyze_anomalies():
    print("--- Volatility & Anomaly check ---")
    try:
        df = pd.read_csv(file_path)
        df['created'] = pd.to_datetime(df['created'], errors='coerce')
        df['date'] = df['created'].dt.date
        
        # 1. Daily Trend (Text Graph)
        daily = df.groupby('date')['amount'].sum().sort_index()
        
        print("\nDaily Revenue Trend (Ascii Graph):")
        max_rev = daily.max()
        if max_rev > 0:
            scale = 50 / max_rev
        else:
            scale = 1
            
        for date, revenue in daily.items():
            bar_len = int(revenue * scale)
            bar = '█' * bar_len
            print(f"{date}: {revenue:7,.0f} {bar}")

        # 2. Whale Orders (Outliers)
        # Definition: Orders > 2x AOV or arbitrary threshold like 7000 RUB
        whales = df[df['amount'] > 7000].sort_values('amount', ascending=False)
        print(f"\nWhale Orders (> 7,000 RUB): Found {len(whales)}")
        if not whales.empty:
            print(whales[['created', 'amount', 'product', 'phone']].head(5).to_string(index=False))

        # 3. Weekday vs Weekend AOV
        df['is_weekend'] = df['created'].dt.dayofweek >= 5 # 5=Sat, 6=Sun
        
        weekend_avg = df[df['is_weekend']]['amount'].mean()
        weekday_avg = df[~df['is_weekend']]['amount'].mean()
        
        print(f"\nAverage Check:")
        print(f"Weekends: {weekend_avg:.2f} RUB")
        print(f"Weekdays: {weekday_avg:.2f} RUB")
        
        if weekday_avg > weekend_avg:
             print("=> Insight: Weekdays check is HIGHER! (Likely office large orders?)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_anomalies()

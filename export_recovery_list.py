
import csv
import os
import re
from datetime import datetime

# Configuration
PROJECT_DIR = '/Users/andreyfilatiev/Projects/Ёжкин ролл/Сайт'
LEADS_FILE = os.path.join(PROJECT_DIR, 'leads.csv')
OUTPUT_FILE = os.path.join(PROJECT_DIR, 'recovery_list.csv')

def clean_phone(phone_str):
    """Normalize phone to +7 format."""
    if not phone_str:
        return None
    # Remove all non-digits
    digits = re.sub(r'\D', '', str(phone_str))
    
    if not digits:
        return None
        
    # Formatting
    if len(digits) == 11:
        if digits.startswith('8'):
            return '+7' + digits[1:]
        elif digits.startswith('7'):
            return '+' + digits
            
    if len(digits) == 10:
        return '+7' + digits
        
    return '+' + digits # Fallback

def export_recovery_list():
    print(f"--- Exporting Abandoned Carts for Recovery ---")
    
    if not os.path.exists(LEADS_FILE):
        print(f"Error: {LEADS_FILE} not found.")
        return

    leads_to_recover = []
    
    try:
        with open(LEADS_FILE, 'r', encoding='utf-8') as f: # Tilda exports are usually utf-8
            # Inspect delimiter
            sample = f.read(1024)
            f.seek(0)
            delimiter = ';' if sample.count(';') > sample.count(',') else ','
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                # Key columns (Tilda names vary, let's try common ones)
                # 'Status', 'Payment', 'Amount', 'Phone', 'Name', 'Created'
                
                # Check Status/Payment
                status = row.get('Status', '').lower()
                payment = row.get('Payment', '').lower()
                
                # We want "Failed" or "New" (Not Paid)
                is_paid = 'paid' in payment or 'оплач' in status or 'оплач' in payment
                if is_paid:
                    continue
                    
                # Extract Amount
                try:
                    amount = float(re.sub(r'[^\d.]', '', row.get('Amount', '0')))
                except:
                    amount = 0
                
                # Filter Low Value (optional, e.g. < 500 rub)
                if amount < 500:
                    continue
                    
                # Get Date
                date_str = row.get('Created', '')
                
                # Clean Phone
                raw_phone = row.get('Phone', '')
                clean_ph = clean_phone(raw_phone)
                
                if clean_ph:
                    leads_to_recover.append({
                        'Phone': clean_ph,
                        'Name': row.get('Name', 'Client'),
                        'Amount': amount,
                        'Date': date_str,
                        'Status': row.get('Status', 'Unknown') or row.get('Payment', 'Unknown')
                    })
                    
    except Exception as e:
        print(f"Error parsing csv: {e}")
        return

    # Sort by Amount (High value first)
    leads_to_recover.sort(key=lambda x: x['Amount'], reverse=True)
    
    # Save to CSV
    if leads_to_recover:
        with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as out:
            fieldnames = ['Phone', 'Name', 'Amount', 'Date', 'Status']
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads_to_recover)
            
        print(f"Success! Exported {len(leads_to_recover)} leads to {OUTPUT_FILE}")
        print("Top 5 High-Value Abandoned Carts:")
        for l in leads_to_recover[:5]:
            print(f"- {l['Name']}: {l['Amount']} RUB ({l['Phone']})")
    else:
        print("No leads found matching recovery criteria.")

if __name__ == "__main__":
    export_recovery_list()

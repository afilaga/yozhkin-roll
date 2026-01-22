import csv
import os
import re

# Helper to normalize phone for preview
def normalize_phone(p):
    d = re.sub(r'\D', '', str(p))
    if len(d) == 11 and d[0] in '78': return '+7' + d[1:]
    if len(d) == 10: return '+7' + d
    return p

def check_csv(filename):
    print(f"\n--- Checking {filename} ---")
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return False

    try:
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            # Auto-detect delimiter
            sample = f.read(2048)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                delimiter = dialect.delimiter
            except:
                delimiter = ',' # Fallback
            
            print(f"✅ Detected delimiter: '{delimiter}'")
            
            reader = csv.DictReader(f, delimiter=delimiter)
            headers = reader.fieldnames
            print(f"📋 Columns found: {', '.join(headers[:5])}...")

            # Check for Phone column
            phone_col = next((h for h in headers if 'phone' in h.lower() or 'телеф' in h.lower()), None)
            
            if phone_col:
                print(f"✅ Phone column matched: '{phone_col}'")
                # Show first 3 phones
                print("📞 Sample Phones (Normalized):")
                count = 0
                for row in reader:
                    original = row[phone_col]
                    clean = normalize_phone(original)
                    print(f"   {original} -> {clean}")
                    count += 1
                    if count >= 3: break
                return True
            else:
                print(f"⚠️ WARNING: Could not find a 'Phone' or 'Телефон' column automatically.")
                print(f"   Available columns: {headers}")
                return False

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    # Check for expected files
    print("SEARCHING FOR DATA FILES...")
    tilda_ok = check_csv("leads.csv")
    loyalty_ok = check_csv("loyalty.csv")  # Hypothetical name for loyalty DB export

    if tilda_ok and loyalty_ok:
        print("\n✅ READY FOR CROSS-ANALYSIS. Run the matching script next.")
    else:
        print("\n⚠️  MISSING DATA. Please put 'leads.csv' and 'loyalty.csv' in this folder.")

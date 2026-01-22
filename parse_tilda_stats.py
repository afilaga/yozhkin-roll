
import os
from bs4 import BeautifulSoup

# Files
# Try to find the correct path dynamically
base_project_dir = '/Users/andreyfilatiev/Projects'
# Search for the directory manually
stat_dir = None

def find_stats_dir():
    print(f"Searching in {base_project_dir}...")
    try:
        for root, dirs, files in os.walk(base_project_dir):
            if 'Statistics_tilda' in dirs:
                return os.path.join(root, 'Statistics_tilda')
            for d in dirs:
                 # Check for lenient match if encoding is weird
                 if 'Statistics_tilda' in d: # Simple substring check
                      return os.path.join(root, d)
            # Just check depth 2 to be safe
            if root.count(os.sep) - base_project_dir.count(os.sep) > 2:
                break
    except Exception as e:
        print(f"Error searching dirs: {e}")
    return '/Users/andreyfilatiev/Projects/Ёжкин ролл/Statistics_tilda' # Fallback

stat_dir = find_stats_dir()
print(f"Resolved Statistics Directory: {stat_dir}")
if stat_dir and os.path.exists(stat_dir):
    print(f"Contents of {stat_dir}:")
    print(os.listdir(stat_dir))
else:
    print("Statistics directory NOT FOUND.")

monthly_site = os.path.join(stat_dir, 'Статистика сайта - Ежкин ролл NEW - Tilda_per_month.html') if stat_dir else ""

def parse_stats():
    print("--- Parsing Tilda Monthly Stats ---")
    
    if os.path.exists(monthly_site):
        try:
             with open(monthly_site, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                
                # Find the main data rows
                rows = soup.find_all('tr', class_='data-row')
                print(f"Found {len(rows)} data rows.")
                
                print(f"{'Month':<15} | {'Sessions':<10} | {'Mobile %':<10} | {'Leads':<10} | {'CR %':<10}")
                print("-" * 65)
                
                for row in rows:
                    date_val = row.get('data-stat-date', 'Unknown')
                    
                    # Columns extraction (based on visual inspection of <td> order)
                    # 0: Name (Month)
                    # 1: Views
                    # 2: Sessions
                    # 3: Visitors
                    # 4: Desktop/Mobile (Complex html)
                    # 5: Leads
                    # 6: Conversion
                    
                    cols = row.find_all('td')
                    if len(cols) < 7: continue
                    
                    month_name = cols[0].get_text(strip=True)
                    sessions = cols[2].get_text(strip=True)
                    leads = cols[5].get_text(strip=True)
                    cr = cols[6].get_text(strip=True)
                    
                    # Extract Mobile % from 4th column spanning
                    # Structure: <span>12%</span><span style="color: #999999">&nbsp;/&nbsp;</span><span>88%</span>
                    # Usually Desktop / Mobile. So second span is Mobile? 
                    # Actually inspection shows: <img src="...desktop..."> / <img src="...mobile...">
                    # The text spans follow. 12% / 88%. 
                    # Let's assume right side is Mobile.
                    mob_text = "N/A"
                    device_spans = cols[4].find_all('span')
                    if len(device_spans) >= 3:
                         mob_text = device_spans[2].get_text(strip=True) # Index 0=Desk, 1=SEP, 2=Mob
                    
                    print(f"{month_name:<15} | {sessions:<10} | {mob_text:<10} | {leads:<10} | {cr:<10}")

        except Exception as e:
            print(f"Error reading site stats: {e}")

if __name__ == "__main__":
    parse_stats()

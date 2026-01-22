import json
import os
import re

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'PRODUCTION', 'data')
PAGES_DIR = os.path.join(BASE_DIR, 'PRODUCTION', 'pages')

CONFIG_FILE = os.path.join(DATA_DIR, 'pricing_config.json')
ZONES_FILE = os.path.join(BASE_DIR, 'PRODUCTION', 'delivery_zones.json')
HTML_FILE = os.path.join(BASE_DIR, 'PRODUCTION', 'delivery.html')


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    print("🚀 Starting Delivery Price Build...")

    # 1. Load Config
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        return
    
    config = load_json(CONFIG_FILE)
    print(f"✅ Loaded config with {len(config)} price groups.")

    # 2. Load GeoJSON
    if not os.path.exists(ZONES_FILE):
        print(f"❌ Zones file not found: {ZONES_FILE}")
        return

    zones_data = load_json(ZONES_FILE)
    print(f"✅ Loaded GeoJSON with {len(zones_data['features'])} features.")

    # 3. Update GeoJSON properties based on Config
    updates_count = 0
    
    # Create a lookup map for speed
    config_map = {}
    for group in config:
        for z_id in group['zone_ids']:
            config_map[z_id] = group

    for feature in zones_data['features']:
        f_id = feature['id']
        if f_id in config_map:
            group = config_map[f_id]
            
            # Formulate description string
            # Format: "Доставка Xр фиксированно\nМинимальная сумма заказа Yр"
            desc = f"Доставка {group['price']}р фиксированно\nМинимальная сумма заказа {group['min_order']}р"
            
            feature['properties']['description'] = desc
            feature['properties']['fill'] = group['color']
            feature['properties']['stroke'] = group['color']
            updates_count += 1

    print(f"🔄 Updated {updates_count} zones in memory.")

    # 4. Save updated GeoJSON
    save_json(ZONES_FILE, zones_data)
    print(f"💾 Saved updated {ZONES_FILE}")

    # 5. Inject into HTML
    if not os.path.exists(HTML_FILE):
        print(f"❌ HTML file not found: {HTML_FILE}")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Minify JSON for injection (remove newlines to avoid JS string issues if not careful, 
    # though standard JSON.stringify is safe, we want it single-ish line or clean)
    json_str = json.dumps(zones_data, ensure_ascii=False)

    # Regex to find the GEO_DATA object
    # const GEO_DATA = { ... };
    # using dotall to match across lines explicitly
    pattern = r"(const\s+GEO_DATA\s*=\s*)(\{.*?\};)"
    
    with open("debug_log.txt", "w") as log:
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            log.write(f"✅ Regex matched code block of length {len(match.group(0))}\n")
            log.write(f"Start: {match.group(0)[:50]}...\n")
        else:
            log.write("❌ Regex DID NOT match!\n")
            # Fallback: try simpler search for start
            start_idx = html_content.find("const GEO_DATA = {")
            if start_idx != -1:
                log.write(f"Found string at index {start_idx}\n")
                
    # We replace the JSON object part - using lambda to avoid escape sequence issues
    new_html_content = re.sub(pattern, lambda m: f"{m.group(1)}{json_str};", html_content, flags=re.DOTALL)
    
    if len(new_html_content) != len(html_content): # Basic check if something changed size-wise (not perfect but helpful)
         print("⚡️ HTML content modified (length changed).")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    print(f"💾 Saved updated {HTML_FILE}")
    print("🎉 Done.")

if __name__ == '__main__':
    main()

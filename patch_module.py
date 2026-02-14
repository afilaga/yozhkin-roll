
import os

target_file = 'module'
backup_file = 'module.bak'

# Backup
if not os.path.exists(backup_file):
    with open(target_file, 'rb') as f_in, open(backup_file, 'wb') as f_out:
        f_out.write(f_in.read())

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern to find (based on view_file output)
pattern = 'updateCartDelivery() { let e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 0; $("[name=\'".concat(this.config.DELIVERY_FIELD_NAME, "\'][value=\'").concat(this.config.DELIVERY_NAME, "\']")).attr("data-delivery-price", e), tcart__updateDelivery() }'

# The replacement code
# Logic: 
# 1. Set native data-delivery-price to 0 (so it doesn't duplicate total).
# 2. Call tcart__updateDelivery() to refresh cart UI (native part).
# 3. Handle "Доставка" product:
#    - If price > 0: Check if "Доставка" exists with correct price. If not, remove old and add new.
#    - If price == 0: Remove "Доставка" if exists.
replacement = """updateCartDelivery() { 
    let e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 0; 
    
    // Set native delivery price to 0 to avoid duplication in total
    $("[name='".concat(this.config.DELIVERY_FIELD_NAME, "'][value='").concat(this.config.DELIVERY_NAME, "']")).attr("data-delivery-price", 0); 
    tcart__updateDelivery(); 
    
    try {
        var t = window.tcart;
        var r = "Доставка";
        var n = t.products || [];
        var o = n.find(function(item) { return item.name === r; });
        
        if (e > 0) {
            // If product doesn't exist or price is different
            if (!o || parseFloat(o.price) !== e) {
                if (o) {
                    // Remove old
                    t.products = n.filter(function(item) { return item.name !== r; });
                    tcart__saveLocalObj();
                    // No need to save/update here, addProduct will do it
                }
                // Add new product
                tcart__addProduct({name: r, price: e, sku: 'delivery_service'});
            }
        } else {
            // Remove product if delivery is 0
            if (o) {
                t.products = n.filter(function(item) { return item.name !== r; });
                tcart__updateTotal();
                tcart__saveLocalObj();
            }
        }
    } catch (err) {
        console.error("Delivery Module Error:", err);
    }
}"""

# Check for exact match first
if pattern in content:
    new_content = content.replace(pattern, replacement)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: File patched successfully.")
else:
    print("ERROR: Pattern not found in file.")
    # Try fuzzy match or debug
    start_snippet = 'updateCartDelivery() { let e = arguments.length'
    idx = content.find(start_snippet)
    if idx != -1:
        print(f"DEBUG: Found start at index {idx}. Context:")
        print(content[idx:idx+300])
    else:
        print(f"DEBUG: Start snippet '{start_snippet}' not found.")

import pandas as pd
from google.colab import files

def load_data(inventory_path, invoice_path):
    """Loads inventory and invoice data from CSV files."""
    inventory = pd.read_csv(inventory_path).set_index("Item")  # Set "Item" as index
    invoice = pd.read_csv(invoice_path).set_index("Item")["Quantity"]
    return inventory, invoice

def add_new_items(inventory, invoice):
    """Adds new items from the invoice that are not in inventory."""
    new_items = invoice.index.difference(inventory.index)  # Find new items

    if not new_items.empty:
        print("\nNew items found in invoice. Adding to inventory...\n")
        
        for item in new_items:
            inventory.loc[item] = {  
                "Quantity": invoice[item],  # Set initial quantity from invoice  
                "Reorder_Threshold": 5,  # Default reorder threshold  
                "Order_Suggestion": 10,  # Default order suggestion  
                "Reorder_Needed": False,  # Initially assume no reorder needed  
            }
            print(f"Added: {item} with Quantity: {invoice[item]}")
    
    return inventory

def update_inventory(inventory, invoice):
    """Updates inventory stock levels based on invoice data."""
    for item, quantity in invoice.items():
        if item in inventory.index:
            inventory.at[item, "Quantity"] += quantity
    return inventory

def flag_reorders(inventory):
    """Flags items that need to be reordered."""
    inventory["Reorder_Needed"] = inventory["Quantity"] < inventory["Reorder_Threshold"]
    return inventory

def save_and_print_reorder_list(inventory, output_path):
    """Saves updated inventory and prints items needing reorder."""
    inventory.to_csv(output_path, index=True)  # Save with index

    # Print reorder list with index
    low_stock_items = inventory.loc[inventory["Reorder_Needed"], ["Quantity", "Reorder_Threshold", "Order_Suggestion"]]
    print("\nItems that need reordering:\n")
    print(low_stock_items)

    files.download(output_path)

def main():
    """Main function to manage inventory update process."""
    inventory_path = "/inventory.csv"
    invoice_path = "/invoice.csv"
    output_path = "updated_inventory.csv"

    # Load data
    inventory, invoice = load_data(inventory_path, invoice_path)
    
    # Add new items if necessary
    inventory = add_new_items(inventory, invoice)
    
    # Update inventory and flag reorders
    inventory = update_inventory(inventory, invoice)
    inventory = flag_reorders(inventory)

    # Save and print results
    save_and_print_reorder_list(inventory, output_path)

# Ensure script runs only when executed directly
if __name__ == "__main__":
    main()

import json
from pathlib import Path
from datetime import datetime

class Shop:
    def __init__(self, db_path = Path("shopdata.json")):
        self.db_path = db_path
        self.customers = self._load_data()

    def _load_data(self):
        if Path(self.db_path).exists():
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except:
                print("No such file exists.")
                return []
        return []
    
    def save_data(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.customers, f, indent = 3)
    
    def create_customer_info(self, name, balance, items, date, time):
        user_data = {
            "name": name,
            "customer_balance": balance,
            "items_purchased": items,
            "date": date,
            "time": time
        }
        self.customers.append(user_data)
        self.save_data()
        return True, user_data
    
    def find_customer(self, name):
        return next((customer for customer in self.customers if customer['name'] == name), None)
    
    def update_record(self, name, new_balance, new_items):
        customer = self.find_customer(name)
        if customer:
            purchase_details = {
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount_added': new_balance,
                'items_added': new_items
            }
            if 'history' not in customer:
                customer['history'] = []
            
            customer['history'].append(purchase_details)

            customer['customer_balance'] += new_balance
            customer['items_purchased'] = customer['items_purchased'] + new_items
            self.save_data()
            return True, customer['customer_balance']
        
        return False, "Customer Not Found"
    
    def remove_customer(self, name):
        customer = self.find_customer(name)
        if customer:
            self.customers.remove(customer)
            self.save_data()
            return True, "Customer details deleted." 
    
    def customer_list(self):
        return [customer for customer in self.customers]
    
        
# Program
# Program
import csv
from tabulate import tabulate
class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
class Inventory:
    def __init__(self, filename='inventory.csv'):
        self.filename = filename
        self.products = self.load_inven()
    def load_inven(self):
        products = {}
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products[int(row['product_id'])] = Product(
                        int(row['product_id']),
                        row['product_name'],
                        float(row['price']),
                        int(row['quantity'])
                    )
        except FileNotFoundError:
            print("Inventory file not found. Starting with an empty inventory.")
        return products
    def save_inven(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['product_id', 'product_name', 'price', 'quantity'])
            for product in self.products.values():
                writer.writerow([product.product_id, product.name, product.price, product.quantity])
    def add_pro(self, product):
        self.products[product.product_id] = product
        self.save_inven()
    def update_product_quantity(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].quantity -= quantity
            self.save_inven()
    def view_inventory(self):
        table = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        print(tabulate(table, headers=["ID", "Name", "Price", "Quantity"], tablefmt="grid"))
class Sale:
    def __init__(self, sale_id, product_id, product_name, quantity_sold, total_price):
        self.sale_id = sale_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity_sold = quantity_sold
        self.total_price = total_price
class SalesManager:
    def __init__(self, filename='sales.csv'):
        self.filename = filename
        self.sales = self.load_sales()
    def load_sales(self):
        sales = []
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sales.append(Sale(
                        int(row['sale_id']),
                        int(row['product_id']),
                        row['product_name'],
                        int(row['quantity_sold']),
                        float(row['total_price'])
                    ))
        except FileNotFoundError:
            print("Sales file not found. Starting with no sales records.")
        return sales
    def save_sales(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['sale_id', 'product_id', 'product_name', 'quantity_sold', 'total_price'])
            for sale in self.sales:
                writer.writerow([sale.sale_id, sale.product_id, sale.product_name, sale.quantity_sold, sale.total_price])
    def record_sale(self, sale):
        self.sales.append(sale)
        self.save_sales()
    def view_sales_report(self):
        table = [[s.sale_id, s.product_id, s.product_name, s.quantity_sold, s.total_price] for s in self.sales]
        print(tabulate(table, headers=["Sale ID", "Product ID", "Name", "Quantity Sold", "Total Price"], tablefmt="grid"))
class ShopSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager()
    def menu(self):
        while True:
            print("\n--- Small Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product to Inventory")
            print("3. Process a Sale")
            print("4. View Sales Report")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.inventory.view_inventory()
            elif choice == '2':
                self.add_prod()
            elif choice == '3':
                self.process_sale()
            elif choice == '4':
                self.sales_manager.view_sales_report()
            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    def add_prod(self):
        product_id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        quantity = int(input("Enter Product Quantity: "))
        product = Product(product_id, name, price, quantity)
        self.inventory.add_pro(product)
        print("Product added successfully!")
    def process_sale(self):
        sale_id = int(input("Enter Sale ID: "))
        while True:
            product_id = input("Enter Product ID to sell (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            product_id = int(product_id)
            if product_id not in self.inventory.products:
                print("Not found!")
                continue
            product = self.inventory.products[product_id]
            quantity = int(input(f"Enter quantity for {product.name}: "))
            self.total_price = total_price
            total_price=self.inventory.sales[0]
            if quantity > product.quantity:
                print("Insufficient stock!")
                continue
            total_price = product.price * quantity
            self.inventory.update_product_quantity(product_id, quantity)
            sale = Sale(sale_id, product_id, product.name, quantity, total_price)
            self.sales_manager.record_sale(sale)
        print(f"Sale {sale_id} recorded successfully!")
if __name__ == "__main__":
    shop_system = ShopSystem()
    shop_system.menu()

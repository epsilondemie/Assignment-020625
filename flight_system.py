
import sqlite3
from tabulate import tabulate

class FlightManager:
    def __init__(self, db_name='flights.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

#Destinations

# view a list of all existing destinations, sorted by city. 

    def view_destination(self):
        self.cursor.execute('''
        SELECT name, city, country, iata_code
        FROM airport
        ORDER BY city''')
        rows = self.cursor.fetchall()

#build table to return to user
        if rows:
            headers = ["Airport", "City", "Country", "IATA Code"]
            print("\n--- Destinations ---")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No destinations found.")

# add a new destination to the database

    def add_destination(self):
        print("\n--- Add a New Destination ---")
        name = input("Enter Airport Name: ").strip()
        city = input("Enter City: ").strip()
        country = input("Enter Country: ").strip()
        iata_code = input("Enter IATA code (3 letters): ").strip().upper()

#this makes all fields mandatory and ensures that the IATA code is 3 letters.

        if not name or not city or not country or len(iata_code) != 3:
            print("Invalid input. All fields are required, and IATA code must be 3 letters.")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO airport (name, city, country, iata_code)
                VALUES (?, ?, ?, ?)
            ''', (name, city, country, iata_code))
            self.conn.commit()

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
    
    def close(self):
        self.conn.close()


#return to the main menu
    

def main_menu():
    manager = FlightManager()
    while True:
        print("\n=== Flight Management System ===")
        print("1. Destinations")
        print("2. Flights (coming soon)")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            destination_menu(manager)
        elif choice == '2':
            print("Feature not implemented yet.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
    manager.close()

def destination_menu(manager):
    while True:
        print("\n--- Destination Menu ---")
        print("1. View All Destinations")
        print("2. Add a New Destination")
        print("3. Back to Main Menu")
    

#Destination submenu
        choice = input("Enter your choice: ")
        if choice == '1':
            manager.view_destination()
        elif choice == '2':
            manager.add_destination() 
        elif choice == '3':
            print("to complete")
            break
        else:
            print("Invalid choice. Try again.")

    
  #Run program 

if __name__ == '__main__':
    main_menu()
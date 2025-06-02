
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
        
        input("\nPress Enter to return to the Destination Menu.") 

# Adding destination: add a new destination to the database

    def add_destination(self):
        print("\n--- Add a New Destination ---")

        while True: 
            name = input("Enter Airport Name: ").strip()
            city = input("Enter City: ").strip()
            country = input("Enter Country (please provide the full name with no abbreviations): ").strip()
            iata_code = input("Enter IATA code (3 letters): ").strip().upper()

#Adding destination: this makes all fields mandatory and ensures that the IATA code is 3 letters.

            if name and city and country and len(iata_code) == 3:
                break #valid input, exit the loop
            else:
                print("\nInvalid input. All fields are required, and IATA code must be 3 letters.")
                input("Press Enter to return to the Destination Menu.") 
                return
         
        
        try:
            self.cursor.execute('''
                INSERT INTO airport (name, city, country, iata_code)
                VALUES (?, ?, ?, ?)
            ''', (name, city, country, iata_code))
            self.conn.commit()
            print(f"\nDestination '{name}' added successfully")

#The user may try to add a new destination, however it may already exist. 
#If this happens, the user will be told. If other error messages are thrown, the user can return to the Destination menu. 
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: airport.iata_code" in str(e):
                print("\nA destination with that IATA code already exists. \n")
                input("Press Enter to return to the Destination Menu.")
                return
            else:
                print(f"Database error: {e}")
                input("\nPress Enter to return to the Destination Menu.")
                return
    
    def close(self):
        self.conn.close()

#Updating existing Destination by inputting IATA code
    def update_destination(self):
        print("\n--- Update a Destination ---")
        print("Enter the IATA code of the destination to update.")
        iata_code = input("IATA code: ").strip().upper()

#Updating destination - only 3 letters will be accepted
        if len(iata_code) != 3:
            print("Invalid IATA code. It must be 3 letters.")
            return

#check if the IATA code is already in the database

        self.cursor.execute("SELECT name, city, country FROM airport WHERE iata_code = ?", (iata_code,))
        row = self.cursor.fetchone()

        if not row:
            print(f"No destination found with IATA code '{iata_code}'.")
            return
        
        print(f"\nCurrent Information: Airport: {row[0]}, City: {row[1]}, Country: {row[2]}")

#request new values, if the IATA code is not found in the flight database. If the user doesn't enter a value, then keep the current one. 

        new_name = input("Enter new airport name (leave blank to keep current): ").strip()
        new_city = input("Enter new city (leave blank to keep current): ").strip()
        new_country = input("Enter new country (leave blank to keep current). Please provide the full country name with no abbreviations: ").strip()

#if the user doesn't enter a new value, keep the current one 
        new_name = new_name or row[0]
        new_city = new_city or row[1]
        new_country = new_country or row[2]

        try:
            self.cursor.execute('''
            UPDATE airport
            SET name = ?, city = ?, country = ?
            WHERE iata_code = ?
            ''', (new_name, new_city, new_country, iata_code))
            self.conn.commit()
            print(f"\nDestination '{iata_code}' updated successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        
        input("\nPress Enter to return to the Destination Menu.") 

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
        print("3. Update a Destination")
        print("4. Back to Main Menu")
    

#Destination submenu
        choice = input("Enter your choice: ")
        if choice == '1':
            manager.view_destination()
        elif choice == '2':
            manager.add_destination() 
        elif choice == '3':
            manager.update_destination()
        elif choice == '4':
            print("Return to menu")
        
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main_menu()
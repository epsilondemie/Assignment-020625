
import sqlite3

class FlightManager:
    def __init__(self, db_name='flights.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    def view_all_flights(self):
        self.cursor.execute
        ('''SELECT flight_id, origin_id, destination_id, departure_timestamp, status 
        FROM flight''')
        rows = self.cursor.fetchall()

        if rows:
            print("\n--- All Flights ---")
            for row in rows:
                print(f"ID: {row[0]}, From: {row[1]}, To: {row[2]}, Depart: {row[3]}, Status: {row[4]}")
        else:
            print("No flights found.")

    def find_flights_by_destination(self):
        dest = input("Enter destination airport code (e.g., JFK): ").strip().upper()
        self.cursor.execute(
          '''SELECT flight_id, origin_id, departure_timestamp, status 
              FROM flight 
              WHERE destination_id = ?''',
              (dest,)
         )
        rows = self.cursor.fetchall()
        if rows:
            print(f"\nFlights to {dest}:")
            for row in rows:
                print(f"ID: {row[0]}, From: {row[1]}, Depart: {row[2]}, Status: {row[3]}")
        else:
            print("No flights found to that destination.")

    def close(self):
        self.conn.close()

def main_menu():
    manager = FlightManager()
    while True:
        print("\n=== Flight Management System ===")
        print("1. View All Flights")
        print("2. Find Flights by Destination")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            manager.view_all_flights()
        elif choice == '2':
            manager.find_flights_by_destination()
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")
    
    manager.close()

if __name__ == '__main__':
    main_menu()

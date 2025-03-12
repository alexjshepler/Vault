from typing import Optional

from tabulate import tabulate

from Database import Database
from Logger import logger as log

class Main():

    def __init__(self):
        self.db = Database()

        self.tables = self.db.list_tables()
        self.table_index = -1

    def select_table(self):
        while True:
            self.tables = self.db.list_tables()
            print("\n---------- Tables ----------")
            if len(self.tables) == 0:
                print('No tables in database')

                user_input = input("Would you like to create a new table? (y/n): ").strip()

                if user_input.lower() in ['y', 'n']:
                    self.create_table()
                    continue
                else:
                    print('Please enter y or n')
            else:
                for i, table in enumerate(self.tables):
                    print(f'{(i+1):02d}: {table}')
                print(f'{(i+2):02d}: Create new table')

                user_input = input(f'\nSelect what table or to create a new table (1-{i+2}): ').strip()

                try:
                    user_input = int(user_input)
                except:
                    print('Please only select a number')

                if user_input < 0 or user_input > (i+2):
                    print(f"Please only select an optin between 1 and {i + 2}")
                    continue

                print('return')
                return (user_input - 1)

    def create_table(self):
        table_name = input("Enter table name: ").strip()

        columns = {}
        while True:
            column_name = input("Enter column name (or press Enter to finish): ").strip()
            if not column_name:
                break

            columns[column_name] = 'TEXT'

        if table_name:
            self.db.create_table(table_name, columns)
        else:
            log.error("No columns provided. Aborting.")

    def main_loop(self):
        while True:
            print('\n\n########## Vault ##########')
            print('01) List Tables')
            print('02) Create Table')
            print('03) Load Table')
            print('00) Exit')

            user_input = input('Select an option: ').strip()

            try:
                user_input = int(user_input)
            except:
                log.error('Please enter a number 0-3')
                continue

            if user_input < 0 or user_input > 3:
                log.error('Please make a selection in the range 0-3')

            if user_input == 0:
                log.info('Exiting program')
                return

            if user_input == 1:
                self.db.list_tables()
            elif user_input == 2:
                self.create_table()
            elif user_input == 3:
                self.load_table()

    def load_table(self):
        self.table_index = self.select_table()

        while True:
            print('01) Show whole table')
            print('02) Add entry')
            print('\n00) Return to main menu')
            
            user_input = input('Please select an option 1-2: ').strip()

            try:
                user_input = int(user_input)
            except:
                log.error('Please enter a number 0-2')

            if user_input < 0 or user_input > 2:
                log.error('Please make a selection in the range 0-3')
                continue

            if user_input == 0:
                log.info('Returning to main menu')
                return

            if user_input == 1:
                table_name = self.tables[self.table_index]
                columns, entries = self.db.get_entries(table_name)

            elif user_input == 2:
                table_name = self.tables[self.table_index]
                self.add_entry(table_name)

    def add_entry(self, table_name):
        columns = self.db.get_columns(table_name)
        data = {}

        for column in columns:
            value = input(f'Enter value for {column}: ').strip()
            data[column] = value

        self.db.insert_entry(table_name, data)

        log.info("Entry added successfully.")

    def main(self):
        self.main_loop()

if __name__ == '__main__':
    main = Main()
    main.main()

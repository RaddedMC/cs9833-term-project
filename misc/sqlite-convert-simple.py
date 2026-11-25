#!/usr/bin/env python3

import csv
import sqlite3
import os

def convert_single_csv_to_sqlite(csv_file, db_path, table_name):
    """Convert a single CSV file to SQLite table."""
    print(f"Processing {csv_file}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Read headers
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
        
        # Sanitize column names
        sanitized_headers = []
        for header in headers:
            col_name = header.strip().replace(' ', '_').replace('-', '_').replace('.', '_')
            col_name = ''.join(c for c in col_name if c.isalnum() or c == '_')
            if col_name and col_name[0].isdigit():
                col_name = 'col_' + col_name
            sanitized_headers.append(col_name)
        
        # Create table
        create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT"
        for header in sanitized_headers:
            create_stmt += f", {header} TEXT"
        create_stmt += ")"
        
        cursor.execute(create_stmt)
        
        # Build INSERT statement
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(sanitized_headers)}) VALUES ({', '.join(['?' for _ in sanitized_headers])})"
        
        # Read and insert rows
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip headers
            
            rows_to_insert = []
            row_count = 0
            
            for row in reader:
                processed_row = []
                for cell in row:
                    processed_row.append(None if cell == '' else cell)
                rows_to_insert.append(tuple(processed_row))
                row_count += 1
                
                if len(rows_to_insert) >= 100:  # Smaller batch for testing
                    cursor.executemany(insert_stmt, rows_to_insert)
                    rows_to_insert = []
            
            if rows_to_insert:
                cursor.executemany(insert_stmt, rows_to_insert)
        
        conn.commit()
        print(f"✓ Successfully inserted {row_count} rows")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {csv_file}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    # Configuration
    data_dir = "./data/MERGED_CSV"
    csv_files = [
        "Merged01.csv",
        "Merged02.csv", 
        "Merged03.csv"
    ]  # Start with just 3 files for testing
    db_path = "./data/merged_data.sqlite3"
    
    print("Starting CSV to SQLite conversion...")
    print(f"Target database: {db_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Process each file
    success_count = 0
    for csv_file in csv_files:
        csv_path = os.path.join(data_dir, csv_file)
        table_name = os.path.splitext(csv_file)[0]
        
        if convert_single_csv_to_sqlite(csv_path, db_path, table_name):
            success_count += 1
    
    print(f"\n✓ Conversion complete! Successfully processed {success_count}/{len(csv_files)} files")

if __name__ == "__main__":
    main()
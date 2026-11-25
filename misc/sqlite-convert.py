#!/usr/bin/env python3

import csv
import glob
import sqlite3
import os
import sys

def csv_to_sqlite(csv_pattern, db_path):
    """Convert multiple CSV files to a single SQLite database."""
    # Get all CSV files matching the pattern
    csv_files = sorted(glob.glob(csv_pattern))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found matching pattern: {csv_pattern}")
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Process each CSV file
    for i, csv_file in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}] Processing {os.path.basename(csv_file)}...")
        
        # Read the first file to get headers and determine data types
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                print(f"  -> Warning: Empty CSV file {os.path.basename(csv_file)}, skipping")
                continue
            
            # Create table name from CSV filename (remove extension and path)
            table_name = os.path.splitext(os.path.basename(csv_file))[0]
            
            # Sanitize column names
            sanitized_headers = []
            for header in headers:
                # Remove spaces, hyphens, and other special chars
                col_name = header.strip().replace(' ', '_').replace('-', '_').replace('.', '_')
                # Remove any non-alphanumeric characters except underscores
                col_name = ''.join(c for c in col_name if c.isalnum() or c == '_')
                # Ensure it starts with a letter
                if col_name and col_name[0].isdigit():
                    col_name = 'col_' + col_name
                sanitized_headers.append(col_name)
            
            # Build CREATE TABLE statement
            create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT"
            for header in sanitized_headers:
                create_stmt += f", {header} TEXT"
            create_stmt += ")"
            
            cursor.execute(create_stmt)
            
            # Build INSERT statement
            insert_stmt = f"INSERT INTO {table_name} ({', '.join(sanitized_headers)}) VALUES ({', '.join(['?' for _ in sanitized_headers])})"
            
            # Read and insert all rows
            rows_to_insert = []
            row_count = 0
            for row in reader:
                # Convert empty strings to None for NULL
                processed_row = []
                for cell in row:
                    if cell == '':
                        processed_row.append(None)
                    else:
                        processed_row.append(cell)
                rows_to_insert.append(tuple(processed_row))
                row_count += 1
                
                # Batch insert every 1000 rows to improve performance
                if len(rows_to_insert) >= 1000:
                    cursor.executemany(insert_stmt, rows_to_insert)
                    rows_to_insert = []
            
            # Insert any remaining rows
            if rows_to_insert:
                cursor.executemany(insert_stmt, rows_to_insert)
                rows_to_insert = []
            
            print(f"  -> Successfully inserted {row_count} rows")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"\n✓ Successfully created database: {db_path}")
    print(f"✓ Processed {len(csv_files)} files with {len(csv_files)} tables")

if __name__ == "__main__":
    # Configuration
    csv_pattern = "./data/MERGED_CSV/Merged*.csv"
    db_path = "./data/merged_data.sqlite3"
    
    print(f"Converting CSV files from: {csv_pattern}")
    print(f"Output SQLite database: {db_path}")
    
    try:
        csv_to_sqlite(csv_pattern, db_path)
    except Exception as e:
        print(f"\u2717 Error: {e}")
        sys.exit(1)
"""
Quick script to view database contents
Run: py view_database.py
"""
import sqlite3
import os

def view_database(db_file):
    """View tables and data in a SQLite database"""
    if not os.path.exists(db_file):
        print(f"[ERROR] Database file '{db_file}' not found!")
        return
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n{'='*60}")
        print(f"Database: {db_file}")
        print(f"{'='*60}")
        print(f"\nTables found: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"\n{'-'*60}")
            print(f"Table: {table_name}")
            print(f"{'-'*60}")
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("\nColumns:")
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                null_str = " NOT NULL" if not_null else ""
                print(f"  • {col_name}: {col_type}{null_str}{pk_str}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nTotal rows: {count}")
            
            # Show data (limit to 10 rows for display)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
                rows = cursor.fetchall()
                
                print(f"\nData (showing first {min(10, count)} rows):")
                print("-" * 60)
                
                # Get column names
                column_names = [col[1] for col in columns]
                print(" | ".join(column_names))
                print("-" * 60)
                
                for row in rows:
                    print(" | ".join(str(val) for val in row))
                
                if count > 10:
                    print(f"\n... and {count - 10} more rows")
        
        conn.close()
        print(f"\n{'='*60}\n")
        
    except sqlite3.Error as e:
        print(f"[ERROR] Error accessing database: {e}")

if __name__ == "__main__":
    # View both databases
    databases = ["dbs.db", "form_data.db"]
    
    for db in databases:
        view_database(db)


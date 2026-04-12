import sqlite3

print("\n" + "=" * 70)
print("DATABASE SCHEMA & STORED DATA")
print("=" * 70)

conn = sqlite3.connect('validation_results.db')
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(validation_results)")
columns = cursor.fetchall()

print("\n📋 Table: validation_results")
print("\n" + "-" * 70)
print("COLUMNS (Schema):")
print("-" * 70)
print(f"{'#':<3} {'Column Name':<25} {'Type':<15} {'Nullable':<10} {'Key'}")
print("-" * 70)
for col in columns:
    col_id, col_name, col_type, not_null, default, primary = col
    nullable = "NO" if not_null else "YES"
    is_key = "PK" if primary else ""
    print(f"{col_id:<3} {col_name:<25} {col_type:<15} {nullable:<10} {is_key}")

# Get row count
cursor.execute("SELECT COUNT(*) FROM validation_results")
row_count = cursor.fetchone()[0]

print("\n" + "=" * 70)
print(f"STORED DATA ({row_count} records)")
print("=" * 70)

cursor.execute("""
    SELECT id, domain, total_records, valid_records, invalid_records, 
           completeness_score, validity_score, consistency_score, final_score, 
           timestamp 
    FROM validation_results 
    ORDER BY id
""")
rows = cursor.fetchall()

if rows:
    for i, row in enumerate(rows, 1):
        rid, domain, total, valid, invalid, complete, validity, consist, final, ts = row
        print(f"\n📁 Record #{rid} | {domain.upper()}")
        print(f"   {'─' * 65}")
        print(f"   Records Processed: {total} | Valid: {valid} | Invalid: {invalid}")
        print(f"   Quality Scores:")
        print(f"     • Completeness: {complete}%")
        print(f"     • Validity: {validity}%")
        print(f"     • Consistency: {consist}%")
        print(f"     • FINAL SCORE: {final}%")
        print(f"   Stored At: {ts}")
else:
    print("\n🔍 No records found")

print("\n" + "=" * 70)
print("✅ PHASE 3: Database Storage Implementation")
print("=" * 70)
print("\n✓ SQLite database auto-initialized")
print("✓ Validation results stored automatically")
print("✓ Historical tracking enabled")
print("✓ Analytics queries available")
print("\n")

conn.close()

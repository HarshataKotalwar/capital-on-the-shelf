
import duckdb

con = duckdb.connect()

calendar = "read_csv_auto('data/raw/calendar.csv', header=true)"

result = con.execute(f"""
    SELECT
        MIN(date) AS first_date,
        MAX(date) AS last_date,
        MIN(d) AS first_day_id,
        MAX(d) AS last_day_id,
        COUNT(*) AS calendar_days
    FROM {calendar}
    WHERE TRY_CAST(
        REGEXP_EXTRACT(d, '[0-9]+') AS INTEGER
    ) <= 1913
""").fetchone()

print("SALES PERIOD")
print("First date:", result[0])
print("Last date:", result[1])
print("First day ID:", result[2])
print("Last day ID:", result[3])
print("Number of days:", result[4])

con.close()
from sqlalchemy import create_engine

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# Query all records from the "measurement" table
result = conn.execute("SELECT * FROM measurement")
for row in result:
    print(row)

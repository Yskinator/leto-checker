import psycopg2
import urlparse
import os

print("Attempting to connect to database")
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
print(url)
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
print("Opened database successfully")
cur = conn.cursor()
print("Creating table")
cur.execute("CREATE TABLE previous_status(id INT PRIMARY KEY NOT NULL, worked BOOL NOT NULL, since_last_full_test INT NOT NULL))"
print("Inserting data")
cur.execute("INSERT INTO previous_status (id, worked, since_last_full_test) VALUES (1, TRUE, 6);")
print("Querying for data")
cur.execute("SELECT * FROM previous_status;")
print(cur.fetchone())

print("Making changes permanent")
conn.commit()

print("Closing connection")
cur.close()
conn.close()

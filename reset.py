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
print("Inserting data")
cur.execute("UPDATE previous_status SET worked=TRUE WHERE id = 1;")
print("Making changes permanent")
conn.commit()

print("Closing connection")
cur.close()
conn.close()

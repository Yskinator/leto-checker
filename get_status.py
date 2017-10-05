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
print("Fetching status")
cur.execute("SELECT * FROM previous_status;")
status = cur.fetchone()
print("Every attempt has succeeded: " + str(status[1]))
print("Test count: " + str(status[2]))

print("Closing connection")
cur.close()
conn.close()

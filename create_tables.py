import psycopg2
import urlparse

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
cur.execute("CREATE TABLE previous_status(id INT PRIMARY KEY NOT NULL, worked BOOL NOT NULL);")
cur.execute("INSERT INTO previous_status (id, worked) VALUES (1, TRUE);")
rows = cur.fetchall()
print("Result:" + rows)

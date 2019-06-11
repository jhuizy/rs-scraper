import urllib.request, json
import psycopg2
from datetime import datetime

connection_str = "dbname='postgres' user='postgres' password='postgres' host='db'"

def migrate():
  print("migrating...")
  try:
    conn = psycopg2.connect(connection_str)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, time TIMESTAMP NOT NULL, name VARCHAR(255) NOT NULL, members BOOLEAN NOT NULL, buy_average INTEGER NOT NULL, buy_quantity INTEGER NOT NULL, sell_average INTEGER NOT NULL, sell_quantity INTEGER NOT NULL, overall_average INTEGER NOT NULL, overall_quantity INTEGER NOT NULL, PRIMARY KEY(id, time));")
    conn.commit()
  except Exception as e:
    print("Error: %s" % e)
  finally:
    conn.close()

def scrape():
  print("scraping...")
  with urllib.request.urlopen("https://storage.googleapis.com/osbuddy-exchange/summary.json") as url:
    data = json.loads(url.read().decode())
    dt = datetime.now()
    try:
      conn = psycopg2.connect(connection_str)
      cur = conn.cursor()
      for key in data.keys():
        item = data[key]
        cur.execute( \
          "INSERT INTO items (id, time, name, members, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
          (item["id"], \
          dt, \
          item["name"], \
          item["members"], \
          item["buy_average"], \
          item["buy_quantity"], \
          item["sell_average"], \
          item["sell_quantity"], \
          item["overall_average"], \
          item["overall_quantity"]) \
        )
      conn.commit()
    except Exception as e:
      print("Error: %s" % e)
    finally:
      conn.close()
    


if __name__ == "__main__":
  migrate()
  scrape()
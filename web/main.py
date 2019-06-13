from flask import Flask, jsonify
import psycopg2
import json
from math import sqrt, pow
from scipy.stats import logistic

app = Flask(__name__)

connection_str = "dbname='postgres' user='postgres' password='postgres' host='db'"

@app.route("/items")
def index():
  try:
    con = psycopg2.connect(connection_str)
    cur = con.cursor()
    items = get_all_items(cur)
    return jsonify(items)
  except Exception as e:
    print("Error: %s" % e)
  finally:
    con.close()

@app.route("/items/<name>/history")
def get_history(name):
  try:
    con = psycopg2.connect(connection_str)
    cur = con.cursor()
    items = get_item_history(name, cur)
    return jsonify(items)
  except Exception as e:
    print("Error: %s" % e)
  finally:
    con.close()

def get_all_items(cur):
  cur.execute("SELECT i1.time, i1.name, i1.members, i1.overall_quantity, i1.overall_average, i1.sell_quantity, i1.sell_average, i1.buy_quantity, buy_average FROM items i1 WHERE i1.overall_quantity > 0 AND i1.overall_average > 0 AND i1.sell_quantity > 0 AND i1.sell_average > 0 AND i1.buy_quantity > 0 AND buy_average > 0 AND i1.time = (select max(i2.time) from items i2 where i1.id = i2.id)")
  return [to_item(t) for t in cur.fetchall()]

def get_item_history(name, cur):
  cur.execute("SELECT i1.time, i1.name, i1.members, i1.overall_quantity, i1.overall_average, i1.sell_quantity, i1.sell_average, i1.buy_quantity, buy_average FROM items i1 WHERE i1.overall_quantity > 0 AND i1.overall_average > 0 AND i1.sell_quantity > 0 AND i1.sell_average > 0 AND i1.buy_quantity > 0 AND buy_average > 0 AND i1.name = %s ORDER BY time desc", (name,))
  return [to_item(t) for t in cur.fetchall()]

def to_item(t):
  time, name, members, overall_quantity,overall_average,sell_quantity,sell_average,buy_quantity,buy_average = t
  return {
    'time': time,
    'name': name,
    'members': members,
    'overall_quantity': float(overall_quantity),
    'overall_average': float(overall_average),
    'sell_quantity': float(sell_quantity),
    'sell_average': float(sell_average),
    'buy_quantity': float(buy_quantity),
    'buy_average': float(buy_average)
  }
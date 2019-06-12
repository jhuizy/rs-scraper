from flask import Flask, jsonify
import psycopg2
import json
from math import sqrt, pow
from scipy.stats import logistic

app = Flask(__name__)

connection_str = "dbname='postgres' user='postgres' password='postgres' host='db'"

@app.route("/supply-demand")
def index():
  return jsonify(calc_relative_ratios()[:100])

@app.route("/unicorns")
def unicorns():
  return jsonify(calc_unicorns()[:100])

sigmoid = logistic.cdf

def pinched_sigmoid(y, mean, max):
  pinched_max = 0.99 / sqrt(1 - pow(0.99, 2))
  def pinch(y):
    return y * (pinched_max / max)
  x = pinch(y)
  pinched_mean = pinch(mean)
  return sigmoid(x - pinched_mean)

def calc_unicorns():
  try:
    conn = psycopg2.connect(connection_str)
    cur = conn.cursor()
    items = get_all_items(cur)
    unicorns = [to_unicorn_item(i) for i in items if is_potential_unicorn(i)]
    avg_score = sum([u[1] for u in unicorns]) / len(unicorns)
    max_score = max([u[1] for u in unicorns])
    adjusted_unicorns = [adjust_unicorn(u, avg_score, max_score) for u in unicorns]
    adjusted_unicorns.sort(key=lambda x: x[1], reverse=False)
    return adjusted_unicorns
  except Exception as e:
    print("Error: %s" % e)
  finally:
    conn.close()

def is_potential_unicorn(item):
  return item['sell_quantity'] > item['buy_quantity'] and item['buy_average'] > item['sell_average']

def to_unicorn_item(item):
  avail_qty = item['sell_quantity'] - item['buy_quantity']
  return (avail_qty, (item['buy_average'] * avail_qty) - (item['sell_average'] * avail_qty), item)

def adjust_unicorn(unicorn, avg_score, max_score):
  a, b, item = unicorn
  return (a, pinched_sigmoid(b, avg_score, max_score), item)

def calc_relative_ratios():
  try:
    conn = psycopg2.connect(connection_str)
    cur = conn.cursor()
    items = get_all_items(cur)
    average = calc_overall_ratio(items)
    res = []
    for item in items:
      if not item['members']:
        x = calc_ratio(item)
        res.append({'name': item['name'], 'v': sigmoid(x - average)})
    res.sort(key=lambda x: x['v'], reverse=False)
    return res
  except Exception as e:
    print("Error: %s" % e)
  finally:
    conn.close()

def calc_overall_ratio(items):
  ratios = [calc_ratio(i) for i in items]
  return sum(ratios) / len(ratios)

def calc_ratio(item):
  overall = item['overall_quantity'] * item['overall_average']
  sell = item['sell_quantity'] * item['sell_average']
  buy = item['buy_quantity'] * item['buy_average']
  return (sell / overall) - (buy / overall)

def get_all_items(cur):
  cur.execute("SELECT i1.time, i1.name, i1.members, i1.overall_quantity, i1.overall_average, i1.sell_quantity, i1.sell_average, i1.buy_quantity, buy_average FROM items i1 WHERE i1.overall_quantity > 0 AND i1.overall_average > 0 AND i1.sell_quantity > 0 AND i1.sell_average > 0 AND i1.buy_quantity > 0 AND buy_average > 0 AND i1.time = (select max(i2.time) from items i2 where i1.id = i2.id)")
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
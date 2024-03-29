from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import json
from math import sqrt, pow
from scipy.stats import logistic

app = Flask(__name__)
CORS(app)

@app.route("/supply-demand")
def supply_demand():
  return jsonify(calc_relative_ratios()[:100])

@app.route("/unicorns")
def unicorns():
  return jsonify(calc_unicorns()[:100])

endpoint = "http://ge-tracker.jhuizy.com:3000"

sigmoid = logistic.cdf

def pinched_sigmoid(y, mean, max):
  pinched_max = 0.99 / sqrt(1 - pow(0.99, 2))
  def pinch(y):
    return y * (pinched_max / max)
  x = pinch(y)
  pinched_mean = pinch(mean)
  return sigmoid(x - pinched_mean)

def calc_unicorns():
  items = get_all_items()
  unicorns = [to_unicorn_item(i) for i in items if is_potential_unicorn(i)]
  avg_score = sum([u[1] for u in unicorns]) / len(unicorns)
  max_score = max([u[1] for u in unicorns])
  adjusted_unicorns = [format_unicorn(adjust_unicorn(u, avg_score, max_score)) for u in unicorns]
  adjusted_unicorns.sort(key=lambda x: x['score'], reverse=True)
  return adjusted_unicorns

def is_potential_unicorn(item):
  return item['sell_quantity'] > item['buy_quantity'] and item['buy_average'] > item['sell_average']

def to_unicorn_item(item):
  avail_qty = item['sell_quantity'] - item['buy_quantity']
  return (avail_qty, (item['buy_average'] * avail_qty) - (item['sell_average'] * avail_qty), item)

def adjust_unicorn(unicorn, avg_score, max_score):
  a, b, item = unicorn
  return (a, pinched_sigmoid(b, avg_score, max_score), item)

def format_unicorn(unicorn):
  avail_qty, score, item = unicorn
  margin_gp = item['buy_average'] - item['sell_average']
  margin_perc = margin_gp / item['sell_average'] * 100
  return {
    'qty': avail_qty,
    'score': score,
    'name': item['name'],
    'memebers': item['members'],
    'margin_percent': margin_perc,
    'margin_gp': margin_gp,
    'buy': item['sell_average'],
    'sell': item['buy_average']
  }

def calc_relative_ratios():
  items = get_all_items()
  average = calc_overall_ratio(items)
  res = []
  for item in items:
    if not item['members']:
      x = calc_ratio(item)
      res.append({'name': item['name'], 'v': sigmoid(x - average)})
  res.sort(key=lambda x: x['v'], reverse=False)
  return res

def calc_overall_ratio(items):
  ratios = [calc_ratio(i) for i in items]
  return sum(ratios) / len(ratios)

def calc_ratio(item):
  overall = item['overall_quantity'] * item['overall_average']
  sell = item['sell_quantity'] * item['sell_average']
  buy = item['buy_quantity'] * item['buy_average']
  return (sell / overall) - (buy / overall)

def get_all_items():
  return fetch_all(endpoint + "/items")

def get_item_history(name):
  return fetch_all(endpoint + "/items/" + name + "/history")

def fetch_all(endpoint):
  def fetch_one(page, per_page):
    with urllib.request.urlopen(endpoint + "?page={page}&per_page={per_page}".format(page=page, per_page=per_page)) as url:
      return json.loads(url.read().decode())
  per_page = 5000
  page = 0
  data = []
  result = fetch_one(page, per_page)
  while len(result) > 0:
    page += 1
    data += result
    result = fetch_one(page, per_page)
  return data
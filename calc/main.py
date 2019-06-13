from flask import Flask, jsonify
import urllib.request
import json
from math import sqrt, pow
from scipy.stats import logistic

app = Flask(__name__)

@app.route("/supply-demand")
def supply_demand():
  return jsonify(calc_relative_ratios()[:100])

@app.route("/unicorns")
def unicorns():
  return jsonify(calc_unicorns()[:100])

endpoint = "http://get-tracker.jhuizy.com:3000"

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
  adjusted_unicorns = [adjust_unicorn(u, avg_score, max_score) for u in unicorns]
  adjusted_unicorns.sort(key=lambda x: x[1], reverse=True)
  return adjusted_unicorns

def is_potential_unicorn(item):
  return item['sell_quantity'] > item['buy_quantity'] and item['buy_average'] > item['sell_average']

def to_unicorn_item(item):
  avail_qty = item['sell_quantity'] - item['buy_quantity']
  return (avail_qty, (item['buy_average'] * avail_qty) - (item['sell_average'] * avail_qty), item)

def adjust_unicorn(unicorn, avg_score, max_score):
  a, b, item = unicorn
  return (a, pinched_sigmoid(b, avg_score, max_score), item)

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
  with urllib.request.urlopen(endpoint + "/items") as url:
    return json.loads(url.read().decode())

def get_item_history(name):
  with urllib.request.urlopen(endpoint + "/items/" + name + "/history") as url:
    return json.loads(url.read().decode())

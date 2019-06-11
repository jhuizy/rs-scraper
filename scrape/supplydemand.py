import psycopg2
from scipy.stats import logistic

connection_str = "dbname='postgres' user='postgres' password='postgres' host='db'"

sigmoid = logistic.cdf

def calc_relative_ratios():
  conn = psycopg2.connect(connection_str)
  cur = conn.cursor()
  items = get_all_items(cur)
  average = calc_overall_ratio(items)
  res = []
  for item in items:
    x = calc_ratio(item)
    res.append({'name': item['name'], 'v': sigmoid(x - average)})
  conn.close()
  res.sort(key=lambda x: x['v'], reverse=True)
  return res
  

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

if __name__ == "__main__":
    print(calc_relative_ratios()[:100])
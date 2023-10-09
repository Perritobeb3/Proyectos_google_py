
#!/usr/bin/env python3

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import json
import locale
import sys
import emails
import reports
import os
from operator import itemgetter

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
        item["revenue"] = item_revenue
        max_revenue = item
  most_sales = 0
  most_sales_car = ""
  for n in data:
    if n["total_sales"] >= most_sales:
      most_sales = n["total_sales"]
      most_sales_car = "{make} {model} ({year})".format(make=n["car"]["car_make"],model=n["car"]["car_model"], year=str(n["car"]["car_year"]))
  cpy = {}  # calculamos el cars per year
  for n in data:
    year = n["car"]["car_year"]
    total_sales = n["total_sales"]
    if year in cpy:
      cpy[year] += total_sales
    else:
      cpy[year] = total_sales
  # calculamos el año más popular
  popular_year = ""
  popular_number = 0
  for k, v in cpy.items():
    if v > popular_number:
      popular_number = v
      popular_year = k

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {car} had the most sales: {sales}.".format(
      car=most_sales_car, sales=most_sales),
    "The most popular year was {year} with {sales} sales. \n".format(
      year=popular_year, sales=popular_number)
  ]
  summary = "<br/>".join(summary)


  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  print(summary)
  sorted_dic = sorted(data, key=itemgetter('total_sales'), reverse = True)
  table_data = cars_dict_to_table(sorted_dic)
  reports.generate("/tmp/cars.pdf","Sales Summary for last month", summary, table_data)
  #turn this into a PDF report
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = summary.replace("<br/>","\n")
  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)
  #send the PDF report as an email attachment


if __name__ == "__main__":
  main(sys.argv)

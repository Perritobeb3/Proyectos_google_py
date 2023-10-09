#!/usr/bin/env python3

import reportlab

from reportlab.lib.units import inch, cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate(filename, title, additional_info, table_data, graph_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')]
  report_table = Table(data=table_data, style=table_style, hAlign="LEFT")
  empty_line = Spacer(1,20)
  report_pie = Pie(width=3000, height=3000)
  report_pie.data = []
  report_pie.labels = []
  for n in graph_data:
    report_pie.data.append(n["total_sales"])
    report_pie.labels.append("{make} {model} ({year})".format(make=n["car"]["car_make"],model=n["car"]["car_model"], year=str(n["car"]["car_year"])))
  report_chart = Drawing()
  report_chart.add(report_pie)
  report.build([report_title, empty_line, report_info, empty_line, report_table, empty_line, report_chart])

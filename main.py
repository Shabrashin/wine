from calendar import c
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from collections import defaultdict
import pandas
import pprint

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data = pandas.read_excel(
    io='wine3.xlsx', 
    sheet_name='Лист1',
    na_values=['N/A', 'NA'],
    keep_default_na=False
).to_dict(orient='records')


collection = defaultdict(list)

for wine in excel_data:
    collection[wine['Категория']].append(wine)

rendered_page = template.render(
    year=datetime.now().year - 1920,
    collection=collection,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

import argparse
import os
from calendar import c
from collections import defaultdict
from datetime import datetime
from email.policy import default
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

COMPANY_ESTABLISHMENT_YEAR = 1920

def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Введите путь к файлу с данными', default=os.getenv('DATA_PATH'))
    args = parser.parse_args()
    data = args.data

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    wine_file_data = pandas.read_excel(
        io=data, 
        sheet_name='Лист1',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    ).to_dict(orient='records')


    wine_collection = defaultdict(list)

    for wine in wine_file_data:
        wine_collection[wine['Категория']].append(wine)

    rendered_page = template.render(
        year=datetime.now().year - COMPANY_ESTABLISHMENT_YEAR,
        wine_collection=wine_collection,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

from flask import Flask, render_template
import csv
import requests

app = Flask(__name__)

@app.route('/')
def index():
    csv_file_path = 'data.csv' 
    urls = []
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            url = row[0]
            urls.append(url)  # Append a tuple of (name, url)

    results = []
    names=[]
    for url in urls:
        try:
            response = requests.get(url)
            status = response.status_code
            if status == 200:
                result = f"The URL {url} is reachable and returns a status code 200 (OK)."
            else:
                result = f"The URL {url} is reachable but returns a status code {status}."
        except requests.ConnectionError:
            result = f"The URL {url} is unreachable."
        results.append(result)  # Append a tuple of (name, result)

    return render_template('index.html', results=results, names=names)

if __name__ == '__main__':
    app.run(debug=True)
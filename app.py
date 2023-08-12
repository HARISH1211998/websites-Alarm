import csv
import requests
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

def check_urls():
    csv_file_path = 'data.csv' 
    urls = []
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            url = row[0]  # Assuming the URLs are in the first column of the CSV
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url  # Adding 'http://' schema if missing
            urls.append(url)

    results = []
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
        results.append(result)
    
    return results

@app.route('/')
def index():
    results = check_urls()
    return render_template('index.html', results=results)

@app.route('/add-url', methods=['POST'])
def add_url():
    new_url = request.json['url']
    
    # Append the new URL to the CSV file
    with open('data.csv', 'a', newline='') as csv_file:
        csv_file.write(new_url + '\n')
    
    return jsonify({'message': 'URL added successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

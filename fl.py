import json
import string
import random
import flask
from flask import request, jsonify, redirect

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
with open('users', 'r') as users_file:
    users = json.loads(users_file.read())

with open('urls', 'r') as urls_file:
    urls = json.loads(urls_file.read())

def saver():
    with open('urls', 'w') as urls_file:
        urls_file.write(json.dumps(urls, indent=4, sort_keys=True))

def random_url_gen():
    random_url = ''.join([random.choice(string.ascii_lowercase) for i in range(8)])
    # optimize
    # maybe ...
    if random_url in urls:
        return random_url_gen()
    return random_url

def shortener(url, id_no):
    random_url = random_url_gen()
    urls[random_url] = [url, id_no]
    # try sorting
    # with open('urls', 'w') as urls_file:
        # urls_file.write(json.dumps(urls, indent=4, sort_keys=True))
    saver()
    return random_url

@app.route('/', methods=['GET'])
def home():
    return '''<h1>API testing website</h1>
<p>Only for users with API keys.</p>'''

@app.route('/api/shorten', methods=['GET', 'POST'])
def api_shorten():
    if 'url' not in request.args:
        return jsonify({'status': 0, 'output': 'No url'})
    if 'api_key' in request.args:
        for i in users:
            if i['api_key'] == request.args['api_key']:
                return jsonify({'status': 1, 'output': shortener(request.args['url'], i['id'])})
        return jsonify({'status': 0, 'output': 'Bad api_key'})
    else:
        return jsonify({'status': 0, 'output': 'No api_key'})

@app.route('/api/change', methods=['GET', 'POST'])
def api_change():
    if 'url' not in request.args:
        return jsonify({'status': 0, 'output': 'No url'})
    if 'short' not in request.args:
        return jsonify({'status': 0, 'output': 'No short'})
    if 'api_key' in request.args:
        for i in users:
            if i['api_key'] == request.args['api_key'] and urls[request.args['short']][1] == i['id']:
                urls[request.args['short']][0] = request.args['url']
                saver()
                return jsonify({'status': 1})
        return jsonify({'status': 0, 'output': 'Bad api_key'})
    else:
        return jsonify({'status': 0, 'output': 'No api_key'})

@app.route('/<short>', methods=['GET', 'POST'])
def redir(short):
    if short in urls:
        return redirect(urls[short][0])
    else:
        return '<b>404 NOT FOUND<b>', 404
        
app.run(host="0.0.0.0")
# app.run()
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


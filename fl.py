import json
import yaml
import string
import random
import flask
from flask import request, jsonify, redirect, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
with open('users.yaml', 'r') as users_file:
    users = yaml.load(users_file.read(), Loader = yaml.Loader)

with open('urls.yaml', 'r') as urls_file:
    urls = yaml.load(urls_file.read(), Loader = yaml.Loader)

def saver():
    with open('urls.yaml', 'w') as urls_file:
        urls_file.write(yaml.dump(urls, Dumper = yaml.Dumper))

def random_url_gen():
    random_url = ''.join([random.choice(string.ascii_lowercase) for i in range(8)])
    # optimize
    # maybe ...
    if random_url in urls:
        return random_url_gen()
    return random_url

def shortener(url, id_no):
    random_url = random_url_gen()
    urls[id_no][random_url] = url
    # try sorting
    # with open('urls', 'w') as urls_file:
        # urls_file.write(json.dumps(urls, indent=4, sort_keys=True))
    saver()
    return random_url

@app.route('/api/shorten', methods=['GET', 'POST'])
def api_shorten():
    if 'url' not in request.args:
        return jsonify({'status': 0, 'output': 'No url'})
    if 'api_key' in request.args:
        for idx, i in enumerate(users):
            if i['api_key'] == request.args['api_key']:
                return jsonify({'status': 1, 'output': shortener(request.args['url'], idx)})
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
        for idx, i in enumerate(users):
            if i['api_key'] == request.args['api_key'] and short in urls[idx]:
                urls[idx][short] = request.args['url']
                saver()
                return jsonify({'status': 1})
        return jsonify({'status': 0, 'output': 'Bad api_key'})
    else:
        return jsonify({'status': 0, 'output': 'No api_key'})

@app.route('/api/list', methods=['GET', 'POST'])
def api_list():
    if 'api_key' in request.args:
        for idx, i in enumerate(users):
            if i['api_key'] == request.args['api_key']:
                return jsonify({'status': 1, 'output': urls[idx]})
        return jsonify({'status': 0, 'output': 'Bad api_key'})
    else:
        return jsonify({'status': 0, 'output': 'No api_key'})

# Not API Calls
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    # return '''<h1>API testing website</h1>
# <p>Only for users with API keys.</p>'''

@app.route('/<short>', methods=['GET', 'POST'])
def redir(short):
    for user_links in urls:
        if short in user_links:
            return redirect(user_links[short])
    return '<b>404 NOT FOUND</b>', 404

@app.route('/list', methods=['POST'])
def get_list():
    if 'api_key' in request.form:
        for idx, i in enumerate(users):
            if i['api_key'] == request.form['api_key']:
                return render_template('list.html',user = users[idx]['username'], urls = urls[idx])
        return '<b>BAD API KEY</b>', 401
    else:
        return '<b>404 NOT FOUND</b>', 404

app.run(host="0.0.0.0")
# app.run()
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

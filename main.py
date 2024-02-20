from flask import Flask, redirect, url_for, request

app = Flask(__name__)

users = [
    {'id':1, 'name':'john'},
    {'id':2, 'name':'ben'},
    {'id':3, 'name':'kenny'}
]

@app.route('/')
@app.route('/home')
def home_page():
    return '''<h1>Welcome Home!</h1>
    <p>This is a home page</p>'''

@app.route('/hello/<name>')
def hello_world(name):
    return f'Hello {name}'

@app.route('/user/<int:id>',methods=['GET','POST'])
def get_user_by_id(id):
    for user in users:
        if user['id'] == id:
            return redirect(url_for('hello_world',name=user['name']))

@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')
    return '''<h1>The language value is: {}</h1>'''.format(language)

# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)
    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# GET requests will be blocked
@app.route('/json-example/v1', methods=['POST'])
def json_example_v1():
    request_data = request.get_json()
    language = request_data['language']
    framework = request_data['framework']
    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']
    # an index is needed because of the array
    example = request_data['examples'][0]
    boolean_test = request_data['boolean_test']
    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

# GET requests will be blocked
@app.route('/json-example/v2', methods=['POST'])
def json_example_v2():
    request_data = request.get_json()

    language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
                if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                    example = request_data['examples'][0]
        if 'boolean_test' in request_data:
                boolean_test = request_data['boolean_test']
        return '''
               The language value is: {}
               The framework value is: {}
               The Python version is: {}
               The item at index 0 in the example list is: {}
               The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

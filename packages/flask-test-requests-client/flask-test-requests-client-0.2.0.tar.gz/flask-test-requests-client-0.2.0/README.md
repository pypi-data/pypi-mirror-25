# Flask Requests Test Client

This package is an alternative to the flask test client, one which has a very similar interface to the *requests* package. This allows the same tests to be re-used against the test client (using this package) and an actual HTTP server (using requests).

```
>>> from flask import Flask, jsonify
>>> app = Flask(__name__)

>>> @app.route('/hello')
... def hello_world():
...     return jsonify({'msg': 'Hello, World!'})

>>> from frtc import TestClient
>>> client = TestClient(app.test_client())

>>> r = client.get('/hello')
>>> r.status_code
200

>>> r.headers['Content-Type']
'application/json'
>>> r.encoding
>>> r.text  # doctest: +ALLOW_UNICODE
'{\n  "msg": "Hello, World!"\n}\n'
>>> r.json()  # doctest: +ALLOW_UNICODE
{'msg': 'Hello, World!'}

```
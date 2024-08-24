from flask import Flask, render_template, request, jsonify
from inference.inference_engine import inference_response
from waitress import serve # production server.

# Flast app
app = Flask(__name__)

# Home page.
@app.route('/')
def index():
    return render_template('index.html', messages=[])

# On send request
@app.route('/send_message', methods=['POST'])
def send_message():
    # Data from the form.
    data = request.json
    user_message = data.get('message')

    # inference.
    bot_response = inference_response(user_message)

    # Returning inference.
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)

import waitress
import os
from flask import Flask, render_template, request
from calculator import get_table


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    # print(timeofevent)
    return render_template('index.html')

form_data = ''

@app.route('/calculate', methods=['POST','GET'])
def data():
    global form_data
    if len(request.form) != 0:
        form_data = request.form
    companies , timeofevent, paramets= get_table(form_data)
    return render_template('data.html', 
        tables=[companies.to_html(classes='data')],
        titles=companies.columns.values, 
        timeofevent = timeofevent,
        paramets = paramets)


if __name__ == '__main__':
    # app.run(debug=True)
    app.debug = True
    port = int(os.environ.get('PORT', 8080))
    waitress.serve(app, port=port)
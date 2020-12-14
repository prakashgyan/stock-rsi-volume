import waitress
import os
from flask import Flask, render_template
from calculator import get_table

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # print(timeofevent)
    companies, timeofevent = get_table()
    return render_template('data.html', tables=[companies.to_html(classes='data')], titles=companies.columns.values,
                           timeofevent=timeofevent)


if __name__ == '__main__':
    # app.run(debug=True)
    app.debug = True
    port = int(os.environ.get('PORT', 8080))
    waitress.serve(app, port=port)

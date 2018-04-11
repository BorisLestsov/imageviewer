import csv
from flask import Flask, render_template, request, redirect, url_for, session
import requests
from pager import Pager
import time


def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]


APPNAME = "NeuralValidator_v0.0"
STATIC_FOLDER = 'example'
TABLE_FILE = "example/fakecatalog.csv"
f=open('out.txt', 'a+')

table = read_table(TABLE_FILE)
pager = Pager(len(table))


app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<int:ind>/', methods=['GET', 'POST'])
def image_view(ind=None):
    if request.method == 'POST':
        text = request.form['text']
        f.write("mypost: {} {}\n".format(ind, text))
        f.flush()
        return redirect('/{}'.format(ind+1))

    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        pager.current = ind
        return render_template(
            'imageview.html',
            index=ind,
            pager=pager,
            data=table[ind])

   


@app.route('/goto', methods=['POST', 'GET'])    
def goto():
    return redirect('/' + request.form['index'])


if __name__ == '__main__':
    app.run(debug=True)

from flask import *

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import sqlite3

app = Flask(__name__)

selquery = "SELECT size FROM data WHERE size = ?"
oldquery = "UPDATE data SET count = count + 1 WHERE size = ?"
newquery = "INSERT INTO data VALUES (?,?)"


def collect(resolution):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    c = cursor.execute(selquery,(resolution,))
    result = c.fetchall()
    if result == []:
        print "New stuff!!!"
        c = cursor.execute(newquery,(resolution,1,))
    else:
        print "Old stuff!!!"
        c = cursor.execute(oldquery,(resolution,))
    connection.commit()


@app.route('/')
def index():
    return send_file("static/form.html")


@app.route('/api', methods=["POST"])
def process():
    resolution = request.form.get("size")
    collect((resolution))
    # todo logic here
    return redirect("/thanks")


@app.route('/favicon.ico')
def icon():
    return send_file("static/favicon.ico")


@app.route('/thanks')
def thanks():
    return send_file("static/thanks.html")


#develop server
'''app.run(
    port=80,
    debug=True
)'''

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()

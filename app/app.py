from flask import Flask, request, render_template, redirect, url_for
from db import add_text, get_data

app = Flask(__name__,template_folder='templates')
@app.route("/")
def getList():
    all_text = get_data()
    return render_template('index.html')

@app.route("/add_text", methods=["POST", "GET"])
def AddText():
    if request.method == "POST":
        ticket_data = request.form["textv"]
        #saving all the values to db
        add_new = add_text(ticket_data)
        return redirect(url_for('getList'))
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')


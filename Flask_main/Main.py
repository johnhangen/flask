from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = "key"


dic = {}
eligible = {}

@app.route("/")
def loop():
    return redirect("/home")


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/candef", methods=["POST","GET"])
def candef():
	if request.method == "POST":
		try:
			inp = dic[request.form["input"].upper().strip()]
			session["user"] = inp[1], inp[0]
			try:
				session["usercolor"] = eligible[inp[1]]
			except:
				session["usercolor"] = "lneligible"
			return redirect(url_for("output"))
		except:
			redirect(url_for("home"))
			session.clear()
			print("Error: Request failed")
		
	return render_template("login.html")
    
@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/pl")
def pl():
    return render_template("pl.html")

@app.route("/output")
def output():
	if "user" in session:
		user = session["user"]
		color = session["usercolor"]
		return render_template("output.html", place = user, color = color)
	else:
		return redirect(url_for("home"))
	

if __name__ == "__main__":
	with open("Address.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		for row in reader:
			dic.update({row[0].upper(): [row[1], row[2]]})
	with open("gr.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		for row in reader:
			eligible.update({row[0]: row[1]})
	print(" * CSV files read") 
app.run(app.run(port=5000, debug=True))
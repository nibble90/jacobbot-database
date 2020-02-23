from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("landing.html")
@app.route("/login")
def login_page():
    return render_template("login.html")
@app.route("/signup")
def signup_page():
    return render_template("signup.html")
@app.route("/login_page", methods = ["GET", "POST"])
def login_request():
    if(request.method == "GET"):
        """return the information for <user_id>"""
        return "Login page"
    elif(request.method == "POST"):
        """modify/update the information for <user_id>"""
        data = request.form # a multidict containing POST data
        return data
    else:
        return "No thank you..."
@app.route("/signup_page", methods = ["GET", "POST"])
def signup_request():
    if(request.method == "GET"):
        """return the information for <user_id>"""
        return "Signup page"
    elif(request.method == "POST"):
        """modify/update the information for <user_id>"""
        data = request.form # a multidict containing POST data
        return data
    else:
        return "No thank you..."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)

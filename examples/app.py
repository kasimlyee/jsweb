from jsweb import JsWebApp, run, render, json

# Create an instance of the JsWebApp
app = JsWebApp()

@app.route("/")
def home(req):
    return render("welcome.html", {"name": "Jones"})

if __name__ == "__main__":
    run(app)

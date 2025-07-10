from jsweb import JsWebApp, run, render, __VERSION__, html

app = JsWebApp()


@app.route("/")
def home(req):
    arr = {"one": "ff", "two": "gg", "three": "gg1"}
    query = req.query.get("name", "")
    return render("welcome.html", {"name": query, "version": __VERSION__, "arr": arr})


@app.filter("shout")
def shout(text):
    return text.upper() + "!!!"


@app.route("/form")
def form(req):
    return html('''
    <h1>Welcome to JsWeb Test</h1>
    <p><a href='/search?q=hello'>Test Query Params</a></p>
    <form method="POST" action="/submit">
        <input name="name" placeholder="Your name" />
        <button type="submit">Submit</button>
    </form>
    ''')


@app.route("/submit", methods=["POST"])
def submit(req):
    name = req.form.get("name", "Anonymous")
    return html(f"<h2>👋 Hello, {name}</h2>")


@app.route("/search")
def search(req):
    query = req.query.get("q", "")
    return html(f"<h2>🔍 You searched for: {query}</h2>")


if __name__ == "__main__":
    run(app)

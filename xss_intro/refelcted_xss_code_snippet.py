from flask import Flask, request, render_template, redirect
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# helper for template footer (year)
@app.context_processor
def inject_now():
    return {"now": lambda: datetime.utcnow().year}

NEWS = [
    {"title": "Product launch: SecureMail", "summary": "A privacy-focused email client arrives."},
    {"title": "Weekly Roundup", "summary": "Top vulnerabilities and patches this week."},
    {"title": "Research: XSS Trends 2025", "summary": "A short summary of XSS cases observed in the wild."},
]


COMMENTS = []


@app.route("/")
def home():

    q = request.args.get("q", "")
    query_escaped = escape(q) 
    return render_template("news.html", news=NEWS, query=q, query_escaped=query_escaped) # <--- The root cause of an xss attack. 

    #render_template function parses input value to the url


@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():

    if request.method == "POST":
        name = request.form.get("name", "Anonymous")
        comment = request.form.get("comment", "")
        
        COMMENTS.append({"name": escape(name), "comment": comment})
        return redirect("/guestbook")

    return render_template("guestbook.html", comments=COMMENTS)


@app.route("/dom")
def dom_preview():

    return render_template("dom_preview.html")


if __name__ == "__main__":
    # bind to all interfaces for lab convenience (change to 127.0.0.1 for local-only)
    app.run(debug=True, host="0.0.0.0", port=5000)

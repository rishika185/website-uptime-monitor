
from flask import Flask, render_template_string, request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from time import perf_counter
from urllib.parse import urlparse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Website Uptime Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f5f9;
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 750px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        }
        h1 { color: #243b55; }
        input {
            width: 70%;
            padding: 12px;
            box-sizing: border-box;
        }
        button {
            padding: 12px 18px;
            background: #2457c5;
            color: white;
            border: none;
            cursor: pointer;
        }
        .result {
            margin-top: 25px;
            padding: 18px;
            background: #eef3f8;
            border-radius: 8px;
        }
        .online { color: green; }
        .offline { color: #c62828; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Website Uptime Monitor</h1>
        <p>Check website availability and response time.</p>

        <form method="POST">
            <input type="text" name="url"
                   placeholder="https://example.com"
                   value="{{ url }}" required>
            <button type="submit">Check Website</button>
        </form>

        {% if status %}
        <div class="result">
            <h3>Monitoring Result</h3>
            <p>Website: {{ url }}</p>
            <p>Status:
                <strong class="{{ css_class }}">{{ status }}</strong>
            </p>
            <p>Response time: {{ response_time }}</p>
            <p>Details: {{ details }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    url = ""
    status = ""
    response_time = "N/A"
    details = ""
    css_class = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if "://" not in url:
            url = "https://" + url

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            status = "Invalid URL"
            details = "Enter a valid HTTP or HTTPS website."
            css_class = "offline"
        else:
            try:
                start = perf_counter()
                req = Request(
                    url,
                    headers={"User-Agent": "WebsiteUptimeMonitor/1.0"}
                )

                with urlopen(req, timeout=5) as response:
                    code = response.status

                elapsed = (perf_counter() - start) * 1000
                response_time = f"{elapsed:.2f} ms"
                status = "ONLINE" if 200 <= code < 400 else "OFFLINE"
                details = f"HTTP status code: {code}"
                css_class = "online" if status == "ONLINE" else "offline"

            except HTTPError as error:
                status = "OFFLINE"
                details = f"HTTP status code: {error.code}"
                css_class = "offline"

            except (URLError, TimeoutError, OSError, ValueError) as error:
                status = "OFFLINE"
                details = f"Connection failed: {error}"
                css_class = "offline"

    return render_template_string(
        HTML,
        url=url,
        status=status,
        response_time=response_time,
        details=details,
        css_class=css_class
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

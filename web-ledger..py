from datetime import datetime
from openai import OpenAI
import json
import os
import time

# ----------------------------
# 1. CONFIG
# ----------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_KEY)

# ----------------------------
# 2. OpenAI News Logic (Kept Identical)
# ----------------------------
def get_dynamic_news(retries=3):
    prompt = """
Generate a concise geopolitical and financial intelligence briefing.
Return STRICT JSON with this schema:
{
  "geo": [["headline", "text"], ...],
  "tech": [["headline", "text"], ...],
  "regional": [["headline", "text"], ...],
  "market": "single paragraph"
}
Constraints: Tone sober, analytical, max 2 sentences per item.
"""
    for attempt in range(retries):
        try:
            # Note: Changed to standard completions for broader compatibility
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if attempt == retries - 1: raise RuntimeError(f"OpenAI failure: {e}")
            time.sleep(2)

# ----------------------------
# 3. Web-Optimized HTML Builder
# ----------------------------
def build_web_html(news):
    now = datetime.now().strftime("%A, %B %d, %Y | %H:%M CEST").upper()

    def render_section(title, items):
        html = f"<h2>{title}</h2>"
        for head, body in items:
            html += f'<div class="item"><strong>{head}:</strong> {body}</div>'
        return html

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Realist Ledger | Evening Update</title>
    <style>
        :root {{
            --bg-color: #121212;
            --container-bg: #1e1e1e;
            --accent: #d35400;
            --highlight: #f39c12;
            --text-main: #e0e0e0;
            --text-dim: #888;
        }}

        body {{
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}

        .container {{
            background-color: var(--container-bg);
            max-width: 900px;
            width: 100%;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-top: 5px solid var(--accent);
            box-sizing: border-box;
        }}

        .header {{
            border-bottom: 1px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
        }}

        .title-group {{ margin-bottom: 10px; }}

        .title {{
            font-size: 2rem;
            font-weight: bold;
            color: #ffffff;
            margin: 0;
        }}

        .edition {{
            font-size: 0.8rem;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .date {{
            font-size: 0.85rem;
            color: var(--text-dim);
        }}

        h2 {{
            font-size: 1.2rem;
            color: var(--accent);
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
            margin-top: 30px;
            text-transform: uppercase;
        }}

        .item {{ margin-bottom: 20px; line-height: 1.6; }}

        .item strong {{ color: var(--highlight); }}

        .market-callout {{
            background-color: #252525;
            border-left: 4px solid var(--highlight);
            padding: 20px;
            margin: 30px 0;
            font-style: italic;
        }}

        .footer-legal {{
            margin-top: 50px;
            font-size: 0.75rem;
            color: #555;
            border-top: 1px solid #333;
            padding-top: 20px;
            line-height: 1.4;
        }}

        @media (max-width: 600px) {{
            .container {{ padding: 20px; }}
            .header {{ flex-direction: column; align-items: flex-start; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="title-group">
                <h1 class="title">The Realist Ledger</h1>
                <div class="edition">Evening Intelligence Update</div>
            </div>
            <div class="date">{now}</div>
        </header>

        <main>
            {render_section("I. Geopolitical & Security Shift", news["geo"])}
            {render_section("II. Technology & Global Capital", news["tech"])}

            <section class="market-callout">
                <strong>EVENING MARKET FLASH:</strong> {news["market"]}
            </section>

            {render_section("III. Regional & Cultural Briefs", news["regional"])}
        </main>

        <footer class="footer-legal">
            <p><strong>LEGAL DISCLAIMER:</strong> AI-generated synthetic intelligence. Not financial or legal advice.</p>
            <p>&copy; {datetime.now().year} Institutional Analytics Group. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
"""

# ----------------------------
# 4. Execution
# ----------------------------
if __name__ == "__main__":
    try:
        news_data = get_dynamic_news()
        html_content = build_web_html(news_data)

        # Save as .html instead of .pdf
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("Web page generated: index.html")
    except Exception as e:
        print("ERROR:", e)
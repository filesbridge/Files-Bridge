from flask import Flask, request, send_from_directory, redirect
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Файловый мост</title>
<style>
  :root {{
    --orange: #ff6a1a;
    --orange-dark: #e0570f;
    --bg: #fffaf6;
    --card: #ffffff;
    --border: #ffe0cc;
    --text: #2b2320;
    --muted: #9c8b80;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    max-width: 480px;
    margin: 0 auto;
    padding: 32px 20px 60px;
  }}

  .logo {{
    width: 40px; height: 40px;
    background: var(--orange);
    border-radius: 12px;
    margin-bottom: 16px;
  }}

  h1 {{
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin: 32px 0 12px;
  }}

  h1:first-of-type {{ margin-top: 0; }}

  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
  }}

  input[type=file] {{
    width: 100%;
    font-size: 14px;
    color: var(--muted);
    margin-bottom: 14px;
  }}

  input[type=file]::file-selector-button {{
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--orange-dark);
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 10px;
    cursor: pointer;
  }}

  input[type=submit] {{
    width: 100%;
    padding: 14px;
    font-size: 15px;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    background: var(--orange);
    color: white;
    cursor: pointer;
    transition: background 0.15s ease;
  }}

  input[type=submit]:hover {{ background: var(--orange-dark); }}

  ul {{ list-style: none; padding: 0; margin: 0; }}

  li {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 14px 4px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
  }}

  li:last-child {{ border-bottom: none; }}

  .fname {{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }}

  .empty {{
    color: var(--muted);
    font-size: 14px;
    padding: 6px 4px;
  }}

  a.dl {{
    text-decoration: none;
    color: var(--orange-dark);
    font-weight: 600;
    font-size: 13px;
    white-space: nowrap;
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 8px;
  }}

  a.dl:active {{ background: var(--bg); }}

  .actions {{
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }}

  button.del {{
    appearance: none;
    background: var(--bg);
    color: var(--muted);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
  }}

  button.del:active {{ background: #ffe8e0; color: #c0392b; }}
</style>
</head>
<body>
  <div class="logo"></div>

  <h1>Загрузить файл</h1>
  <div class="card">
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file" required>
      <input type="submit" value="Загрузить">
    </form>
  </div>

  <h1>Файлы на сервере</h1>
  <div class="card">
    <ul>
      {file_items}
    </ul>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    files = sorted(os.listdir(UPLOAD_DIR))
    if files:
        items = "".join(
            f'<li><span class="fname">{f}</span>'
            f'<span class="actions">'
            f'<a class="dl" href="/download/{f}">Скачать</a>'
            f'<form action="/delete/{f}" method="post" '
            f'onsubmit="return confirm(\'Удалить файл {f}?\');" style="margin:0;">'
            f'<button class="del" type="submit">✕</button>'
            f'</form>'
            f'</span></li>'
            for f in files
        )
    else:
        items = '<li class="empty">Пока пусто</li>'
    return PAGE.format(file_items=items)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f and f.filename:
        f.save(os.path.join(UPLOAD_DIR, f.filename))
    return redirect("/")

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)

@app.route("/delete/<path:filename>", methods=["POST"])
def delete(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.commonpath([path, UPLOAD_DIR]) == UPLOAD_DIR and os.path.isfile(path):
        os.remove(path)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

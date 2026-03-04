from flask import Flask, render_template, request
from security1st.scanner.http_headers import check_headers

app = Flask(__name__)

# シンプルなHTMLテンプレートを文字列として定義（最小限の構成）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security-First 診断ツール</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        .result-box { background: #f4f4f4; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .present-true { color: green; font-weight: bold; }
        .present-false { color: red; font-weight: bold; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 20px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Security-First 診断ツール</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="診断したいURL (例: https://example.com)" required>
        <button type="submit">診断開始</button>
    </form>

    {% if results %}
        <div class="result-box">
            <h2>診断結果: {{ url }}</h2>
            {% if results.error %}
                <p style="color: red;">エラー: {{ results.error }}</p>
            {% else %}
                <table border="1" width="100%" style="border-collapse: collapse;">
                    <thead>
                        <tr style="background: #eee;">
                            <th>ヘッダー名</th>
                            <th>状態</th>
                            <th>説明</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for header, data in results.items() %}
                        <tr>
                            <td>{{ header }}</td>
                            <td class="present-{{ data.present|lower }}">{{ '有効' if data.present else '未設定' }}</td>
                            <td>{{ data.description }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endif %}
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    url = None
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            results = check_headers(url)
    return render_template_string(HTML_TEMPLATE, results=results, url=url)

# Flaskのrender_template_stringを使うためにインポートを追加
from flask import render_template_string

if __name__ == '__main__':
    print("サーバーを起動します。ブラウザで http://127.0.0.1:5000 を開いてください。")
    app.run(debug=True)

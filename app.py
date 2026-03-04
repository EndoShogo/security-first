from flask import Flask, render_template_string, request
from security1st.scanner.http_headers import check_headers
from security1st.utils.assessment import evaluate_security

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security-First 診断ツール</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .result-box { margin-top: 30px; border-top: 2px solid #eee; padding-top: 20px; }
        .present-true { color: #27ae60; font-weight: bold; }
        .present-false { color: #e74c3c; font-weight: bold; }
        input[type="text"] { width: 75%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
        button { padding: 12px 24px; cursor: pointer; background-color: #3498db; color: white; border: none; border-radius: 6px; font-size: 16px; transition: background 0.3s; }
        button:hover { background-color: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
        th { background-color: #f8f9fa; }
        .assessment { background: #fdfdfd; padding: 20px; border-radius: 8px; border-left: 5px solid #3498db; margin-top: 30px; }
        .rank { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .tasks { color: #c0392b; font-size: 14px; margin-top: 10px; list-style-type: none; padding-left: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Security-First 診断ツール</h1>
        <p style="text-align:center; color:#666;">Webサイトの安全性をヘッダー情報から検証します</p>
        
        <form method="POST" style="text-align: center; margin-top: 20px;">
            <input type="text" name="url" placeholder="診断したいURL (例: https://example.com)" value="{{ url or '' }}" required>
            <button type="submit">診断開始</button>
        </form>

        {% if results %}
            <div class="result-box">
                <h2>診断URL: <span style="font-weight:normal; font-size:16px;">{{ url }}</span></h2>
                
                {% if results.error %}
                    <p style="color: #e74c3c; background: #fadbd8; padding: 15px; border-radius: 6px;">エラー: {{ results.error }}</p>
                {% else %}
                    <table>
                        <thead>
                            <tr>
                                <th>項目名</th>
                                <th>状態</th>
                                <th>役割</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for header, data in results.items() %}
                            <tr>
                                <td><strong>{{ header }}</strong></td>
                                <td class="present-{{ data.present|lower }}">{{ '有効' if data.present else '未設定' }}</td>
                                <td>{{ data.description }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>

                    <div class="assessment">
                        <h3>総合診断結果</h3>
                        <p><strong>スコア:</strong> {{ assessment.score }}</p>
                        <p><strong>ランク:</strong> <span class="rank">{{ assessment.rank }}</span></p>
                        <p><strong>評価:</strong> {{ assessment.stability }}</p>
                        
                        {% if assessment.tasks %}
                            <p><strong>今後の課題:</strong></p>
                            <ul class="tasks">
                                {% for task in assessment.tasks %}
                                    <li>{{ task }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            <p style="color: #27ae60;"><strong>課題:</strong> 現在のところ、主要な課題は見当たりません。</p>
                        {% endif %}
                    </div>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    url = None
    assessment = None
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            results = check_headers(url)
            if 'error' not in results:
                assessment = evaluate_security(results)
    return render_template_string(HTML_TEMPLATE, results=results, url=url, assessment=assessment)

if __name__ == '__main__':
    app.run(debug=True)

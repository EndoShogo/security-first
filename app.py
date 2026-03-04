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
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; background: #f0f2f5; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        h1 { color: #1a73e8; text-align: center; }
        .result-box { margin-top: 30px; border-top: 2px solid #eee; padding-top: 20px; }
        .present-true { color: #1e8e3e; font-weight: bold; }
        .present-false { color: #d93025; font-weight: bold; }
        .cat-tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; color: white; }
        .cat-必須 { background: #d93025; }
        .cat-推奨 { background: #1a73e8; }
        .cat-モダン { background: #f29900; }
        .cat-レガシー { background: #80868b; }
        input[type="text"] { width: 75%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
        button { padding: 12px 24px; cursor: pointer; background-color: #1a73e8; color: white; border: none; border-radius: 6px; font-size: 16px; transition: background 0.3s; }
        button:hover { background-color: #1557b0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
        th, td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
        th { background-color: #f8f9fa; color: #5f6368; }
        .assessment { background: #fff; padding: 20px; border-radius: 8px; border-left: 5px solid #1a73e8; margin-top: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .rank { font-size: 28px; font-weight: bold; color: #202124; margin-right: 15px; }
        .tasks { color: #3c4043; font-size: 14px; margin-top: 10px; list-style-type: none; padding-left: 0; }
        .tasks li { margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security-First 精密診断</h1>
        <p style="text-align:center; color:#5f6368;">最新のセキュリティヘッダー（全8項目）に基づき、サイトの安全性を多角的に検証します</p>
        
        <form method="POST" style="text-align: center; margin-top: 20px;">
            <input type="text" name="url" placeholder="診断したいURL (例: https://example.com)" value="{{ url or '' }}" required>
            <button type="submit">診断開始</button>
        </form>

        {% if results %}
            <div class="result-box">
                <h2>診断対象: <span style="font-weight:normal; font-size:16px; color:#1a73e8;">{{ url }}</span></h2>
                
                {% if results.error %}
                    <p style="color: #d93025; background: #fce8e6; padding: 15px; border-radius: 6px;">エラー: {{ results.error }}</p>
                {% else %}
                    <div class="assessment">
                        <div style="display:flex; align-items:center;">
                            <span class="rank">{{ assessment.rank }}</span>
                            <span>スコア: <strong>{{ assessment.score }}</strong></span>
                        </div>
                        <p style="margin-top:10px;"><strong>評価:</strong> {{ assessment.stability }}</p>
                        
                        {% if assessment.tasks %}
                            <p style="margin-top:15px; border-top: 1px dashed #ddd; padding-top:10px;"><strong>改善アドバイス:</strong></p>
                            <ul class="tasks">
                                {% for task in assessment.tasks %}
                                    {% if '【' in task %}
                                        <li style="font-weight:bold; margin-top:10px; color:#202124;">{{ task }}</li>
                                    {% else %}
                                        <li>{{ task }}</li>
                                    {% endif %}
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>

                    <table>
                        <thead>
                            <tr>
                                <th>重要度</th>
                                <th>セキュリティ項目</th>
                                <th>状態</th>
                                <th>役割</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for header, data in results.items() %}
                            <tr>
                                <td><span class="cat-tag cat-{{ data.category }}">{{ data.category }}</span></td>
                                <td><strong>{{ header }}</strong></td>
                                <td class="present-{{ data.present|lower }}">{{ '有効' if data.present else '未設定' }}</td>
                                <td>{{ data.description }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
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
    app.run(host='127.0.0.1', port=5001, debug=True)

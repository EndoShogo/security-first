import requests

# チェック対象のセキュリティヘッダーとその詳細
# Category: 必須 (Critical), 推奨 (Important), モダン (Modern/Optional)
SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'desc': 'HTTPS接続を強制し、中間者攻撃を防止する',
        'cat': '必須'
    },
    'Content-Security-Policy': {
        'desc': 'XSSやデータ注入攻撃を強力にブロックする',
        'cat': '必須'
    },
    'X-Frame-Options': {
        'desc': 'サイトが他サイトに埋め込まれる（クリックジャッキング）のを防ぐ',
        'cat': '必須'
    },
    'X-Content-Type-Options': {
        'desc': 'ブラウザによるファイル形式の誤認（MIMEスニッフィング）を防ぐ',
        'cat': '推奨'
    },
    'Referrer-Policy': {
        'desc': 'リンク遷移時に送信されるリファラ情報を制御しプライバシーを守る',
        'cat': '推奨'
    },
    'Permissions-Policy': {
        'desc': 'カメラ、マイク、位置情報などのブラウザ機能の使用を制限する',
        'cat': 'モダン'
    },
    'Cross-Origin-Opener-Policy': {
        'desc': '閲覧コンテキストを隔離し、クロスドメイン攻撃のリスクを低減する',
        'cat': 'モダン'
    },
    'X-XSS-Protection': {
        'desc': 'ブラウザの簡易XSSフィルタを制御する (現在は非推奨・レガシー)',
        'cat': 'レガシー'
    },
}

def check_headers(url):
    """
    指定されたURLのHTTPヘッダーをスキャンし、詳細なセキュリティ設定を確認します。
    """
    results = {}
    try:
        # User-Agentを設定して一般的なブラウザを装う（ブロック回避）
        headers_to_send = {
            'User-Agent': 'Mozilla/5.0 (Security-First Diagnostic Tool)'
        }
        response = requests.get(url, headers=headers_to_send, timeout=10)
        headers = response.headers
        
        for header, info in SECURITY_HEADERS.items():
            results[header] = {
                'present': header in headers,
                'description': info['desc'],
                'category': info['cat'],
                'value': headers.get(header, 'Missing')
            }
        return results
    except requests.exceptions.RequestException as e:
        return {'error': f"接続エラー: {str(e)}"}

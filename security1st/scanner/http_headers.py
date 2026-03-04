import requests

# チェック対象のセキュリティヘッダーとその目的
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'HTTPS経由の接続を強制する',
    'Content-Security-Policy': 'XSSやデータインジェクションを防止する',
    'X-Content-Type-Options': 'MIMEスニッフィングを防止する',
    'X-Frame-Options': 'クリックジャッキングを防止する',
    'X-XSS-Protection': 'XSSフィルタリングを有効にする (レガシー)',
}

def check_headers(url):
    """
    指定されたURLのHTTPヘッダーをスキャンし、セキュリティ設定を確認します。
    """
    results = {}
    try:
        # タイムアウトを10秒に設定
        response = requests.get(url, timeout=10)
        headers = response.headers
        for header, description in SECURITY_HEADERS.items():
            results[header] = {
                'present': header in headers,
                'description': description,
                'value': headers.get(header, 'Missing')
            }
        return results
    except requests.exceptions.RequestException as e:
        return {'error': f"接続エラー: {str(e)}"}

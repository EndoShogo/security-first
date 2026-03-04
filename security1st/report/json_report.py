import json

def generate_report(results, filename='security_report.json'):
    """
    スキャン結果をJSONファイルとして保存します。
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"レポートを生成しました: {filename}")

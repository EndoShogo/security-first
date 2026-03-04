def evaluate_security(results):
    """
    スキャン結果に基づいて総合評価と課題を生成します。
    """
    if 'error' in results:
        return None

    total_headers = len(results)
    present_count = sum(1 for data in results.values() if data.get('present'))
    
    # 評価ランクの決定
    if present_count == 5:
        rank = "A (非常に安全)"
        stability = "現在の設定は完璧です。主要なセキュリティヘッダーがすべて正しく設定されています。"
    elif present_count >= 3:
        rank = "B (良好)"
        stability = "基本的なセキュリティ対策は行われていますが、一部の推奨設定が不足しています。"
    elif present_count >= 1:
        rank = "C (注意)"
        stability = "最低限の設定は確認できましたが、多くの脆弱性に対して無防備な状態です。"
    else:
        rank = "D (危険)"
        stability = "セキュリティヘッダーが全く確認できません。早急な対策が必要です。"

    # 課題（不足している項目）の抽出
    tasks = []
    for header, data in results.items():
        if not data.get('present'):
            tasks.append(f"・{header}: {data.get('description')} が設定されていません。")

    return {
        'rank': rank,
        'stability': stability,
        'tasks': tasks,
        'score': f"{present_count} / {total_headers}"
    }

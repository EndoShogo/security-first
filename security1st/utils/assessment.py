def evaluate_security(results):
    """
    スキャン結果に基づいて、重み付けされた評価と詳細な課題を生成します。
    """
    if 'error' in results:
        return None

    total_headers = len(results)
    present_headers = {h: d['present'] for h, d in results.items()}
    
    # カテゴリ別カウント
    critical_missing = [h for h, d in results.items() if d['category'] == '必須' and not d['present']]
    important_missing = [h for h, d in results.items() if d['category'] == '推奨' and not d['present']]
    modern_missing = [h for h, d in results.items() if d['category'] == 'モダン' and not d['present']]
    
    # 評価ランクの算出
    if not critical_missing:
        if not important_missing:
            rank = "S (極めて安全)"
            stability = "主要な対策が完璧に行われ、推奨設定も網羅されています。業界最高水準のセキュリティです。"
        else:
            rank = "A (安全)"
            stability = "必須となる強力な保護機能はすべて備わっています。さらに安全性を高めるための推奨設定がいくつかあります。"
    elif len(critical_missing) == 1:
        rank = "B (良好)"
        stability = "基本的な保護は行われていますが、1つ重要なセキュリティ設定が不足しています。優先的に修正すべきです。"
    else:
        rank = "C (要改善)"
        stability = "複数の重要なセキュリティ対策が欠落しています。脆弱性攻撃を受けるリスクが高い状態です。"
    
    # 重大な脆弱性がある場合の特別ランク
    if len(critical_missing) >= 3:
        rank = "D (危険)"
        stability = "サイトが非常に無防備な状態です。早急にセキュリティヘッダーの設定を見直す必要があります。"

    # 具体的な課題の生成（重要度順）
    tasks = []
    if critical_missing:
        tasks.append("【最優先課題 (Critical)】")
        for h in critical_missing:
            tasks.append(f"・{h}: {results[h]['description']}")
    
    if important_missing:
        tasks.append("【推奨改善案 (Recommended)】")
        for h in important_missing:
            tasks.append(f"・{h}: {results[h]['description']}")
            
    if modern_missing:
        tasks.append("【将来への備え (Modern)】")
        for h in modern_missing:
            tasks.append(f"・{h}: {results[h]['description']}")

    # X-XSS-Protection に関する補足（CSPがある場合）
    if results.get('Content-Security-Policy', {}).get('present') and not results.get('X-XSS-Protection', {}).get('present'):
        stability += " (※レガシーなX-XSS-Protectionは未設定ですが、CSPによって十分に補完されています。)"

    return {
        'rank': rank,
        'stability': stability,
        'tasks': tasks,
        'score': f"{sum(1 for d in results.values() if d['present'])} / {total_headers}"
    }

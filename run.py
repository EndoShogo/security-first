import argparse
import sys
from security1st.scanner.http_headers import check_headers
from security1st.report.json_report import generate_report
from security1st.utils.assessment import evaluate_security

def run_web_ui():
    """Flaskサーバーを起動してWeb UIを提供します。"""
    try:
        from app import app as flask_app
        print("\n" + "="*50)
        print("Web UIを起動します。")
        print("ブラウザで以下のURLを開いてください:")
        print("http://127.0.0.1:5001")
        print("="*50 + "\n")
        flask_app.run(host='127.0.0.1', port=5001, debug=False)
    except ImportError:
        print("エラー: Flaskがインストールされていないか、app.pyが見つかりません。")
        print("pip install Flask を実行してください。")

def main():
    parser = argparse.ArgumentParser(description='Webサイトの基本的なセキュリティ診断ツール')
    parser.add_argument('url', nargs='?', help='スキャンするWebサイトのURL')
    parser.add_argument('--web', action='store_true', help='Web UIモードで起動します')
    args = parser.parse_args()

    if args.web:
        run_web_ui()
        return

    url = args.url
    if not url:
        print("--- セキュリティ診断ツール ---")
        print("1. ターミナルで診断 (CLIモード)")
        print("2. ブラウザで診断 (Web UIモード)")
        
        try:
            choice = input("モードを選択してください (1 または 2): ").strip()
        except EOFError:
            sys.exit(0)

        if choice == '2':
            run_web_ui()
            return
        
        print("\n[CLIモード]")
        url = input("診断したいURLを入力してください (例: https://example.com): ").strip()
        if not url:
            print("URLが入力されなかったため、終了します。")
            sys.exit(0)

    # CLI診断の実行
    print(f"\nスキャンを開始します: {url}")
    header_results = check_headers(url)
    
    if 'error' in header_results:
        print(f"エラーが発生しました: {header_results['error']}")
        sys.exit(1)
    else:
        # レポート保存
        generate_report(header_results)
        
        # 評価と課題の表示
        assessment = evaluate_security(header_results)
        print("\n" + "="*30)
        print(f"【総合診断結果】")
        print(f"スコア: {assessment['score']}")
        print(f"ランク: {assessment['rank']}")
        print(f"評価: {assessment['stability']}")
        
        if assessment['tasks']:
            print("\n【今後の課題】")
            for task in assessment['tasks']:
                print(task)
        else:
            print("\n課題: 現在のところ、主要な課題は見当たりません。")
        print("="*30 + "\n")
        
        print("スキャンが正常に完了しました。\n")

if __name__ == "__main__":
    main()

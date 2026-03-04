import argparse
import sys
from security1st.scanner.http_headers import check_headers
from security1st.report.json_report import generate_report

def run_web_ui():
    """Flaskサーバーを起動してWeb UIを提供します。"""
    try:
        from app import app as flask_app
        print("\n" + "="*50)
        print("Web UIを起動します。")
        print("ブラウザで以下のURLを開いてください:")
        print("http://127.0.0.1:5000")
        print("="*50 + "\n")
        # ログが混ざらないように、Flaskのバナーを少し抑える設定で起動
        flask_app.run(host='127.0.0.1', port=5000, debug=False)
    except ImportError:
        print("エラー: Flaskがインストールされていないか、app.pyが見つかりません。")
        print("pip install Flask を実行してください。")

def main():
    parser = argparse.ArgumentParser(description='Webサイトの基本的なセキュリティ診断ツール')
    parser.add_argument('url', nargs='?', help='スキャンするWebサイトのURL')
    parser.add_argument('--web', action='store_true', help='Web UIモードで起動します')
    args = parser.parse_args()

    # --web フラグがある場合はWeb UIを起動
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
        generate_report(header_results)
        print("スキャンが正常に完了しました。\n")

if __name__ == "__main__":
    main()

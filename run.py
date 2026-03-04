import argparse
import sys
from security1st.scanner.http_headers import check_headers
from security1st.report.json_report import generate_report

def main():
    parser = argparse.ArgumentParser(description='Webサイトの基本的なセキュリティ診断ツール')
    parser.add_argument('url', nargs='?', help='スキャンするWebサイトのURL (省略した場合は対話形式)')
    args = parser.parse_args()

    url = args.url
    if not url:
        print("--- セキュリティ診断ツール ---")
        url = input("診断したいURLを入力してください (例: https://example.com): ").strip()
        if not url:
            print("URLが入力されなかったため、終了します。")
            sys.exit(0)

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

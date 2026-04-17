import requests
import os

# 国土地理院のRDF URL（HTTP）
SOURCE_URL = "http://www.gsi.go.jp/index.rdf"
# 保存先のファイル名
OUTPUT_FILE = "gsi_updates.rdf"

def fetch_and_save():
    try:
        # verify=False は証明書エラーを無視しますが、今回はHTTPなので基本不要です。
        # もしHTTPS側から取る場合は verify=False を検討してください。
        response = requests.get(SOURCE_URL, timeout=30)
        response.raise_for_status()

        # 文字化け対策（必要に応じて設定）
        response.encoding = response.apparent_encoding

        # ファイルを書き出し
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Successfully updated {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()

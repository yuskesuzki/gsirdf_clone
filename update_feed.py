from curl_cffi import requests

def fetch_and_save():
    # 最終的にリダイレクトされるHTTPSのURLを指定
    url = "https://www.gsi.go.jp/index.rdf"
    output_file = "gsi_updates.rdf"

    try:
        # impersonate="chrome" でブラウザの通信（TLSフィンガープリント含む）を完全模倣
        # OSのOpenSSLを使わないため、レガシーエラーもEOFエラーも突破できます
        response = requests.get(
            url,
            impersonate="chrome",
            verify=False,  # 証明書エラーを無視
            timeout=30
        )

        response.raise_for_status()

        # バイトデータとしてそのまま保存（文字化けリスクを排除）
        with open(output_file, "wb") as f:
            f.write(response.content)

        print(f"Success: Saved to {output_file}")

    except Exception as e:
        print(f"Critical Error: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
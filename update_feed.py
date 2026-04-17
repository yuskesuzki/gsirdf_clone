import re
from curl_cffi import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from email.utils import formatdate
from datetime import datetime
import time

def fetch_and_fix_feed():
    url = "https://www.gsi.go.jp/index.rdf"
    output_file = "gsi_updates.xml"

    # 【重要】ご自身のGitHub PagesのURLに書き換えてください（W3Cの atom:link 準拠のため）
    # 例: "https://your-username.github.io/your-repo/gsi_updates.xml"
    FEED_URL = "https://yuskesuzki.github.io/gsirdf_clone/gsi_updates.xml"

    try:
        response = requests.get(url, impersonate="chrome", verify=False, timeout=30)
        response.raise_for_status()

        raw_text = response.text
        # 構文エラーの原因となる <br> タグを事前に除去
        raw_text = re.sub(r'<br\s*/?>', ' ', raw_text, flags=re.IGNORECASE)

        soup = BeautifulSoup(raw_text, 'html.parser')

        # Atom名前空間を追加 (W3C推奨要件)
        rss = ET.Element("rss", {
            "version": "2.0",
            "xmlns:atom": "http://www.w3.org/2005/Atom"
        })
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = "国土地理院 更新情報"
        ET.SubElement(channel, "link").text = "https://www.gsi.go.jp/"
        ET.SubElement(channel, "description").text = "国土地理院のRDFを自動修復したフィードです。"

        # atom:linkの追加 (W3C推奨要件)
        ET.SubElement(channel, "atom:link", {
            "href": FEED_URL,
            "rel": "self",
            "type": "application/rss+xml"
        })

        items = soup.find_all('item')

        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            desc_tag = item.find('description')
            date_tag = item.find('dc:date') or item.find('date')

            title = title_tag.get_text(separator=" ", strip=True) if title_tag else "タイトルなし"

            # 【修正点1】linkタグの取得方法を強化（空要素問題の回避）
            # RDFの仕様上、itemの属性(rdf:about)にURLが入っていることが多いのでまずそれを探す
            link_url = item.get('rdf:about') or item.get('about')
            # 属性にない場合、linkタグの「隣のテキスト」としてパースされてしまったURLを拾う
            if not link_url and link_tag and isinstance(link_tag.next_sibling, str):
                link_url = link_tag.next_sibling.strip()

            # それでも見つからない場合のフォールバック
            if not link_url or not link_url.startswith("http"):
                link_url = "https://www.gsi.go.jp/"

            description = desc_tag.get_text(separator=" ", strip=True) if desc_tag else ""
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            pub_date = formatdate(time.time())
            if date_str:
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    pub_date = formatdate(dt.timestamp())
                except Exception:
                    pass

            rss_item = ET.SubElement(channel, "item")
            ET.SubElement(rss_item, "title").text = title
            ET.SubElement(rss_item, "link").text = link_url
            ET.SubElement(rss_item, "description").text = description
            ET.SubElement(rss_item, "pubDate").text = pub_date

            # 【修正点2】guid要素の追加 (W3C推奨要件)
            ET.SubElement(rss_item, "guid", {"isPermaLink": "true"}).text = link_url

        tree = ET.ElementTree(rss)
        if hasattr(ET, 'indent'):
            ET.indent(tree, space="  ", level=0)

        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Success: Parsed and saved as valid RSS 2.0 to {output_file}")

    except Exception as e:
        print(f"Critical Error: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_fix_feed()

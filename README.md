# gsirdf_clone
国土地理院のRDFがそのままSlackで閲覧できないので、定期的に更新をチェックして、このリポジトリの Github Pagesで転送してみる。

# 使い方
1. `git clone` してローカルにリポジトリをコピーする。
2. uv をインストールする。
3. `uv sync` を実行して、依存関係をインストールする。
4. `uv run update_feed.py` を実行して、RDFを更新する。

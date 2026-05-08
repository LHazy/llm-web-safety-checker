# これはなに？
LLMにWebサイトのコンテンツが安全かどうかを判断してもらうツールです。

# セットアップ
1. Dockerをインストールしてください。
2. コンテナのビルド
```bash
docker build -t llm-web-safety-checker .
```

# 使い方
```bash
docker run --rm llm-web-safety-checker <url>
```
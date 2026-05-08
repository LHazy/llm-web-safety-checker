# これはなに？
LLMにWebサイトのコンテンツが安全かどうかを判断してもらうツールです。

# セットアップ
1. Dockerをインストールしてください。
2. コンテナのビルド
```bash
docker build -t llm-web-safety-checker .
```

# サンプル
1. OllamaでGemma4:31bを取得
```
ollama pull gemma4:31b
```
2. Ollamaサーバーを起動
```
ollama.exe run gemma4:31b
```
3. dockerコマンドでURLを指定して実行
```bash
docker run --rm llm-web-safety-checker --model-endpoint http://host.docker.internal:11434/ --model-id gemma4:31b <url>
```
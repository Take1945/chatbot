履修要綱RAGチャットボット

大学の履修要綱PDFをもとに、自然言語で質問できるチャットボットです。

デモ
🔗 https://chat-risyu-bot.vercel.app

概要
RAGという技術を使い、履修要綱のPDFから関連する情報を検索し、AIが回答を生成します。「1年生が取れる単位は？」のような質問に、PDF内の情報をもとに答えます。


技術スタック


フロントエンド
Vite / React
TypeScript

バックエンド

FastAPI（Python）
LangChain
Docling（PDF解析）
PGVector（ベクトル検索）
OpenAI API（gpt-4o-mini）

インフラ

Vercel（フロントエンド）
Render（バックエンド）
Supabase（PostgreSQL + pgvector）

工夫した点

Doclingのメモリ不足問題を、画像解像度の調整とページ画像生成の無効化で解決
PDF解析（ingest）と質問応答（chat）を分離し、本番環境では軽量なchat機能のみをデプロイ
HybridChunkerによるトークン数を考慮したチャンク分割（最大300トークン）

参考

初めてのLangChain（O'Reilly）
LangChain公式ドキュメント

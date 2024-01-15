# DiscordBotVoiceState

## 概要

* Discordのチャンネル入退室監視用bot
* ロビー or Gamingボイスチャンネルの入退室通知を特定のメッセージチャンネルとLINEに行う

## 環境

* docker-composeで構築

### ライブラリ

* [Discord.py](https://discordpy.readthedocs.io/ja/latest/api.html)
* python-dotenv
  * 環境変数ファイルの読み込み
* requests
  * LINE通知のHTTP通信

# DiscordBotVoiceState

## 概要

* Discordのチャンネル入退室監視用bot
* ロビー or Gamingボイスチャンネルの入退室通知を特定のメッセージチャンネルとLINEに行う

## 環境

* 自宅サーバーやEC2で使えるようにdocker-composeでPython環境を構築 
* LINE通知はLINE Notifyを使用

## ライブラリ

* [Discord.py](https://discordpy.readthedocs.io/ja/latest/api.html)
* python-dotenv
  * 環境変数ファイルの読み込み
* requests
  * LINE通知のHTTP通信

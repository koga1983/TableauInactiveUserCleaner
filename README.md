# 🚀 Tableau User Cleanup Script

このリポジトリには、Tableau ServerおよびTableau Cloud上のユーザーのアクセス権をレビューし、古いユーザーを削除するPythonスクリプトが含まれています。Slack通知機能を使用して、削除予定のユーザーに1週間前に通知し、実際の削除後にも通知を行います。

## 📋 必要条件

- Tableau Server または Tableau Online のアカウント
- API トークン
- Python 3.6以上
- Tableau Server Client ライブラリ
- SlackワークスペースとBotトークン

## 📁 ファイル構成

- `config.json`: 設定情報を含むファイル。
- `main.py`: メインのPythonスクリプト。
- `requirements.txt`: 必要なライブラリを記載したファイル。

## 🛠️ 設定

1. `config.json` ファイルにTableau ServerまたはTableau CloudとSlackの認証情報を入力します。

```json
{
  "tableau": {
    "server_url": "your_tableau_server_or_cloud_url",
    "personal_access_token_name": "your_personal_access_token_name",
    "personal_access_token": "your_personal_access_token",
    "site_id": "your_site_id"
  },
  "slack": {
    "slack_bot_token": "your_slack_bot_token",
    "slack_channel_id": "your_slack_channel_id"
  }
}
```

## ▶️ 実行方法

以下のコマンドを実行して必要なライブラリをインストールし、スクリプトを実行します：

```sh
pip install -r requirements.txt
python main.py
```

## 📦 必要なライブラリ

プロジェクトに必要なライブラリは `requirements.txt` ファイルに記載されています：

```plaintext
tableauserverclient
slack_sdk
pytz
```

## 🌟 機能

- JSONファイルから設定情報を読み込みます。
- Tableau ServerまたはTableau Cloudの認証にPersonalAccessTokenAuthを使用します。
- 最後のログインから指定された期間（デフォルトは90日）以上経過したユーザーを特定します。
- 削除予定のユーザーを1週間前にSlackに通知します。
- 指定されたユーザーを削除し、削除後にSlackに通知します。

## 📋 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、`LICENSE`ファイルを参照してください。

---

## 📚 詳細情報

- **Tableau Server Client ドキュメント**: [Tableau Server Client Library](https://tableau.github.io/server-client-python/docs/)
- **Tableau REST API ドキュメント**: [Tableau REST API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm)

## 💡 注意事項

このスクリプトを実行する際には、適切なAPIトークンとアクセス権限が必要です。APIトークンの管理には十分注意してください。

---


### 🌟 **スターを付けてください！** 🌟

このリポジトリが役に立った場合は、スターを付けてください。あなたのサポートが私たちの励みになります！

[![GitHub Stars](https://img.shields.io/github/stars/koga1983/TableauInactiveUserCleaner?style=social)](https://github.com/koga1983/TableauInactiveUserCleaner/stargazers)
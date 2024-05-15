import tableauserverclient as TSC
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pytz
import json


# JSONファイルから設定情報を読み込む関数
def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


# Slackにメッセージを送信する関数
def send_slack_message(client, channel_id, blocks):
    try:
        response = client.chat_postMessage(channel=channel_id, blocks=blocks)
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")


# 古いユーザーや不要なアクセス権を削除する関数
def review_and_cleanup_users(server, slack_client, channel_id, threshold_days=90, notify_days=7):
    with server.auth.sign_in(server_auth):
        all_users, pagination_item = server.users.get()
        now = datetime.now(pytz.utc)  # 現在時刻をUTCに設定
        threshold_date = now - timedelta(days=threshold_days)
        notify_date = now - timedelta(days=threshold_days - notify_days)

        removed_users = []
        users_to_notify = []
        users_to_remove = []

        for user in all_users:
            if user.last_login:
                last_login_utc = user.last_login.astimezone(pytz.utc)
                if last_login_utc < notify_date and last_login_utc >= threshold_date:
                    users_to_notify.append(user)
                elif last_login_utc < threshold_date:
                    users_to_remove.append(user)

        if users_to_notify:
            pre_removal_message_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*以下のユーザーは、{threshold_days}日以上アクティブではなかったため、1週間後に削除される予定です:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join(
                            [f"- {user.name} (最終ログイン: {user.last_login})" for user in users_to_notify])
                    }
                }
            ]
            send_slack_message(slack_client, channel_id, pre_removal_message_blocks)

        if users_to_remove:
            for user in users_to_remove:
                print(f"Removing user: {user.name}, last login: {user.last_login}")
                server.users.remove(user.id)
                removed_users.append(user.name)

            post_removal_message_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*以下のユーザーが削除されました:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join([f"- {user}" for user in removed_users])
                    }
                }
            ]
            send_slack_message(slack_client, channel_id, post_removal_message_blocks)
        else:
            no_removal_message_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{threshold_days}日以内にすべてのユーザーがログインしています。削除されるユーザーはいません。*"
                    }
                }
            ]
            send_slack_message(slack_client, channel_id, no_removal_message_blocks)

        print("User review and cleanup completed.")


if __name__ == "__main__":
    config = load_config()

    tableau_config = config['tableau']
    slack_config = config['slack']

    server = TSC.Server(tableau_config['server_url'], use_server_version=True)
    server_auth = TSC.PersonalAccessTokenAuth(
        tableau_config['personal_access_token_name'],
        tableau_config['personal_access_token'],
        tableau_config['site_id']
    )

    slack_client = WebClient(token=slack_config['slack_bot_token'])
    slack_channel_id = slack_config['slack_channel_id']

    print(f"Starting user review and cleanup at {datetime.now()}")
    review_and_cleanup_users(server, slack_client, slack_channel_id, threshold_days=90, notify_days=7)
    print("Completed user review and cleanup.")

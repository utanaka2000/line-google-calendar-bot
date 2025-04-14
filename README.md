# Line Google Calendar Bot

## 準備

### Google Calendar

1. [公式ページ](https://developers.google.com/workspace/calendar/api/quickstart/python?hl=ja)を参考に`credentials.json`を取得する
2. `token.json`を生成する

    ```bash
    poetry run python src/google_calendar/quickstart.py
    ```

3. `token.json`をsecretsに登録する

    ```bash
    gcloud secrets create oauth2-token --data-file=token.json
    ```

### Line

1. 予定を送信したいグループのIDを確認する。

    ```bash
    poetry run uvicorn src.line.get_line_group_id:app --host 0.0.0.0 --port 8900 --reload
    ```

2. [ngrok](https://dashboard.ngrok.com/get-started/setup/macos) で一時的なURLを払い出す

3. Lineのwebhookに2のURLを登録し、確認したいグループで何か投稿すると、コンソールにprintされるのでメモする

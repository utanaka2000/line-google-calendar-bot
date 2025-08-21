# Line Google Calendar Bot

Line のトークルームに Google カレンダーの予定のリマインドを投下するボット。

以前はLine Notifyを利用してIFTTTなどでノーコードで作成できたが、Line Notify がサービス終了したため、現状ノーコードはおそらく存在しない。

公式 Line アカウントを作成して Line Messaging API を利用する。
実行は、Google Cloud Functions + Cloud Scheduler 上で行う。

## 準備

### Google Calendar

1. [公式ページ](https://developers.google.com/workspace/calendar/api/quickstart/python?hl=ja)を参考に`credentials.json`を取得する
2. `token.json`を生成する

    ```bash
    poetry run python src/google_calendar/quickstart.py
    ```

3. token.json の内容を`.env.yaml`に書く

    ```yaml
    CALENDAR_TOKEN_JSON: '{"token": "... }'
    ```

### Line

#### APIトークンの確認

チャネルアクセストークンを確認し、`.env.yaml`に書く

```yaml
LINE_CHANNEL_ACCESS_TOKEN: XXX...
```

#### 送信先グループIDの確認

予定を送信したいグループのIDを確認する。webhook用のエンドポイントをホストして、それに対するリクエストボディから確認する。

1. webhook用のエンドポイントをローカルにホストする

    ```bash
    poetry run uvicorn src.line.get_line_group_id:app --host 0.0.0.0 --port 8900 --reload
    ```

2. [ngrok](https://dashboard.ngrok.com/get-started/setup/macos) で一時的なURLを払い出す

3. Lineのwebhookに2のURLを登録する

4. 確認したいグループで何か投稿すると、コンソールにprintされるので`.env.yaml`に書く

  ```yaml
  LINE_USER_ID: XXX...
  ```

## GCP

### Cloud Run Function

#### 権限設定

```bash
# Cloud Functions 用のサービスアカウントを作成
gcloud iam service-accounts create my-function-sa \
  --display-name "Cloud Functions Service Account"
# Cloud Functions にsecretへのアクセス権限を付与
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:my-function-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### デプロイ実行

```sh
gcloud functions deploy hello_world --runtime python312 \
 --trigger-http --entry-point main \
 --env-vars-file .env.yaml \
 --service-account my-function-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
 --no-allow-unauthenticated --region=asia-northeast1 \
 --gen2
```

### Cloud Scheduler

#### 権限設定

```bash
# Cloud Schedular 用のサービスアカウントを作成
gcloud iam service-accounts create my-schedular-sa \
  --display-name "Cloud Schedular Service Account"
# Cloud Schedular にFunctionsへのOIDC認証を付ける
gcloud functions add-iam-policy-binding FUNCTION_NAME \
  --member="serviceAccount:SCHEDULER_SA@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker" --region=asia-northeast1
```

#### デプロイの実行

```bash
# なぜか以下はエラーが出てCLIでは作れなかったので手動で作る
gcloud scheduler jobs create http my-scheduled-job \
  --schedule "0 19 * * *" \
  --uri https://REGION-PROJECT_ID.cloudfunctions.net/my-scheduled-function \
  --http-method GET \
  --time-zone "Asia/Tokyo" \
 --location asia-northeast1 \ --oidc-service-account-email scheduler-sa@PROJECT_ID.iam.gserviceaccount.com
```

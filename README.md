# haro とは

ハロ(haro)は、Slack用のBotです。
Slackに通知されたAlert Managerからのアラートメッセージを受け、スマート電源タップ(Meross)の電源を制御します。

これにより、ユニコーンガンダムのNT-Dを発動させ光らせること等ができます。

デモ動画は[こちら](https://youtu.be/0-yCTHrpOm0)を参照ください。

# セットアップ方法

## コマンドで起動する場合

1. 環境変数を設定

```
$ export SLACK_APP_TOKEN=<Slack Appのトークン (e.g., xapp-x-xxx)>
$ export SLACK_BOT_TOKEN=<Slack Botのトークン (e.g., xoxb-xxxxx)>
$ export ALERTMANAGER_ID=<Slackでの AlertManagerのBot ID (e.g., B03DZ3JPES2)>
$ export MEROSS_EMAIL=<Merossのユーザ登録しているメールアドレス>
$ export MEROSS_PASSWORD=<Merossのパスワード>
$ export MEROSS_DEVICE_TYPE=<Merossのデバイスタイプ (e.g., mss425f)>
$ export MEROSS_DEVICE_NAME=<Merossのデバイス名 (e.g., tap1)>
$ export MEROSS_DEVICE_CHANNEL=<Meross上のコンセント番号 (e.g., 3)>
```

2. Pythonのパッケージをインストール

```
$ pip install -r requirements.txt
```

3. haro.pyを実行

```
$ cd manifests
$ python ./haro.py
```

## Kubernetes上で起動する場合

1. ネームスペースを作成

```
$ kubectl create ns haro
```

2. secret.yaml を作成

```YAML
apiVersion: v1
kind: Secret
metadata:
  name: haro
  namespace: haro
type: Opaque
data:
  SLACK_APP_TOKEN: <Slack Appのトークン (e.g., xapp-x-xxx)>
  SLACK_BOT_TOKEN: <Slack Botのトークン (e.g., xoxb-xxxxx)>
  ALERTMANAGER_ID: <Slackでの AlertManagerのBot ID (e.g., B03DZ3JPES2)>
  MEROSS_EMAIL: <Merossのユーザ登録しているメールアドレス>
  MEROSS_PASSWORD: <Merossのパスワード>
  MEROSS_DEVICE_TYPE: <Merossのデバイスタイプ (e.g., mss425f)>
  MEROSS_DEVICE_NAME: <Merossのデバイス名 (e.g., tap1)>
  MEROSS_DEVICE_CHANNEL: <Meross上のコンセント番号 (e.g., 3)>
```

:memo: 各値はbase64でエンコードした値を設定してください。

(e.g., Base64へのエンコードの実行例)
```
$ echo -n "xapp-x-xxx" |base64
```

3. secret.yamlのデプロイ

```
$ kubectl apply -f secret.yaml
```

4. haroのデプロイ

```
$ kubectl apply -k manifests/
```

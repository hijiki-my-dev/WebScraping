# ライトノベルの新刊情報をスクレイピングして、Notionに追加するプログラム。

電撃文庫やMF文庫などの新刊情報をスクレイピングし、その結果をNotionに通知するアプリです。2年前の時点より大幅な変更を行い、Google Cloud Runへデプロイすることで自動的に定期実行が行われるよう改修しました。<br>スクレイピング元のサイトに関して、規約に違反していないことは確かめていますが、今後規約の変更でスクレイピングが禁止となる場合も考えられます。使用については自己責任でお願いいたします。<br>

## 仕様

- 各レーベルの新刊の欄から情報を取得して、以下の内容をNotionのデータベースに追加する。
    - タイトル
    - 発売日
    - レーベル
    - 追っている作品かどうか
- タイトルが既存のものに完全に一致している場合は、データベースに追加しない。
- 60日以上前に追加した内容は（追っている作品以外は）削除する。
- ローカルでの実行時は、config.pyを変えて直接job.pyを動かす
    - 定期実行はcronやタスクスケジューラを用いる。ただし、PCが起動していないと実行できない。
- 基本的にはGoogle Cloud等のクラウドサービスを使用する想定。
    - Google Cloud Runにデプロイし、スケジューラーを用いて定期実行。Flaskを用いてエンドポイントを作成し、そこへスケジューラーからリクエストを送る。
    - cronとは異なり、PCスリープ時にも問題なく起動
    - 新刊を追っている作品を記載したファイルをCloud Storage上に保存することで、作品リストの更新も容易に行える。

## 追記
- 2023-04-09
    - Notion APIの呼び出し制限（データベースのアイテム100個まで）により、作品を重複して追加してしまう不具合を修正。
- 2023-09-15
    - ガガガ文庫作品の発売日を18日固定としていたので、18日以外の発売でも対応できるように修正。
    - その他のコードについても一部内容を修正。
- 2023-10-10
    - requirements.txtを追加。現時点でrequestsを最新バージョンにすると一部サイトにアクセスできない。
- 2025-03
    - Google Cloudへのデプロイに対応するため、app.pyやDockerfile等を追加
    - コードを分割し、全体を大幅に改修
    - タイプヒント等のリファクタと、ログの追加を実施
    - 課金の関係からAzure Functions用のブランチを作成（azure）。mainブランチはGoogleCloudのまま。
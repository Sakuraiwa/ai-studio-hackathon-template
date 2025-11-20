# repository-template

このリポジトリは各プロジェクトを開始する際にテンプレートとして利用するためのリポジトリです。<br/>
Startapp v2を実行すると、このリポジトリをテンプレートとして新しいリポジトリを作成します。<br/>
リポジトリの初期構築時に最初から設定しておきたいリポジトリごとの設定は、こちらに反映してください。

併せてStartapp v2の説明も確認してください。

## コピーされる設定


現在、以下の初期設定がコピーされます。

* ブランチ（main / develop）の作成
* デフォルトブランチをdevelopに設定
* ISSUEテンプレートとPRテンプレートの設定
* developへのマージはPRRを経なければエラーとなるよう設定（[Branches Protection Rule](https://github.com/dottIO/repository-template/settings/branches)）

なお、以下の設定はテンプレートからはコピーされません。
* ラベルの追加（feedback,backend等）　※Startapp v2にて自動設定
* PRマージ時にfeatureブランチの自動削除
* Branch Protection Rule


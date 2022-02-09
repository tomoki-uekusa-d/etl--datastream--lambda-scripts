# etl--datastream--lambda-scripts

AWS Lambda scripts for datastream

## Log format


項目         | 型     | 備考                       | 例
-------------|--------|:---------------------------|:------------------------------------
service_name | string | サービス名                     | dev-listengo-requests
log_platform | string | プラットフォーム名                 | cloudlogging
time         | string | 時刻 (yyyy-MM-dd HH:mm:ss) | 2021-10-18 20:20:30
log_type     | string | ログの種類                    | access, error, smtp, etc...
facility     | string | ファシリティ                     | error, warning, critial, fatal, info
client       | string | クライアントのホスト名,IP名          | 23.11.165.4
server       | string | サーバーのホスト名,ALB,ELB,IP      | test-music.dwango.jp
method       | string | アクセス方法                   | GET, POST, OPTIONS, HEAD, etc...
access_path  | string | アクセスパス                     | /noren/item/material/253/1004304
server_port  | integer | ポート番号                    | 443
protocol         | string |              プロトコル              | http|https|etc
protocol_version | string |       プロトコルバージョン                     | HTTP/1.1, HTTP/2.0
response_code    | string |               レスポンスコード             | 200, 403, etc...
user_agent       | string |           ユーザーエージェント                 | Mozilla/XXXXXXXXXXXXXX
message          | string |            オリジナルメッセージ                | ""
org_body          | string|          ログ原文 | "2021-10-18\t20...."


## reference

- https://paper.dropbox.com/doc/DataFormat--BUnoeYThGf6Yjk5QxmFQ9EuPAg-JylWIfhxxpgGCtW3RIiBu
- https://paper.dropbox.com/doc/LogDataFormat--BUnV2Skq~zXCme_JhWLzJyjiAg-ZBEMlOq1JGltPzazNgEP8

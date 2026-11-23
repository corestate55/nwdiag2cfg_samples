# diagrams コンフィグ生成レポート

- 入力: `diagrams.drawio.svg`（sha256: `a8d46f58f5ba8cd4`）
- 対象タブ: 「物理・論理合成図_4C」
- 補助タブ: 「論理構成図_4C」
- 既定値ファイル: なし（すべてナレッジ v1.1 の既定値）
- ツール: nwdiag2cfg 0.1.0（ナレッジ v1.1 準拠）
- 作成日: 2026-11-23

## 0. 要約

- コンフィグ: 18 台（`configs/`）。無線AP・サーバーは対象外（9章）
- 指摘: ERROR 4 / WARN 38 / INFO 16 件（review.md）
- 未確定値（<TBD>）: 132 箇所（6章）

**ERROR の指摘**

- R-001 A-01 os1 MGMT ⇔ tk1 DMZ: アドレスが同じ（172.17.2.0/24 と 172.17.2.0/24）（暫定: os1 MGMT は論理構成図の 172.18.1.0/24 を採用【論】）
- R-002 A-01 os1 MGMT ⇔ tk1 MGMT: アドレスが同じ（172.17.2.0/24 と 172.17.2.0/24）（暫定: 別の指摘の解決で重複が解消（os1 MGMT=172.18.1.0/24【論】 / tk1 MGMT=172.17.2.0/24【図】））
- R-003 A-01 tk1 DMZ ⇔ tk1 MGMT: アドレスが同じ（172.17.2.0/24 と 172.17.2.0/24）（暫定: tk1 MGMT は論理構成図の 172.17.1.0/24 を採用【論】）
- R-004 A-07 172.17.2.0/24MGMT,VLAN9: 同じアドレスのラベル「172.17.2.0/24MGMT,VLAN9」が複数の拠点（os1, tk1）にある（暫定: A-01 の扱いに従う）

## 1. 機種判定

| 機器 | 図の記載 | 判定 | 採用した記法 | 理由 |
|---|---|---|---|---|
| os1-core01 | C社 L3switch 9000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| os1-core02 | C社 L3switch 9000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| os1-fmacc01 | C社 L2switch 1000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| os1-fmacc02 | C社 L2switch 1000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| os1-fw01 | C社 Firewall 3000 | 特定不能 | Cisco ASA | 図の Vendor Model「C社 Firewall 3000」は実在のベンダー名・型番として読めない。ファイアウォールとして ASA 記法を採用（同一セグメントの2ポートを BVI で表現できる）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| os1-rt01 | C社 Router 1000 | 特定不能 | Cisco IOS-XE（ISR 相当） | 図の Vendor Model「C社 Router 1000」は実在のベンダー名・型番として読めない。ルーターとして静的経路・スイッチポート＋SVI を書ける ISR（IOS-XE）を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-core01 | C社 L3switch 9000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-core02 | C社 L3switch 9000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-fnacc01 | C社 L2switch 1000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-fnacc01-dup2 | C社 L2switch 1000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-fw01 | C社 Firewall 3000 | 特定不能 | Cisco ASA | 図の Vendor Model「C社 Firewall 3000」は実在のベンダー名・型番として読めない。ファイアウォールとして ASA 記法を採用（同一セグメントの2ポートを BVI で表現できる）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-mgmt01 | C社 L2switch 1000-48 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-48」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-mgmt02 | C社 L2switch 1000-48 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 1000-48」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-rt01 | C社 Router 1000 | 特定不能 | Cisco IOS-XE（ISR 相当） | 図の Vendor Model「C社 Router 1000」は実在のベンダー名・型番として読めない。ルーターとして静的経路・スイッチポート＋SVI を書ける ISR（IOS-XE）を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-sr1acc01 | C社 L2switch 3000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-sr1acc01-dup2 | C社 L2switch 3000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-sr1acc02 | C社 L2switch 3000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |
| tk1-sr1acc02-dup2 | C社 L2switch 3000-24 | 特定不能 | Cisco IOS-XE（Catalyst 9000 相当） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す |

## 2. 抽出サマリ

### 2.1 機器台帳

| 機器 | 図のホスト名（仮称のとき） | 機種 | 役割 | 拠点 | 冗長ペア | 出力 | cell |
|---|---|---|---|---|---|---|---|
| os1-core01 |  | C社 L3switch 9000-24 | L3SW | os1 | os1-core02 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-162 |
| os1-core02 |  | C社 L3switch 9000-24 | L3SW | os1 | os1-core01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-142 |
| os1-fmacc01 |  | C社 L2switch 1000-24 | L2SW | os1 | os1-fmacc02 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-521 |
| os1-fmacc02 |  | C社 L2switch 1000-24 | L2SW | os1 | os1-fmacc01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-581 |
| os1-fmap01 |  | Wifi AP | 無線AP | os1 |  | 設定項目表 | 9BYiFAK1cGA9hBdD1Cum-522 |
| os1-fmap02 |  | Wifi AP | 無線AP | os1 |  | 設定項目表 | 9BYiFAK1cGA9hBdD1Cum-523 |
| os1-fw01 |  | C社 Firewall 3000 | FW | os1 |  | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-143 |
| os1-rt01 |  | C社 Router 1000 | ルーター | os1 |  | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-144 |
| tk1-svr101-dup2 | tk1-svr101 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | os1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-557 |
| tk1-svr101-dup3 | tk1-svr101 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | os1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-583 |
| tk1-cdns01 |  | Linux/djbdns | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-273 |
| tk1-cdns01-dup2 | tk1-cdns01 | Linux/djbdns | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-571 |
| tk1-core01 |  | C社 L3switch 9000-24 | L3SW | tk1 | tk1-core02 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-148 |
| tk1-core02 |  | C社 L3switch 9000-24 | L3SW | tk1 | tk1-core01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-147 |
| tk1-f6ap01 |  | Wifi AP | 無線AP | tk1 |  | 設定項目表 | 9BYiFAK1cGA9hBdD1Cum-375 |
| tk1-f6ap02 |  | Wifi AP | 無線AP | tk1 |  | 設定項目表 | 9BYiFAK1cGA9hBdD1Cum-376 |
| tk1-fnacc01 |  | C社 L2switch 1000-24 | L2SW | tk1 | tk1-fnacc01-dup2 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-374 |
| tk1-fnacc01-dup2 | tk1-fnacc01 | C社 L2switch 1000-24 | L2SW | tk1 | tk1-fnacc01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-488 |
| tk1-fw01 |  | C社 Firewall 3000 | FW | tk1 |  | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-145 |
| tk1-mgmt01 |  | C社 L2switch 1000-48 | L2SW | tk1 | tk1-mgmt02 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-360 |
| tk1-mgmt02 |  | C社 L2switch 1000-48 | L2SW | tk1 | tk1-mgmt01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-503 |
| tk1-proxy01 |  | Linux/Squid | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-272 |
| tk1-proxy01-dup2 | tk1-proxy01 | Linux/Squid | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-570 |
| tk1-rt01 |  | C社 Router 1000 | ルーター | tk1 |  | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-146 |
| tk1-sr1acc01 |  | C社 L2switch 3000-24 | L2SW | tk1 | tk1-sr1acc02 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-231 |
| tk1-sr1acc01-dup2 | tk1-sr1acc01 | C社 L2switch 3000-24 | L2SW | tk1 | tk1-sr1acc02-dup2 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-406 |
| tk1-sr1acc02 |  | C社 L2switch 3000-24 | L2SW | tk1 | tk1-sr1acc01 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-392 |
| tk1-sr1acc02-dup2 | tk1-sr1acc02 | C社 L2switch 3000-24 | L2SW | tk1 | tk1-sr1acc01-dup2 | コンフィグ | 9BYiFAK1cGA9hBdD1Cum-447 |
| tk1-svr101 |  | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-232 |
| tk1-svr102 |  | D社 RackMountServer X100V社 Hypervisor (業務アプリ/本番系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-476 |
| tk1-svr108 |  | D社 RackMountServer X100V社 Hypervisor (業務アプリ/開発系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-477 |
| tk1-svr201 |  | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-545 |
| tk1-svr202 |  | D社 RackMountServer X100V社 Hypervisor (業務アプリ/本番系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-546 |
| tk1-svr208 |  | D社 RackMountServer X100V社 Hypervisor (業務アプリ/開発系) | サーバー | tk1 |  | 対象外 | 9BYiFAK1cGA9hBdD1Cum-547 |

### 2.2 セグメント台帳

| 拠点 | 色 | 名前 | VLAN | アドレス | 出所 | VIP | L3（バッジ） | 払い出し単位 |
|---|---|---|---|---|---|---|---|---|
| os1 | #CC0000 | EXT | 2 | 172.18.0.0/27 | 【図】 | .6 | os1-core01 .4; os1-core02 .5; os1-fw01 .1; os1-rt01 .2 |  |
| os1 | #6600CC | MGMT | 9 | 172.18.1.0/24 | 【論】 | .3 | os1-core01 .1; os1-core02 .2; os1-fmacc01 .x; os1-fmacc02 .x |  |
| os1 | #CC6600 | DMZ | 10 | 172.18.2.0/24 | 【図】 | .3 | os1-core01 .1; os1-core02 .2 |  |
| os1 | #007FFF | COMMON | 11 | 172.18.3.0/24 | 【図】 | .3 | os1-core01 .1; os1-core02 .2 |  |
| os1 | #999900 | OFFICE_Fn | 300-399 | 172.18.64.0/18 | 【図】 | .3 | os1-core01 .x; os1-core02 .x+1 | フロア（【論】） |
| os1 | #9999FF | INTER-BLDG | - | 172.16.0.0/24 | 【図】 |  | os1-rt01 .x |  |
| os1 | #FF66FF | OS-INET | - | 203.0.113.0/25 | 【図】 |  | os1-fw01 .x |  |
| tk1 | #CC0000 | EXT | 2 | 172.17.0.0/27 | 【図】 | .6 | tk1-core01 .4; tk1-core02 .5; tk1-fw01 .1; tk1-rt01 2 |  |
| tk1 | #6600CC | MGMT | 9 | 172.17.1.0/24 | 【論】 | .3 | tk1-core01 .1; tk1-core02 .2; tk1-fnacc01 .x; tk1-fnacc01-dup2 .x; tk1-mgmt01 .x; tk1-mgmt02 .x |  |
| tk1 | #CC6600 | DMZ | 10 | 172.17.2.0/24 | 【図】 | .3 | tk1-core01 .1; tk1-core02 .2 |  |
| tk1 | #007FFF | COMMON | 11 | 172.17.3.0/24 | 【図】 | .3 | tk1-core01 .1; tk1-core02 .2 |  |
| tk1 | #009900 | APx_PROD | 100-199 | 172.17.128.0/18 | 【図】 | .3 | tk1-core01 .1; tk1-core02 .2 | 業務アプリ（【図注記】） |
| tk1 | #66CC00 | APx_DEV | 200-299 | 172.17.192.0/18 | 【図】 | .3 | tk1-core01 .1; tk1-core02 .2 | 注記なし |
| tk1 | #999900 | OFFICE_Fn | 300-399 | 172.17.64.0/18 | 【図】 | .3 | tk1-core01 .x; tk1-core02 .x+1 | フロア（【論】） |
| tk1 | #9999FF | INTER-BLDG | - | 172.16.0.0/24 | 【図】 |  | tk1-rt01 .x |  |
| tk1 | #FF66FF | TK-INET | - | 198.51.100.0/25 | 【図】 |  | tk1-fw01 .x |  |

### 2.3 結線表

| A | 端点A | B | 端点B | 線幅 | ケーブル（凡例） | LAG | 線 cell |
|---|---|---|---|---|---|---|---|
| os1-core01 Te0/2 | ○ | os1-rt01 Gi0/2 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-754 |
| os1-core01 Te0/4 | ● | tk1-svr101-dup3 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-757 |
| os1-core01 Te0/5 | ● | os1-fmacc01 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-759 |
| os1-core01 Te0/23 | ● | os1-core02 Te0/23 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-108 |
| os1-core01 Te0/24 | ● | os1-core02 Te0/24 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-106 |
| os1-core02 Gi0/1 | ● | os1-fmacc02 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-582 |
| os1-core02 Te0/4 | ● | tk1-svr101-dup3 eth2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-758 (推定) |
| os1-fmacc01 Gi0/1 | - | os1-fmap01 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-507 |
| os1-fmacc01 Gi0/3-20 | - | オフィス固定端末 x5-10 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-527 |
| os1-fmacc01 Gi0/21 | - | tk1-svr101-dup2 BMC | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-604 |
| os1-fmacc01 Gi0/23 | - | os1-fmacc02 Gi0/23 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-543 |
| os1-fmacc01 Gi0/24 | - | os1-fmacc02 Gi0/24 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-544 |
| os1-fmacc02 Gi0/1 | - | os1-fmap02 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-511 |
| os1-fmacc02 Gi0/3-20 | - | オフィス固定端末 x5-10 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-528 |
| os1-fmacc02 Gi0/21 | - | tk1-svr101-dup3 BMC | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-605 |
| os1-fw01 Te0/1 | ● | 回線終端装置 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-92 |
| os1-fw01 Te0/2 | ● | os1-core01 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-580 |
| os1-fw01 Te0/3 | ● | os1-core02 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-755 |
| os1-rt01 Gi0/1 | - | 回線終端装置 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-97 |
| os1-rt01 Gi0/3 | - | os1-core02 Te0/2 | ○ | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-101 |
| tk1-core01 Mgmt | - | tk1-mgmt01 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-200 |
| tk1-core01 Te0/1 | ● | tk1-fw01 Te0/2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-309 |
| tk1-core01 Te0/2 | ○ | tk1-rt01 Gi0/2 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-22 |
| tk1-core01 Te0/6 | ● | tk1-sr1acc01-dup2 Te0/2 | ● | 3 | 10GBASE-SR(OM3) | Po3/Po2 | 9BYiFAK1cGA9hBdD1Cum-470 |
| tk1-core01 Te0/22 | ○ | tk1-mgmt01 Gi0/2 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-350 |
| tk1-core01 Te0/23 | ● | tk1-core02 Te0/23 | ● | 3 | 10GBASE-SR(OM3) | Po1 | 9BYiFAK1cGA9hBdD1Cum-186 |
| tk1-core01 Te0/24 | ● | tk1-core02 Te0/24 | ● | 3 | 10GBASE-SR(OM3) | Po1 | 9BYiFAK1cGA9hBdD1Cum-184 |
| tk1-core02 Mgmt | - | tk1-mgmt02 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-345 |
| tk1-core02 Te0/5 | ● | tk1-sr1acc02-dup2 Te0/1 | ● | 3 | 10GBASE-SR(OM3) | Po3/Po2 | 9BYiFAK1cGA9hBdD1Cum-471 |
| tk1-core02 Te0/7 | ● | tk1-fnacc01-dup2 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-768 |
| tk1-core02 Te0/22 | ○ | tk1-mgmt02 Gi0/2 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-357 |
| tk1-fnacc01 Gi0/1 | - | tk1-f6ap01 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-74 |
| tk1-fnacc01 Gi0/3-20 | - | オフィス固定端末 x5-10 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-385 |
| tk1-fnacc01 Gi0/23 | - | tk1-fnacc01-dup2 Gi0/23 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-499 |
| tk1-fnacc01 Gi0/24 | - | tk1-fnacc01-dup2 Gi0/24 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-500 |
| tk1-fnacc01 Te0/1 | ● | tk1-core01 Te0/7 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-756 |
| tk1-fnacc01-dup2 Gi0/1 | - | tk1-f6ap02 Gi0/1 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-79 |
| tk1-fnacc01-dup2 Gi0/3-20 | - | オフィス固定端末 x5-10 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-386 |
| tk1-fw01 Te0/1 | ● | 回線終端装置 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-70 |
| tk1-fw01 Te0/3 | ● | tk1-core02 Te0/1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-66 |
| tk1-mgmt01 Gi0/47 | - | tk1-mgmt02 Gi0/47 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-334 |
| tk1-mgmt01 Gi0/48 | - | tk1-mgmt02 Gi0/48 | - | 1 | 1000BASE-T(Cat6a) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-502 |
| tk1-rt01 Gi0/1 | - | 回線終端装置 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-64 |
| tk1-rt01 Gi0/3 | - | tk1-core02 Te0/2 | ○ | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-68 |
| tk1-sr1acc01 Mgmt | - | tk1-mgmt01 Gi0/3 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-338 |
| tk1-sr1acc01 Te0/1 | ● | tk1-core01 Te0/3 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po2 | 9BYiFAK1cGA9hBdD1Cum-33 |
| tk1-sr1acc01 Te0/2 | ● | tk1-core01 Te0/4 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po2 | 9BYiFAK1cGA9hBdD1Cum-36 |
| tk1-sr1acc01 Te0/3 | ● | tk1-svr101 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-767 |
| tk1-sr1acc01 Te0/4 | ● | tk1-svr102 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-763 |
| tk1-sr1acc01 Te0/10 | ● | tk1-svr108 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-766 |
| tk1-sr1acc01 Te0/23 | ● | tk1-sr1acc02 Te0/23 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-32 |
| tk1-sr1acc01 Te0/24 | ● | tk1-sr1acc02 Te0/24 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-31 |
| tk1-sr1acc01-dup2 Mgmt | - | tk1-mgmt01 Gi0/4 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-440 |
| tk1-sr1acc01-dup2 Te0/1 | ● | tk1-core01 Te0/5 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po3 | 9BYiFAK1cGA9hBdD1Cum-468 |
| tk1-sr1acc01-dup2 Te0/3 | ● | tk1-svr201 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-448 |
| tk1-sr1acc01-dup2 Te0/4 | ● | tk1-svr202 eth1 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-449 |
| tk1-sr1acc01-dup2 Te0/23 | ● | tk1-sr1acc02-dup2 Te0/23 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-396 |
| tk1-sr1acc01-dup2 Te0/24 | ● | tk1-sr1acc02-dup2 Te0/24 | ● | 3 | 10GBASE-SR(OM3) | Po1/Po1 | 9BYiFAK1cGA9hBdD1Cum-395 |
| tk1-sr1acc02 Mgmt | - | tk1-mgmt02 Gi0/3 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-313 |
| tk1-sr1acc02 Te0/1 | ● | tk1-core02 Te0/3 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po2 | 9BYiFAK1cGA9hBdD1Cum-41 |
| tk1-sr1acc02 Te0/2 | ● | tk1-core02 Te0/4 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po2 | 9BYiFAK1cGA9hBdD1Cum-43 |
| tk1-sr1acc02 Te0/3 | ● | tk1-svr101 eth2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-762 |
| tk1-sr1acc02 Te0/4 | ● | tk1-svr102 eth2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-764 |
| tk1-sr1acc02-dup2 Mgmt | - | tk1-mgmt02 Gi0/4 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-347 |
| tk1-sr1acc02-dup2 Te0/2 | ● | tk1-core02 Te0/6 | ● | 3 | 10GBASE-SR(OM3) | Po2/Po3 | 9BYiFAK1cGA9hBdD1Cum-469 |
| tk1-sr1acc02-dup2 Te0/3 | ● | tk1-svr201 eth2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-450 |
| tk1-sr1acc02-dup2 Te0/4 | ● | tk1-svr202 eth2 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-451 |
| tk1-svr101 BMC | - | tk1-mgmt01 Gi0/5 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-303 |
| tk1-svr101-dup2 eth1 | ● | os1-core01 Te0/3 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-760 |
| tk1-svr101-dup2 eth2 | ● | os1-core02 Te0/3 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-761 |
| tk1-svr102 BMC | - | tk1-mgmt01 Gi0/6 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-305 |
| tk1-svr108 BMC | - | tk1-mgmt01 Gi0/12 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-307 |
| tk1-svr108 eth2 | ● | tk1-sr1acc02 Te0/10 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-765 |
| tk1-svr201 BMC | - | tk1-mgmt02 Gi0/5 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-331 |
| tk1-svr202 BMC | - | tk1-mgmt02 Gi0/6 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-329 |
| tk1-svr208 BMC | - | tk1-mgmt02 Gi0/12 | - | 1 | 1000BASE-T(Cat6a) |  | 9BYiFAK1cGA9hBdD1Cum-327 |
| tk1-svr208 eth1 | ● | tk1-sr1acc01-dup2 Te0/10 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-453 |
| tk1-svr208 eth2 | ● | tk1-sr1acc02-dup2 Te0/10 | ● | 3 | 10GBASE-SR(OM3) |  | 9BYiFAK1cGA9hBdD1Cum-452 |

### 2.4 ポート所属表（図から作った表。V-09 の基準）

| 機器 | ポート | モード | VLAN | 根拠 |
|---|---|---|---|---|
| os1-core01 | Po1（Te0/23,Te0/24） | trunk | 9-11,300-399 | 所属線【図】 |
| os1-core01 | Te0/1 | access | 2 | 所属線【図】 |
| os1-core01 | Te0/2 | access | 2 | 所属線【図】 |
| os1-core01 | Te0/3 | trunk | 10-11 | 所属線【図】 |
| os1-core01 | Te0/4 | trunk | 10-11 | 所属線【図】 |
| os1-core01 | Te0/5 | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 所属線【図】 |
| os1-core02 | Gi0/1 | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 冗長ペアの対称性【推測：対称性】 |
| os1-core02 | Po1（Te0/23,Te0/24） | trunk | 9-11,300-399 | 冗長ペアの対称性【推測：対称性】 |
| os1-core02 | Te0/1 | access | 2 | 冗長ペアの対称性【推測：対称性】 |
| os1-core02 | Te0/2 | access | 2 | 冗長ペアの対称性【推測：対称性】 |
| os1-core02 | Te0/3 | trunk | 10-11 | 冗長ペアの対称性【推測：対称性】 |
| os1-core02 | Te0/4 | trunk | 10-11 | 冗長ペアの対称性【推測：対称性】 |
| os1-fmacc01 | Gi0/1 | access | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 所属線【図】 |
| os1-fmacc01 | Gi0/3-20 | access | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 所属線【図】 |
| os1-fmacc01 | Gi0/21 | access | 9 | 所属線【図】 |
| os1-fmacc01 | Po1（Gi0/23,Gi0/24） | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 所属線【図】 |
| os1-fmacc01 | Te0/1 | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 所属線【図】 |
| os1-fmacc02 | Gi0/1 | access | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 冗長ペアの対称性【推測：対称性】 |
| os1-fmacc02 | Gi0/3-20 | access | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 冗長ペアの対称性【推測：対称性】 |
| os1-fmacc02 | Gi0/21 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| os1-fmacc02 | Po1（Gi0/23,Gi0/24） | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 冗長ペアの対称性【推測：対称性】 |
| os1-fmacc02 | Te0/1 | trunk | 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 冗長ペアの対称性【推測：対称性】 |
| os1-fw01 | Te0/1 | L3 | OS-INET | 所属線【図】 |
| os1-fw01 | Te0/2 | access | 2 | 所属線【図】 |
| os1-fw01 | Te0/3 | access | 2 | 所属線【図】 |
| os1-rt01 | Gi0/1 | L3 | INTER-BLDG | 所属線【図】 |
| os1-rt01 | Gi0/2 | access | 2 | 所属線【図】 |
| os1-rt01 | Gi0/3 | access | 2 | 所属線【図】 |
| tk1-core01 | Mgmt | L3（vrf mgmt） | MGMT | Mgmt ポート（R12）【推測】 |
| tk1-core01 | Po1（Te0/23,Te0/24） | trunk | 2,10-11,100-399 | 所属線【図】 |
| tk1-core01 | Po2（Te0/3,Te0/4） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-core01 | Po3（Te0/5,Te0/6） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-core01 | Te0/1 | access | 2 | 所属線【図】 |
| tk1-core01 | Te0/2 | access | 2 | 所属線【図】 |
| tk1-core01 | Te0/7 | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 所属線【図】 |
| tk1-core01 | Te0/22 | access | 9 | 所属線【図】 |
| tk1-core02 | Mgmt | L3（vrf mgmt） | MGMT | Mgmt ポート（R12）【推測】 |
| tk1-core02 | Po2（Te0/3,Te0/4） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Po3（Te0/5,Te0/6） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/1 | access | 2 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/2 | access | 2 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/7 | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/22 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/23 | trunk | 2,10-11,100-399 | 冗長ペアの対称性【推測：対称性】 |
| tk1-core02 | Te0/24 | trunk | 2,10-11,100-399 | 冗長ペアの対称性【推測：対称性】 |
| tk1-fnacc01 | Gi0/1 | access | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 所属線【図】 |
| tk1-fnacc01 | Gi0/3-20 | access | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 所属線【図】 |
| tk1-fnacc01 | Po1（Gi0/23,Gi0/24） | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 所属線【図】 |
| tk1-fnacc01 | Te0/1 | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 所属線【図】 |
| tk1-fnacc01-dup2 | Gi0/1 | access | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 冗長ペアの対称性【推測：対称性】 |
| tk1-fnacc01-dup2 | Gi0/3-20 | access | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 冗長ペアの対称性【推測：対称性】 |
| tk1-fnacc01-dup2 | Po1（Gi0/23,Gi0/24） | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 冗長ペアの対称性【推測：対称性】 |
| tk1-fnacc01-dup2 | Te0/1 | trunk | 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 冗長ペアの対称性【推測：対称性】 |
| tk1-fw01 | Te0/1 | L3 | TK-INET | 所属線【図】 |
| tk1-fw01 | Te0/2 | access | 2 | 所属線【図】 |
| tk1-fw01 | Te0/3 | access | 2 | 所属線【図】 |
| tk1-mgmt01 | Gi0/1 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/2 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/3 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/4 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/5 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/6 | access | 9 | 所属線【図】 |
| tk1-mgmt01 | Gi0/12 | access | 9 | ラベルへの線【図】(D-04) |
| tk1-mgmt01 | Po1（Gi0/47,Gi0/48） | access | 9 | 所属線【図】 |
| tk1-mgmt02 | Gi0/1 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/2 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/3 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/4 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/5 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/6 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Gi0/12 | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-mgmt02 | Po1（Gi0/47,Gi0/48） | access | 9 | 冗長ペアの対称性【推測：対称性】 |
| tk1-rt01 | Gi0/1 | L3 | INTER-BLDG | 所属線【図】 |
| tk1-rt01 | Gi0/2 | access | 2 | 所属線【図】 |
| tk1-rt01 | Gi0/3 | access | 2 | 所属線【図】 |
| tk1-sr1acc01 | Mgmt | L3（vrf mgmt） | MGMT | 所属線【図】 |
| tk1-sr1acc01 | Po1（Te0/23,Te0/24） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-sr1acc01 | Po2（Te0/1,Te0/2） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-sr1acc01 | Te0/3 | trunk | 10-11 | 所属線【図】 |
| tk1-sr1acc01 | Te0/4 | access | <TBD:APx_PROD_VLAN> | 所属線【図】 |
| tk1-sr1acc01 | Te0/10 | access | <TBD:APx_DEV_VLAN> | 所属線【図】 |
| tk1-sr1acc01-dup2 | Mgmt | L3（vrf mgmt） | MGMT | 所属線【図】 |
| tk1-sr1acc01-dup2 | Po1（Te0/23,Te0/24） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-sr1acc01-dup2 | Po2（Te0/1,Te0/2） | trunk | 10-11,100-299 | 所属線【図】 |
| tk1-sr1acc01-dup2 | Te0/3 | trunk | 10-11 | 所属線【図】 |
| tk1-sr1acc01-dup2 | Te0/4 | access | <TBD:APx_PROD_VLAN> | 所属線【図】 |
| tk1-sr1acc01-dup2 | Te0/10 | access | <TBD:APx_DEV_VLAN> | 所属線【図】 |
| tk1-sr1acc02 | Mgmt | L3（vrf mgmt） | MGMT | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02 | Po1（Te0/23,Te0/24） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02 | Po2（Te0/1,Te0/2） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02 | Te0/3 | trunk | 10-11 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02 | Te0/4 | access | <TBD:APx_PROD_VLAN> | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02 | Te0/10 | access | <TBD:APx_DEV_VLAN> | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Mgmt | L3（vrf mgmt） | MGMT | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Po1（Te0/23,Te0/24） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Po2（Te0/1,Te0/2） | trunk | 10-11,100-299 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Te0/3 | trunk | 10-11 | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Te0/4 | access | <TBD:APx_PROD_VLAN> | 冗長ペアの対称性【推測：対称性】 |
| tk1-sr1acc02-dup2 | Te0/10 | access | <TBD:APx_DEV_VLAN> | 冗長ペアの対称性【推測：対称性】 |

## 3. 機器別コンフィグ

### 3.1 os1-core01（C社 L3switch 9000-24、L3SW）

ファイル: `configs/os1-core01.cfg`

```
! ==== os1-core01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-core01
!
ip routing
!
fhrp version vrrp v3
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
spanning-tree vlan 2,9,300-399 root primary ! 【推測】冗長ペアの01号機をルート
!
vlan 2
 name EXT
vlan 9
 name MGMT
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan2
 description EXT 172.18.0.0/27
 ip address 172.18.0.4 255.255.255.224
 vrrp 2 address-family ipv4
  address 172.18.0.6 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan9
 description MGMT 172.18.1.0/24
 ip address 172.18.1.1 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
 vrrp 9 address-family ipv4
  address 172.18.1.3 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan10
 description DMZ 172.18.2.0/24
 ip address 172.18.2.1 255.255.255.0
 vrrp 10 address-family ipv4
  address 172.18.2.3 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan11
 description COMMON 172.18.3.0/24
 ip address 172.18.3.1 255.255.255.0
 vrrp 11 address-family ipv4
  address 172.18.3.3 primary
  priority 110
  preempt
 exit-vrrp
!
! --- OFFICE_Fn: VLAN300-399 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:OFFICE_Fn_VLAN_ID>
 description OFFICE_Fn 172.18.64.0/18
 ip address <TBD:OFFICE_Fn_IP_os1-core01> <TBD:OFFICE_Fn_MASK>
 vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4
  address <TBD:OFFICE_Fn_VIP> primary
  priority 110
  preempt
 exit-vrrp
!
interface Port-channel1
 description to os1-core02 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
!
interface TenGigabitEthernet0/1
 description to os1-fw01 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/2
 description to os1-rt01 Gi0/2 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/3
 description to tk1-svr101-dup2 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr101-dup3 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/5
 description to os1-fmacc01 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface TenGigabitEthernet0/23
 description to os1-core02 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to os1-core02 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
 channel-group 1 mode active
!
ip route 0.0.0.0 0.0.0.0 172.18.0.1 ! 【論】 default
ip route 172.17.0.0 255.255.0.0 172.18.0.2 ! 【論】 to東京（tk1 拠点ブロック【推測】）
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-core01 | Host 欄「os1-core01 / C社 L3switch 9000-24」（cell 9BYiFAK1cGA9hBdD1Cum-162） | 【図】 | R-014, R-025, R-032, R-033 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | 未接続線を推定して GRT と EXT の接続とした。アドレス 172.18.0.0/27【図】。バッジ .4。vip .6（VRRP） | 【図】【推測】 | R-014, R-025, R-032, R-033 |
| 4 | interface Vlan9 | ルーティング箱（GRT）と MGMT の横線が線でつながる。アドレス 172.18.1.0/24【論】。バッジ .1。vip .3（VRRP） | 【図】【論】 | R-014, R-025, R-032, R-033 |
| 5 | interface Vlan10 | ルーティング箱（GRT）と DMZ の横線が線でつながる。アドレス 172.18.2.0/24【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-014, R-025, R-032, R-033 |
| 6 | interface Vlan11 | ルーティング箱（GRT）と COMMON の横線が線でつながる。アドレス 172.18.3.0/24【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-014, R-025, R-032, R-033 |
| 7 | interface Vlan<TBD> | ルーティング箱（GRT）と OFFICE_Fn の横線が線でつながる。アドレス 172.18.64.0/18【図】。バッジ .x（値が未確定なので <TBD>）。vip .3（VRRP） | 【図】 | R-014, R-025, R-032, R-033 |
| 8 | Po1 trunk 9-11,300-399 | Po1 が DMZ・COMMON・OFFICE_Fn・MGMT の横線に所属（所属線【図】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 os1-core02 Te0/23, os1-core02 Te0/24 | 【図】 |  |
| 9 | Te0/1 access 2 | Te0/1 が EXT の横線に所属（所属線【図】）。対向 os1-fw01 Te0/2 | 【図】 |  |
| 10 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（所属線【図】）。対向 os1-rt01 Gi0/2 | 【図】 |  |
| 11 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（所属線【図】）。対向 tk1-svr101-dup2 eth1 | 【図】 |  |
| 12 | Te0/4 trunk 10-11 | Te0/4 が DMZ・COMMON の横線に所属（所属線【図】）。対向 tk1-svr101-dup3 eth1 | 【図】 |  |
| 13 | Te0/5 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Te0/5 が OFFICE_Fn・MGMT の横線に所属（所属線【図】）。対向 os1-fmacc01 Te0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 14 | route 172.17.0.0/16 → 172.18.0.2 | 論理構成図の矢印「to東京」→ os1-rt01。next-hop は os1-rt01 の .2 | 【論】 |  |
| 15 | route 0.0.0.0/0 → 172.18.0.1 | 論理構成図の矢印「default」→ os1-fw01。next-hop は os1-fw01 の .1 | 【論】 |  |

### 3.2 os1-core02（C社 L3switch 9000-24、L3SW）

ファイル: `configs/os1-core02.cfg`

```
! ==== os1-core02 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-core02
!
ip routing
!
fhrp version vrrp v3
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
spanning-tree vlan 2,9,300-399 root secondary ! 【推測】冗長ペアの02号機をセカンダリ
!
vlan 2
 name EXT
vlan 9
 name MGMT
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan2
 description EXT 172.18.0.0/27
 ip address 172.18.0.5 255.255.255.224
 vrrp 2 address-family ipv4
  address 172.18.0.6 primary
  preempt
 exit-vrrp
!
interface Vlan9
 description MGMT 172.18.1.0/24
 ip address 172.18.1.2 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
 vrrp 9 address-family ipv4
  address 172.18.1.3 primary
  preempt
 exit-vrrp
!
interface Vlan10
 description DMZ 172.18.2.0/24
 ip address 172.18.2.2 255.255.255.0
 vrrp 10 address-family ipv4
  address 172.18.2.3 primary
  preempt
 exit-vrrp
!
interface Vlan11
 description COMMON 172.18.3.0/24
 ip address 172.18.3.2 255.255.255.0
 vrrp 11 address-family ipv4
  address 172.18.3.3 primary
  preempt
 exit-vrrp
!
! --- OFFICE_Fn: VLAN300-399 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:OFFICE_Fn_VLAN_ID>
 description OFFICE_Fn 172.18.64.0/18
 ip address <TBD:OFFICE_Fn_IP_os1-core02> <TBD:OFFICE_Fn_MASK>
 vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4
  address <TBD:OFFICE_Fn_VIP> primary
  preempt
 exit-vrrp
!
interface Port-channel1
 description to os1-core01 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
!
interface GigabitEthernet0/1
 description to os1-fmacc02 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> ! WARN R-029
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 ! 図のポート名のまま（冗長ペアの対称位置は Te0/5。誤記の可能性）
!
interface TenGigabitEthernet0/1
 description to os1-fw01 Te0/3 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/2
 description to os1-rt01 Gi0/3 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/3
 description to tk1-svr101-dup2 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr101-dup3 eth2 [SFP+/LC 10GBASE-SR(OM3)] (推定接続)
 switchport mode trunk
 switchport trunk allowed vlan 10-11 ! WARN R-026
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/23
 description to os1-core01 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to os1-core01 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9-11,300-399
 channel-group 1 mode active
!
ip route 0.0.0.0 0.0.0.0 172.18.0.1 ! 【論】 default
ip route 172.17.0.0 255.255.0.0 172.18.0.2 ! 【論】 to東京（tk1 拠点ブロック【推測】）
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-core02 | Host 欄「os1-core02 / C社 L3switch 9000-24」（cell 9BYiFAK1cGA9hBdD1Cum-142） | 【図】 | R-032, R-033 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | EXT の色の IP バッジがある。アドレス 172.18.0.0/27【図】。バッジ .5。vip .6（VRRP） | 【図】 | R-032, R-033 |
| 4 | interface Vlan9 | 冗長ペアの os1-core01 と同じ構成（os1-core02 の箱では線が省略）。アドレス 172.18.1.0/24【論】。バッジ .2。vip .3（VRRP） | 【図】【論】【推測】 | R-032, R-033 |
| 5 | interface Vlan10 | 冗長ペアの os1-core01 と同じ構成（os1-core02 の箱では線が省略）。アドレス 172.18.2.0/24【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-032, R-033 |
| 6 | interface Vlan11 | 冗長ペアの os1-core01 と同じ構成（os1-core02 の箱では線が省略）。アドレス 172.18.3.0/24【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-032, R-033 |
| 7 | interface Vlan<TBD> | 冗長ペアの os1-core01 と同じ構成（os1-core02 の箱では線が省略）。アドレス 172.18.64.0/18【図】。バッジ .x+1（値が未確定なので <TBD>）。vip .3（VRRP） | 【図】【推測】 | R-032, R-033 |
| 8 | Gi0/1 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Gi0/1 が OFFICE_Fn・MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 os1-fmacc02 Te0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 | R-029 |
| 9 | Po1 trunk 9-11,300-399 | Po1 が DMZ・COMMON・OFFICE_Fn・MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 os1-core01 Te0/23, os1-core01 Te0/24 | 【図】【推測：対称性】 |  |
| 10 | Te0/1 access 2 | Te0/1 が EXT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 os1-fw01 Te0/3 | 【図】【推測：対称性】 |  |
| 11 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 os1-rt01 Gi0/3 | 【図】【推測：対称性】 |  |
| 12 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr101-dup2 eth2 | 【図】【推測：対称性】 |  |
| 13 | Te0/4 trunk 10-11 | Te0/4 が DMZ・COMMON の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr101-dup3 eth2 | 【図】【推測：対称性】 | R-026 |
| 14 | route 172.17.0.0/16 → 172.18.0.2 | 論理構成図の矢印「to東京」→ os1-rt01。next-hop は os1-rt01 の .2 | 【論】 |  |
| 15 | route 0.0.0.0/0 → 172.18.0.1 | 論理構成図の矢印「default」→ os1-fw01。next-hop は os1-fw01 の .1 | 【論】 |  |

### 3.3 os1-fmacc01（C社 L2switch 1000-24、L2SW）

ファイル: `configs/os1-fmacc01.cfg`

```
! ==== os1-fmacc01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-fmacc01
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan9
 description MGMT 172.18.1.0/24
 ip address <TBD:MGMT_IP_os1-fmacc01> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to os1-fmacc02 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface GigabitEthernet0/1
 description to os1-fmap01 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
 power inline auto ! 【図】PoE（AP 接続）
!
interface GigabitEthernet0/2
 description PoE予備
 shutdown ! 図に「PoE予備」と明示（R14）
!
interface range GigabitEthernet0/3 - 20
 description to オフィス固定端末 x5-10 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
!
interface GigabitEthernet0/21
 description to tk1-svr101-dup2 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/23
 description to os1-fmacc02 Gi0/23 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface GigabitEthernet0/24
 description to os1-fmacc02 Gi0/24 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface TenGigabitEthernet0/1
 description to os1-core01 Te0/5 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
ip default-gateway 172.18.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-fmacc01 | Host 欄「os1-fmacc01 / C社 L2switch 1000-24」（cell 9BYiFAK1cGA9hBdD1Cum-521） | 【図】 | R-033 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.18.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-033 |
| 4 | Gi0/1 access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Gi0/1 が OFFICE_Fn の横線に所属（所属線【図】）。対向 os1-fmap01 Gi0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 5 | Gi0/2 shutdown | 図に「PoE予備」と明示（R14） | 【図】 |  |
| 6 | Gi0/3-20 access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Gi0/3-20 が OFFICE_Fn の横線に所属（所属線【図】）。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 7 | Gi0/21 access 9 | Gi0/21 が MGMT の横線に所属（所属線【図】）。対向 tk1-svr101-dup2 BMC | 【図】 |  |
| 8 | Po1 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Po1 が MGMT・OFFICE_Fn の横線に所属（所属線【図】）。Po 箱が Gi0/23・Gi0/24 にまたがる（R5）。対向 os1-fmacc02 Gi0/23, os1-fmacc02 Gi0/24。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 9 | Te0/1 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Te0/1 が MGMT・OFFICE_Fn の横線に所属（所属線【図】）。対向 os1-core01 Te0/5。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 10 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.4 os1-fmacc02（C社 L2switch 1000-24、L2SW）

ファイル: `configs/os1-fmacc02.cfg`

```
! ==== os1-fmacc02 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-fmacc02
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan9
 description MGMT 172.18.1.0/24
 ip address <TBD:MGMT_IP_os1-fmacc02> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to os1-fmacc01 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface GigabitEthernet0/1
 description to os1-fmap02 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
 power inline auto ! 【図】PoE（AP 接続）
!
interface GigabitEthernet0/2
 description PoE予備
 shutdown ! 図に「PoE予備」と明示（R14）
!
interface range GigabitEthernet0/3 - 20
 description to オフィス固定端末 x5-10 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
!
interface GigabitEthernet0/21
 description to tk1-svr101-dup3 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/23
 description to os1-fmacc01 Gi0/23 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface GigabitEthernet0/24
 description to os1-fmacc01 Gi0/24 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface TenGigabitEthernet0/1
 description to os1-core02 Gi0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
ip default-gateway 172.18.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-fmacc02 | Host 欄「os1-fmacc02 / C社 L2switch 1000-24」（cell 9BYiFAK1cGA9hBdD1Cum-581） | 【図】 | R-033 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.18.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-033 |
| 4 | Gi0/1 access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Gi0/1 が OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 os1-fmap02 Gi0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 5 | Gi0/2 shutdown | 図に「PoE予備」と明示（R14） | 【図】 |  |
| 6 | Gi0/3-20 access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Gi0/3-20 が OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 7 | Gi0/21 access 9 | Gi0/21 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr101-dup3 BMC | 【図】【推測：対称性】 |  |
| 8 | Po1 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Po1 が MGMT・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Gi0/23・Gi0/24 にまたがる（R5）。対向 os1-fmacc01 Gi0/23, os1-fmacc01 Gi0/24。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 9 | Te0/1 trunk 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | Te0/1 が MGMT・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 os1-core02 Gi0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 10 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.5 os1-fw01（C社 Firewall 3000、FW）

ファイル: `configs/os1-fw01.cfg`

```
! ==== os1-fw01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco ASA（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-fw01
!
interface TenGigabitEthernet0/1
 description to 回線終端装置 [SFP+/LC 10GBASE-SR(OM3)]
 nameif outside
 security-level 0
 ip address <TBD:OS-INET_IP_os1-fw01> 255.255.255.128
!
interface TenGigabitEthernet0/2
 description to os1-core01 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 bridge-group 2
 nameif to-os1-core01
 security-level 100
!
interface TenGigabitEthernet0/3
 description to os1-core02 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 bridge-group 2
 nameif to-os1-core02
 security-level 100
!
interface BVI2
 description EXT（Te0/2+Te0/3）
 ip address 172.18.0.1 255.255.255.224 ! 【推測】同一セグメントの2ポートを BVI で表現（R10）
!
same-security-traffic permit inter-interface
!
route outside 0.0.0.0 0.0.0.0 <TBD:Internet_GW> ! 【論】 default
route to-os1-core01 172.18.0.0 255.255.0.0 172.18.0.6 ! 【論】 to大阪（os1 拠点ブロック【推測】）
!
! --- NAT・ポリシーの雛形（【一般】6.2） ---
object network OBJ-OS1-INTERNAL
 subnet 172.18.0.0 255.255.0.0
 nat (any,outside) dynamic interface
access-list OUTSIDE-IN extended <TBD:FW_POLICY>
access-group OUTSIDE-IN in interface outside
!
!
ntp server <TBD:NTP_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-fw01 | Host 欄「os1-fw01 / C社 Firewall 3000」（cell 9BYiFAK1cGA9hBdD1Cum-143） | 【図】 | R-032 |
| 2 | 記法（asa） | 図の Vendor Model「C社 Firewall 3000」は実在のベンダー名・型番として読めない。ファイアウォールとして ASA 記法を採用（同一セグメントの2ポートを BVI で表現できる）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface BVI（Te0/2+Te0/3） | ルーティング箱（GRT）と EXT の横線が線でつながる。アドレス 172.18.0.0/27【図】。バッジ .1。同じ横線に2ポート（Te0/2・Te0/3）がつながるので BVI（R10、4.2） | 【図】【推測】 | R-032 |
| 4 | interface Te0/1（L3） | ルーティング箱（GRT）と OS-INET の横線が線でつながる。アドレス 203.0.113.0/25【図】。バッジ .x（値が未確定なので <TBD>） | 【図】 | R-032 |
| 5 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（所属線【図】）。対向 os1-core01 Te0/1 | 【図】 |  |
| 6 | Te0/3 access 2 | Te0/3 が EXT の横線に所属（所属線【図】）。対向 os1-core02 Te0/1 | 【図】 |  |
| 7 | route 0.0.0.0/0 → <TBD:Internet_GW> | 論理構成図の矢印「default」→ Internet。相手側の IP は図に無い | 【論】 |  |
| 8 | route 172.18.0.0/16 → 172.18.0.6 | 論理構成図の矢印「to大阪」→ os1-core01/02。next-hop は VIP .6 | 【論】 |  |

### 3.6 os1-rt01（C社 Router 1000、ルーター）

ファイル: `configs/os1-rt01.cfg`

```
! ==== os1-rt01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE (ISR)（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname os1-rt01
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 2
 name EXT
!
interface Vlan2
 description EXT 172.18.0.0/27
 ip address 172.18.0.2 255.255.255.224
!
interface GigabitEthernet0/1
 description to 回線終端装置 [RJ45 1000BASE-T(Cat6a)]
 ip address <TBD:INTER-BLDG_IP_os1-rt01> 255.255.255.0
!
interface GigabitEthernet0/2
 description to os1-core01 Te0/2 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface GigabitEthernet0/3
 description to os1-core02 Te0/2 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
ip route 172.17.0.0 255.255.0.0 <TBD:INTER-BLDG_IP_tk1-rt01> ! 【論】 to東京（tk1 拠点ブロック【推測】）
ip route 172.18.0.0 255.255.0.0 172.18.0.6 ! 【論】 to大阪（os1 拠点ブロック【推測】）
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname os1-rt01 | Host 欄「os1-rt01 / C社 Router 1000」（cell 9BYiFAK1cGA9hBdD1Cum-144） | 【図】 | R-032 |
| 2 | 記法（isr） | 図の Vendor Model「C社 Router 1000」は実在のベンダー名・型番として読めない。ルーターとして静的経路・スイッチポート＋SVI を書ける ISR（IOS-XE）を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | ルーティング箱（GRT）と EXT の横線が線でつながる。アドレス 172.18.0.0/27【図】。バッジ .2。同じ横線に2ポートがつながるのでスイッチポート＋SVI（R10、4.2） | 【図】 | R-032 |
| 4 | interface Gi0/1（L3） | ルーティング箱（GRT）と INTER-BLDG の横線が線でつながる。アドレス 172.16.0.0/24【図】。バッジ .x（値が未確定なので <TBD>） | 【図】 | R-032 |
| 5 | Gi0/2 access 2 | Gi0/2 が EXT の横線に所属（所属線【図】）。対向 os1-core01 Te0/2 | 【図】 |  |
| 6 | Gi0/3 access 2 | Gi0/3 が EXT の横線に所属（所属線【図】）。対向 os1-core02 Te0/2 | 【図】 |  |
| 7 | route 172.17.0.0/16 → <TBD:INTER-BLDG_IP_tk1-rt01> | 論理構成図の矢印「d to東京」→ tk1-rt01。next-hop は tk1-rt01 の .x | 【論】 |  |
| 8 | route 172.18.0.0/16 → 172.18.0.6 | 論理構成図の矢印「to大阪」→ os1-core01/02。next-hop は VIP .6 | 【論】 |  |

### 3.7 tk1-core01（C社 L3switch 9000-24、L3SW）

ファイル: `configs/tk1-core01.cfg`

```
! ==== tk1-core01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-core01
!
ip routing
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
fhrp version vrrp v3
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
spanning-tree vlan 2,9-11,100-399 root primary ! 【推測】冗長ペアの01号機をルート
!
vlan 2
 name EXT
vlan 9
 name MGMT
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan2
 description EXT 172.17.0.0/27
 ip address 172.17.0.4 255.255.255.224
 vrrp 2 address-family ipv4
  address 172.17.0.6 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address 172.17.1.1 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
 vrrp 9 address-family ipv4
  address 172.17.1.3 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan10
 description DMZ 172.17.2.0/24
 ip address 172.17.2.1 255.255.255.0
 vrrp 10 address-family ipv4
  address 172.17.2.3 primary
  priority 110
  preempt
 exit-vrrp
!
interface Vlan11
 description COMMON 172.17.3.0/24
 ip address 172.17.3.1 255.255.255.0
 vrrp 11 address-family ipv4
  address 172.17.3.3 primary
  priority 110
  preempt
 exit-vrrp
!
! --- APx_PROD: VLAN100-199 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:APx_PROD_VLAN_ID>
 description APx_PROD 172.17.128.0/18
 ip address <TBD:APx_PROD_IP_tk1-core01> <TBD:APx_PROD_MASK>
 vrrp <TBD:APx_PROD_VRRP_GROUP> address-family ipv4
  address <TBD:APx_PROD_VIP> primary
  priority 110
  preempt
 exit-vrrp
!
! --- APx_DEV: VLAN200-299 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:APx_DEV_VLAN_ID>
 description APx_DEV 172.17.192.0/18
 ip address <TBD:APx_DEV_IP_tk1-core01> <TBD:APx_DEV_MASK>
 vrrp <TBD:APx_DEV_VRRP_GROUP> address-family ipv4
  address <TBD:APx_DEV_VIP> primary
  priority 110
  preempt
 exit-vrrp
!
! --- OFFICE_Fn: VLAN300-399 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:OFFICE_Fn_VLAN_ID>
 description OFFICE_Fn 172.17.64.0/18
 ip address <TBD:OFFICE_Fn_IP_tk1-core01> <TBD:OFFICE_Fn_MASK>
 vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4
  address <TBD:OFFICE_Fn_VIP> primary
  priority 110
  preempt
 exit-vrrp
!
interface Port-channel1
 description to tk1-core02 Te0/23 ほか
 switchport mode trunk
 switchport trunk allowed vlan 2,10-11,100-399 ! WARN R-008 R-030
!
interface Port-channel2
 description to tk1-sr1acc01 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299 ! WARN R-009
!
interface Port-channel3
 description to tk1-sr1acc01-dup2 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299 ! WARN R-010
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt01 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-core01> 255.255.255.0 ! 【推測】R12
!
interface TenGigabitEthernet0/1
 description to tk1-fw01 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/2
 description to tk1-rt01 Gi0/2 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/3
 description to tk1-sr1acc01 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/4
 description to tk1-sr1acc01 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/5
 description to tk1-sr1acc01-dup2 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 3 mode active
!
interface TenGigabitEthernet0/6
 description to tk1-sr1acc01-dup2 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 3 mode active
!
interface TenGigabitEthernet0/7
 description to tk1-fnacc01 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> ! WARN R-011
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface TenGigabitEthernet0/22
 description to tk1-mgmt01 Gi0/2 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface TenGigabitEthernet0/23
 description to tk1-core02 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 2,10-11,100-399
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to tk1-core02 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 2,10-11,100-399
 channel-group 1 mode active
!
ip route 0.0.0.0 0.0.0.0 172.17.0.1 ! 【論】 default
ip route 172.18.0.0 255.255.0.0 172.17.0.2 ! 【論】 to大阪（os1 拠点ブロック【推測】）
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-core01 | Host 欄「tk1-core01 / C社 L3switch 9000-24」（cell 9BYiFAK1cGA9hBdD1Cum-148） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | ルーティング箱（GRT）と EXT の横線が線でつながる。アドレス 172.17.0.0/27【図】。バッジ .4。vip .6（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 4 | interface Vlan9 | ルーティング箱（GRT）と MGMT の横線が線でつながる。アドレス 172.17.1.0/24【論】。バッジ .1。vip .3（VRRP） | 【図】【論】 | R-034, R-035, R-036, R-037, R-045 |
| 5 | interface Vlan10 | ルーティング箱（GRT）と DMZ の横線が線でつながる。アドレス 172.17.2.0/24【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 6 | interface Vlan11 | ルーティング箱（GRT）と COMMON の横線が線でつながる。アドレス 172.17.3.0/24【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 7 | interface Vlan<TBD> | ルーティング箱（GRT）と APx_PROD の横線が線でつながる。アドレス 172.17.128.0/18【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 8 | interface Vlan<TBD> | ルーティング箱（GRT）と APx_DEV の横線が線でつながる。アドレス 172.17.192.0/18【図】。バッジ .1。vip .3（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 9 | interface Vlan<TBD> | ルーティング箱（GRT）と OFFICE_Fn の横線が線でつながる。アドレス 172.17.64.0/18【図】。バッジ .x（値が未確定なので <TBD>）。vip .3（VRRP） | 【図】 | R-034, R-035, R-036, R-037, R-045 |
| 10 | Po1 trunk 2,10-11,100-399 | Po1 が EXT・DMZ・COMMON・APx_PROD・APx_DEV・OFFICE_Fn の横線に所属（所属線【図】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 tk1-core02 Te0/23, tk1-core02 Te0/24 | 【図】 | R-008, R-030 |
| 11 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/3・Te0/4 にまたがる（R5）。対向 tk1-sr1acc01 Te0/1, tk1-sr1acc01 Te0/2 | 【図】 | R-009 |
| 12 | Po3 trunk 10-11,100-299 | Po3 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/5・Te0/6 にまたがる（R5）。対向 tk1-sr1acc01-dup2 Te0/1, tk1-sr1acc01-dup2 Te0/2 | 【図】 | R-010 |
| 13 | Te0/1 access 2 | Te0/1 が EXT の横線に所属（所属線【図】）。対向 tk1-fw01 Te0/2 | 【図】 |  |
| 14 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（所属線【図】）。対向 tk1-rt01 Gi0/2 | 【図】 |  |
| 15 | Te0/7 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Te0/7 が OFFICE_Fn・MGMT の横線に所属（所属線【図】）。対向 tk1-fnacc01 Te0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 | R-011 |
| 16 | Te0/22 access 9 | Te0/22 が MGMT の横線に所属（所属線【図】）。対向 tk1-mgmt01 Gi0/2 | 【図】 |  |
| 17 | 管理（r12） | Mgmt ポートが管理SWにつながるが vrf 箱もバッジも無い → 管理 VRF に入れる（R12） | 【推測】 |  |
| 18 | route 172.18.0.0/16 → 172.17.0.2 | 論理構成図の矢印「to 大阪」→ tk1-rt01。next-hop は tk1-rt01 の 2 | 【論】 |  |
| 19 | route 0.0.0.0/0 → 172.17.0.1 | 論理構成図の矢印「default」→ tk1-fw01。next-hop は tk1-fw01 の .1 | 【論】 |  |
| 20 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

### 3.8 tk1-core02（C社 L3switch 9000-24、L3SW）

ファイル: `configs/tk1-core02.cfg`

```
! ==== tk1-core02 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-core02
!
ip routing
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
fhrp version vrrp v3
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
spanning-tree vlan 2,9-11,100-399 root secondary ! 【推測】冗長ペアの02号機をセカンダリ
!
vlan 2
 name EXT
vlan 9
 name MGMT
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan2
 description EXT 172.17.0.0/27
 ip address 172.17.0.5 255.255.255.224
 vrrp 2 address-family ipv4
  address 172.17.0.6 primary
  preempt
 exit-vrrp
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address 172.17.1.2 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
 vrrp 9 address-family ipv4
  address 172.17.1.3 primary
  preempt
 exit-vrrp
!
interface Vlan10
 description DMZ 172.17.2.0/24
 ip address 172.17.2.2 255.255.255.0
 vrrp 10 address-family ipv4
  address 172.17.2.3 primary
  preempt
 exit-vrrp
!
interface Vlan11
 description COMMON 172.17.3.0/24
 ip address 172.17.3.2 255.255.255.0
 vrrp 11 address-family ipv4
  address 172.17.3.3 primary
  preempt
 exit-vrrp
!
! --- APx_PROD: VLAN100-199 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:APx_PROD_VLAN_ID>
 description APx_PROD 172.17.128.0/18
 ip address <TBD:APx_PROD_IP_tk1-core02> <TBD:APx_PROD_MASK>
 vrrp <TBD:APx_PROD_VRRP_GROUP> address-family ipv4
  address <TBD:APx_PROD_VIP> primary
  preempt
 exit-vrrp
!
! --- APx_DEV: VLAN200-299 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:APx_DEV_VLAN_ID>
 description APx_DEV 172.17.192.0/18
 ip address <TBD:APx_DEV_IP_tk1-core02> <TBD:APx_DEV_MASK>
 vrrp <TBD:APx_DEV_VRRP_GROUP> address-family ipv4
  address <TBD:APx_DEV_VIP> primary
  preempt
 exit-vrrp
!
! --- OFFICE_Fn: VLAN300-399 の各 VLAN に同じ形の SVI を作る（テンプレート、5.4） ---
interface Vlan<TBD:OFFICE_Fn_VLAN_ID>
 description OFFICE_Fn 172.17.64.0/18
 ip address <TBD:OFFICE_Fn_IP_tk1-core02> <TBD:OFFICE_Fn_MASK>
 vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4
  address <TBD:OFFICE_Fn_VIP> primary
  preempt
 exit-vrrp
!
interface Port-channel2
 description to tk1-sr1acc02 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface Port-channel3
 description to tk1-sr1acc02-dup2 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt02 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-core02> 255.255.255.0 ! 【推測】R12
!
interface TenGigabitEthernet0/1
 description to tk1-fw01 Te0/3 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/2
 description to tk1-rt01 Gi0/3 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface TenGigabitEthernet0/3
 description to tk1-sr1acc02 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/4
 description to tk1-sr1acc02 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/5
 description to tk1-sr1acc02-dup2 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 3 mode active
!
interface TenGigabitEthernet0/6
 description to tk1-sr1acc02-dup2 Te0/2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 3 mode active
!
interface TenGigabitEthernet0/7
 description to tk1-fnacc01-dup2 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface TenGigabitEthernet0/22
 description to tk1-mgmt02 Gi0/2 [SFP+/RJ45 (10GB-T) 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface TenGigabitEthernet0/23
 description to tk1-core01 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 2,10-11,100-399
!
interface TenGigabitEthernet0/24
 description to tk1-core01 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 2,10-11,100-399
!
ip route 0.0.0.0 0.0.0.0 172.17.0.1 ! 【論】 default
ip route 172.18.0.0 255.255.0.0 172.17.0.2 ! 【論】 to大阪（os1 拠点ブロック【推測】）
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-core02 | Host 欄「tk1-core02 / C社 L3switch 9000-24」（cell 9BYiFAK1cGA9hBdD1Cum-147） | 【図】 | R-034, R-035, R-036, R-037 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L3switch 9000-24」は実在のベンダー名・型番として読めない。L3スイッチ（ルーティング箱＋横線）として SVI・VRRP・Port-channel・VRF を標準的に書ける Catalyst 9000 系 IOS-XE を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.0.0/27【図】。バッジ .5。vip .6（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 4 | interface Vlan9 | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.1.0/24【論】。バッジ .2。vip .3（VRRP） | 【図】【論】【推測】 | R-034, R-035, R-036, R-037 |
| 5 | interface Vlan10 | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.2.0/24【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 6 | interface Vlan11 | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.3.0/24【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 7 | interface Vlan<TBD> | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.128.0/18【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 8 | interface Vlan<TBD> | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.192.0/18【図】。バッジ .2。vip .3（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 9 | interface Vlan<TBD> | 冗長ペアの tk1-core01 と同じ構成（tk1-core02 の箱では線が省略）。アドレス 172.17.64.0/18【図】。バッジ .x+1（値が未確定なので <TBD>）。vip .3（VRRP） | 【図】【推測】 | R-034, R-035, R-036, R-037 |
| 10 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/3・Te0/4 にまたがる（R5）。対向 tk1-sr1acc02 Te0/1, tk1-sr1acc02 Te0/2 | 【図】【推測：対称性】 |  |
| 11 | Po3 trunk 10-11,100-299 | Po3 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/5・Te0/6 にまたがる（R5）。対向 tk1-sr1acc02-dup2 Te0/1, tk1-sr1acc02-dup2 Te0/2 | 【図】【推測：対称性】 |  |
| 12 | Te0/1 access 2 | Te0/1 が EXT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-fw01 Te0/3 | 【図】【推測：対称性】 |  |
| 13 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-rt01 Gi0/3 | 【図】【推測：対称性】 |  |
| 14 | Te0/7 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Te0/7 が OFFICE_Fn・MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-fnacc01-dup2 Te0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 15 | Te0/22 access 9 | Te0/22 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-mgmt02 Gi0/2 | 【図】【推測：対称性】 |  |
| 16 | Te0/23 trunk 2,10-11,100-399 | Te0/23 が EXT・DMZ・COMMON・APx_PROD・APx_DEV・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-core01 Te0/23 | 【図】【推測：対称性】 |  |
| 17 | Te0/24 trunk 2,10-11,100-399 | Te0/24 が EXT・DMZ・COMMON・APx_PROD・APx_DEV・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-core01 Te0/24 | 【図】【推測：対称性】 |  |
| 18 | 管理（r12） | Mgmt ポートが管理SWにつながるが vrf 箱もバッジも無い → 管理 VRF に入れる（R12） | 【推測】 |  |
| 19 | route 172.18.0.0/16 → 172.17.0.2 | 論理構成図の矢印「to 大阪」→ tk1-rt01。next-hop は tk1-rt01 の 2 | 【論】 |  |
| 20 | route 0.0.0.0/0 → 172.17.0.1 | 論理構成図の矢印「default」→ tk1-fw01。next-hop は tk1-fw01 の .1 | 【論】 |  |
| 21 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

### 3.9 tk1-fnacc01（C社 L2switch 1000-24、L2SW）

ファイル: `configs/tk1-fnacc01.cfg`

```
! ==== tk1-fnacc01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-fnacc01
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address <TBD:MGMT_IP_tk1-fnacc01> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to tk1-fnacc01-dup2 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface GigabitEthernet0/1
 description to tk1-f6ap01 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
 power inline auto ! 【図】PoE（AP 接続）
!
interface GigabitEthernet0/2
 description PoE予備
 shutdown ! 図に「PoE予備」と明示（R14）
!
interface range GigabitEthernet0/3 - 20
 description to オフィス固定端末 x5-10 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
!
interface GigabitEthernet0/23
 description to tk1-fnacc01-dup2 Gi0/23 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface GigabitEthernet0/24
 description to tk1-fnacc01-dup2 Gi0/24 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/7 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
ip default-gateway 172.17.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-fnacc01 | Host 欄「tk1-fnacc01 / C社 L2switch 1000-24」（cell 9BYiFAK1cGA9hBdD1Cum-374） | 【図】 | R-036, R-037 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.17.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-036, R-037 |
| 4 | Gi0/1 access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Gi0/1 が OFFICE_Fn の横線に所属（所属線【図】）。対向 tk1-f6ap01 Gi0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 5 | Gi0/2 shutdown | 図に「PoE予備」と明示（R14） | 【図】 |  |
| 6 | Gi0/3-20 access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Gi0/3-20 が OFFICE_Fn の横線に所属（所属線【図】）。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 7 | Po1 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Po1 が MGMT・OFFICE_Fn の横線に所属（所属線【図】）。Po 箱が Gi0/23・Gi0/24 にまたがる（R5）。対向 tk1-fnacc01-dup2 Gi0/23, tk1-fnacc01-dup2 Gi0/24。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 8 | Te0/1 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Te0/1 が MGMT・OFFICE_Fn の横線に所属（所属線【図】）。対向 tk1-core01 Te0/7。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】 |  |
| 9 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.10 tk1-fnacc01-dup2（C社 L2switch 1000-24、L2SW）

ファイル: `configs/tk1-fnacc01-dup2.cfg`

```
! ==== tk1-fnacc01-dup2 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-fnacc01-dup2 ! WARN R-037 R-036
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
vlan 300-399 ! OFFICE_Fn（集約表現: 個々の VLAN 名は <TBD>）
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address <TBD:MGMT_IP_tk1-fnacc01-dup2> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to tk1-fnacc01 Po1
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
interface GigabitEthernet0/1
 description to tk1-f6ap02 Gi0/1 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
 power inline auto ! 【図】PoE（AP 接続）
!
interface GigabitEthernet0/2
 description PoE予備
 shutdown ! 図に「PoE予備」と明示（R14）
!
interface range GigabitEthernet0/3 - 20
 description to オフィス固定端末 x5-10 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 spanning-tree portfast
!
interface GigabitEthernet0/23
 description to tk1-fnacc01 Gi0/23 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface GigabitEthernet0/24
 description to tk1-fnacc01 Gi0/24 [RJ45 1000BASE-T(Cat6a)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
 channel-group 1 mode active
!
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/7 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>
 ! OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4）
!
ip default-gateway 172.17.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-fnacc01-dup2 | Host 欄「tk1-fnacc01 / C社 L2switch 1000-24」（cell 9BYiFAK1cGA9hBdD1Cum-488）。同名の機器があるため仮称 | 【図】【推測】 | R-036, R-037 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.17.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-036, R-037 |
| 4 | Gi0/1 access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Gi0/1 が OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-f6ap02 Gi0/1。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 5 | Gi0/2 shutdown | 図に「PoE予備」と明示（R14） | 【図】 |  |
| 6 | Gi0/3-20 access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Gi0/3-20 が OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 7 | Po1 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Po1 が MGMT・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Gi0/23・Gi0/24 にまたがる（R5）。対向 tk1-fnacc01 Gi0/23, tk1-fnacc01 Gi0/24。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 8 | Te0/1 trunk 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | Te0/1 が MGMT・OFFICE_Fn の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-core02 Te0/7。OFFICE_Fn は払い出し単位（フロア）の機器向けなので <TBD>（5.4） | 【図】【推測：対称性】 |  |
| 9 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.11 tk1-fw01（C社 Firewall 3000、FW）

ファイル: `configs/tk1-fw01.cfg`

```
! ==== tk1-fw01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco ASA（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-fw01
!
interface TenGigabitEthernet0/1
 description to 回線終端装置 [SFP+/LC 10GBASE-SR(OM3)]
 nameif outside
 security-level 0
 ip address <TBD:TK-INET_IP_tk1-fw01> 255.255.255.128
!
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 bridge-group 2
 nameif to-tk1-core01
 security-level 100
!
interface TenGigabitEthernet0/3
 description to tk1-core02 Te0/1 [SFP+/LC 10GBASE-SR(OM3)]
 bridge-group 2
 nameif to-tk1-core02
 security-level 100
!
interface BVI2
 description EXT（Te0/2+Te0/3）
 ip address 172.17.0.1 255.255.255.224 ! 【推測】同一セグメントの2ポートを BVI で表現（R10）
!
same-security-traffic permit inter-interface
!
route outside 0.0.0.0 0.0.0.0 <TBD:Internet_GW> ! 【論】 default
route to-tk1-core01 172.17.0.0 255.255.0.0 172.17.0.6 ! 【論】 to東京（tk1 拠点ブロック【推測】）
!
! --- NAT・ポリシーの雛形（【一般】6.2） ---
object network OBJ-TK1-INTERNAL
 subnet 172.17.0.0 255.255.0.0
 nat (any,outside) dynamic interface
access-list OUTSIDE-IN extended <TBD:FW_POLICY>
access-group OUTSIDE-IN in interface outside
!
!
ntp server <TBD:NTP_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-fw01 | Host 欄「tk1-fw01 / C社 Firewall 3000」（cell 9BYiFAK1cGA9hBdD1Cum-145） | 【図】 | R-035 |
| 2 | 記法（asa） | 図の Vendor Model「C社 Firewall 3000」は実在のベンダー名・型番として読めない。ファイアウォールとして ASA 記法を採用（同一セグメントの2ポートを BVI で表現できる）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface BVI（Te0/2+Te0/3） | ルーティング箱（GRT）と EXT の横線が線でつながる。アドレス 172.17.0.0/27【図】。バッジ .1。同じ横線に2ポート（Te0/2・Te0/3）がつながるので BVI（R10、4.2） | 【図】【推測】 | R-035 |
| 4 | interface Te0/1（L3） | ルーティング箱（GRT）と TK-INET の横線が線でつながる。アドレス 198.51.100.0/25【図】。バッジ .x（値が未確定なので <TBD>） | 【図】 | R-035 |
| 5 | Te0/2 access 2 | Te0/2 が EXT の横線に所属（所属線【図】）。対向 tk1-core01 Te0/1 | 【図】 |  |
| 6 | Te0/3 access 2 | Te0/3 が EXT の横線に所属（所属線【図】）。対向 tk1-core02 Te0/1 | 【図】 |  |
| 7 | route 0.0.0.0/0 → <TBD:Internet_GW> | 論理構成図の矢印「default」→ Internet。相手側の IP は図に無い | 【論】 |  |
| 8 | route 172.17.0.0/16 → 172.17.0.6 | 論理構成図の矢印「to東京」→ tk1-core01/02。next-hop は VIP .6 | 【論】 |  |

### 3.12 tk1-mgmt01（C社 L2switch 1000-48、L2SW）

ファイル: `configs/tk1-mgmt01.cfg`

```
! ==== tk1-mgmt01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-mgmt01
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address <TBD:MGMT_IP_tk1-mgmt01> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to tk1-mgmt02 Po1
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/1
 description to tk1-core01 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/2
 description to tk1-core01 Te0/22 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/3
 description to tk1-sr1acc01 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/4
 description to tk1-sr1acc01-dup2 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/5
 description to tk1-svr101 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/6
 description to tk1-svr102 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/12
 description to tk1-svr108 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9 ! WARN R-012
 spanning-tree portfast
!
interface GigabitEthernet0/47
 description to tk1-mgmt02 Gi0/47 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
!
interface GigabitEthernet0/48
 description to tk1-mgmt02 Gi0/48 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
!
ip default-gateway 172.17.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-mgmt01 | Host 欄「tk1-mgmt01 / C社 L2switch 1000-48」（cell 9BYiFAK1cGA9hBdD1Cum-360） | 【図】 | R-036 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-48」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.17.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-036 |
| 4 | Gi0/1 access 9 | Gi0/1 が MGMT の横線に所属（所属線【図】）。対向 tk1-core01 Mgmt | 【図】 |  |
| 5 | Gi0/2 access 9 | Gi0/2 が MGMT の横線に所属（所属線【図】）。対向 tk1-core01 Te0/22 | 【図】 |  |
| 6 | Gi0/3 access 9 | Gi0/3 が MGMT の横線に所属（所属線【図】）。対向 tk1-sr1acc01 Mgmt | 【図】 |  |
| 7 | Gi0/4 access 9 | Gi0/4 が MGMT の横線に所属（所属線【図】）。対向 tk1-sr1acc01-dup2 Mgmt | 【図】 |  |
| 8 | Gi0/5 access 9 | Gi0/5 が MGMT の横線に所属（所属線【図】）。対向 tk1-svr101 BMC | 【図】 |  |
| 9 | Gi0/6 access 9 | Gi0/6 が MGMT の横線に所属（所属線【図】）。対向 tk1-svr102 BMC | 【図】 |  |
| 10 | Gi0/12 access 9 | Gi0/12 が MGMT の横線に所属（ラベルへの線【図】(D-04)）。対向 tk1-svr108 BMC | 【図】 | R-012 |
| 11 | Po1 access 9 | Po1 が MGMT の横線に所属（所属線【図】）。Po 箱が Gi0/47・Gi0/48 にまたがる（R5）。対向 tk1-mgmt02 Gi0/47, tk1-mgmt02 Gi0/48 | 【図】 |  |
| 12 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.13 tk1-mgmt02（C社 L2switch 1000-48、L2SW）

ファイル: `configs/tk1-mgmt02.cfg`

```
! ==== tk1-mgmt02 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-mgmt02
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 9
 name MGMT
!
interface Vlan9
 description MGMT 172.17.1.0/24
 ip address <TBD:MGMT_IP_tk1-mgmt02> 255.255.255.0 ! 【論】合成図のラベルと違うため論理構成図の値
!
interface Port-channel1
 description to tk1-mgmt01 Po1
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/1
 description to tk1-core02 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/2
 description to tk1-core02 Te0/22 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/3
 description to tk1-sr1acc02 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/4
 description to tk1-sr1acc02-dup2 Mgmt [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
!
interface GigabitEthernet0/5
 description to tk1-svr201 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/6
 description to tk1-svr202 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/12
 description to tk1-svr208 BMC [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
!
interface GigabitEthernet0/47
 description to tk1-mgmt01 Gi0/47 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
!
interface GigabitEthernet0/48
 description to tk1-mgmt01 Gi0/48 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
!
ip default-gateway 172.17.1.3 ! 【推測】MGMT の VIP .3
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-mgmt02 | Host 欄「tk1-mgmt02 / C社 L2switch 1000-48」（cell 9BYiFAK1cGA9hBdD1Cum-503） | 【図】 | R-036 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 1000-48」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan9 | MGMT の色の IP バッジがある。アドレス 172.17.1.0/24【論】。バッジ .x（値が未確定なので <TBD>） | 【図】【論】 | R-036 |
| 4 | Gi0/1 access 9 | Gi0/1 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-core02 Mgmt | 【図】【推測：対称性】 |  |
| 5 | Gi0/2 access 9 | Gi0/2 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-core02 Te0/22 | 【図】【推測：対称性】 |  |
| 6 | Gi0/3 access 9 | Gi0/3 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-sr1acc02 Mgmt | 【図】【推測：対称性】 |  |
| 7 | Gi0/4 access 9 | Gi0/4 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-sr1acc02-dup2 Mgmt | 【図】【推測：対称性】 |  |
| 8 | Gi0/5 access 9 | Gi0/5 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr201 BMC | 【図】【推測：対称性】 |  |
| 9 | Gi0/6 access 9 | Gi0/6 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr202 BMC | 【図】【推測：対称性】 |  |
| 10 | Gi0/12 access 9 | Gi0/12 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr208 BMC | 【図】【推測：対称性】 |  |
| 11 | Po1 access 9 | Po1 が MGMT の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Gi0/47・Gi0/48 にまたがる（R5）。対向 tk1-mgmt01 Gi0/47, tk1-mgmt01 Gi0/48 | 【図】【推測：対称性】 |  |
| 12 | 管理（inband） | 管理セグメントの横線上にバッジだけがある → インバンド管理（SVI） | 【図】 |  |

### 3.14 tk1-rt01（C社 Router 1000、ルーター）

ファイル: `configs/tk1-rt01.cfg`

```
! ==== tk1-rt01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE (ISR)（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-rt01
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 2
 name EXT
!
interface Vlan2
 description EXT 172.17.0.0/27
 ip address 172.17.0.2 255.255.255.224
!
interface GigabitEthernet0/1
 description to 回線終端装置 [RJ45 1000BASE-T(Cat6a)]
 ip address <TBD:INTER-BLDG_IP_tk1-rt01> 255.255.255.0
!
interface GigabitEthernet0/2
 description to tk1-core01 Te0/2 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
interface GigabitEthernet0/3
 description to tk1-core02 Te0/2 [RJ45 1000BASE-T(Cat6a)]
 switchport mode access
 switchport access vlan 2
!
ip route 172.17.0.0 255.255.0.0 172.17.0.6 ! 【論】 to東京（tk1 拠点ブロック【推測】）
ip route 172.18.0.0 255.255.0.0 <TBD:INTER-BLDG_IP_os1-rt01> ! 【論】 to大阪（os1 拠点ブロック【推測】）
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-rt01 | Host 欄「tk1-rt01 / C社 Router 1000」（cell 9BYiFAK1cGA9hBdD1Cum-146） | 【図】 | R-035 |
| 2 | 記法（isr） | 図の Vendor Model「C社 Router 1000」は実在のベンダー名・型番として読めない。ルーターとして静的経路・スイッチポート＋SVI を書ける ISR（IOS-XE）を採用。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | interface Vlan2 | ルーティング箱（GRT）と EXT の横線が線でつながる。アドレス 172.17.0.0/27【図】。バッジ 2。同じ横線に2ポートがつながるのでスイッチポート＋SVI（R10、4.2） | 【図】 | R-035 |
| 4 | interface Gi0/1（L3） | ルーティング箱（GRT）と INTER-BLDG の横線が線でつながる。アドレス 172.16.0.0/24【図】。バッジ .x（値が未確定なので <TBD>） | 【図】 | R-035 |
| 5 | Gi0/2 access 2 | Gi0/2 が EXT の横線に所属（所属線【図】）。対向 tk1-core01 Te0/2 | 【図】 |  |
| 6 | Gi0/3 access 2 | Gi0/3 が EXT の横線に所属（所属線【図】）。対向 tk1-core02 Te0/2 | 【図】 |  |
| 7 | route 172.18.0.0/16 → <TBD:INTER-BLDG_IP_os1-rt01> | 論理構成図の矢印「to大阪」→ os1-rt01。next-hop は os1-rt01 の .x | 【論】 |  |
| 8 | route 172.17.0.0/16 → 172.17.0.6 | 論理構成図の矢印「to東京」→ tk1-core01/02。next-hop は VIP .6 | 【論】 |  |

### 3.15 tk1-sr1acc01（C社 L2switch 3000-24、L2SW）

ファイル: `configs/tk1-sr1acc01.cfg`

```
! ==== tk1-sr1acc01 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-sr1acc01
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
!
interface Port-channel1
 description to tk1-sr1acc02 Po1
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface Port-channel2
 description to tk1-core01 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt01 Gi0/3 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-sr1acc01> 255.255.255.0
!
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/3 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/4 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/3
 description to tk1-svr101 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr102 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_PROD_VLAN>
 ! APx_PROD は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/10
 description to tk1-svr108 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_DEV_VLAN>
 ! APx_DEV は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc02 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc02 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-sr1acc01 | Host 欄「tk1-sr1acc01 / C社 L2switch 3000-24」（cell 9BYiFAK1cGA9hBdD1Cum-231） | 【図】 | R-034 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | Po1 trunk 10-11,100-299 | Po1 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 tk1-sr1acc02 Te0/23, tk1-sr1acc02 Te0/24 | 【図】 |  |
| 4 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/1・Te0/2 にまたがる（R5）。対向 tk1-core01 Te0/3, tk1-core01 Te0/4 | 【図】 |  |
| 5 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（所属線【図】）。対向 tk1-svr101 eth1 | 【図】 |  |
| 6 | Te0/4 access <TBD:APx_PROD_VLAN> | Te0/4 が APx_PROD の横線に所属（所属線【図】）。対向 tk1-svr102 eth1。APx_PROD は VLAN 範囲なので access の VLAN は <TBD> | 【図】 |  |
| 7 | Te0/10 access <TBD:APx_DEV_VLAN> | Te0/10 が APx_DEV の横線に所属（所属線【図】）。対向 tk1-svr108 eth1。APx_DEV は VLAN 範囲なので access の VLAN は <TBD> | 【図】 |  |
| 8 | 管理（oob） | vrf 箱（mgmt）と Mgmt ポート → OOB 管理 | 【図】 |  |
| 9 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

### 3.16 tk1-sr1acc01-dup2（C社 L2switch 3000-24、L2SW）

ファイル: `configs/tk1-sr1acc01-dup2.cfg`

```
! ==== tk1-sr1acc01-dup2 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-sr1acc01-dup2 ! WARN R-034
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
!
interface Port-channel1
 description to tk1-sr1acc02-dup2 Po1
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface Port-channel2
 description to tk1-core01 Po3
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt01 Gi0/4 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-sr1acc01-dup2> 255.255.255.0
!
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/5 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/6 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/3
 description to tk1-svr201 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr202 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_PROD_VLAN>
 ! APx_PROD は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/10
 description to tk1-svr208 eth1 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_DEV_VLAN>
 ! APx_DEV は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc02-dup2 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc02-dup2 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-sr1acc01-dup2 | Host 欄「tk1-sr1acc01 / C社 L2switch 3000-24」（cell 9BYiFAK1cGA9hBdD1Cum-406）。同名の機器があるため仮称 | 【図】【推測】 | R-034 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | Po1 trunk 10-11,100-299 | Po1 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 tk1-sr1acc02-dup2 Te0/23, tk1-sr1acc02-dup2 Te0/24 | 【図】 |  |
| 4 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（所属線【図】）。Po 箱が Te0/1・Te0/2 にまたがる（R5）。対向 tk1-core01 Te0/5, tk1-core01 Te0/6 | 【図】 |  |
| 5 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（所属線【図】）。対向 tk1-svr201 eth1 | 【図】 |  |
| 6 | Te0/4 access <TBD:APx_PROD_VLAN> | Te0/4 が APx_PROD の横線に所属（所属線【図】）。対向 tk1-svr202 eth1。APx_PROD は VLAN 範囲なので access の VLAN は <TBD> | 【図】 |  |
| 7 | Te0/10 access <TBD:APx_DEV_VLAN> | Te0/10 が APx_DEV の横線に所属（所属線【図】）。対向 tk1-svr208 eth1。APx_DEV は VLAN 範囲なので access の VLAN は <TBD> | 【図】 |  |
| 8 | 管理（oob） | vrf 箱（mgmt）と Mgmt ポート → OOB 管理 | 【図】 |  |
| 9 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

### 3.17 tk1-sr1acc02（C社 L2switch 3000-24、L2SW）

ファイル: `configs/tk1-sr1acc02.cfg`

```
! ==== tk1-sr1acc02 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-sr1acc02
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
!
interface Port-channel1
 description to tk1-sr1acc01 Po1
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface Port-channel2
 description to tk1-core02 Po2
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt02 Gi0/3 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-sr1acc02> 255.255.255.0
!
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/3 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/2
 description to tk1-core02 Te0/4 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/3
 description to tk1-svr101 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr102 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_PROD_VLAN>
 ! APx_PROD は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/10
 description to tk1-svr108 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_DEV_VLAN>
 ! APx_DEV は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc01 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc01 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-sr1acc02 | Host 欄「tk1-sr1acc02 / C社 L2switch 3000-24」（cell 9BYiFAK1cGA9hBdD1Cum-392） | 【図】 | R-034 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | Po1 trunk 10-11,100-299 | Po1 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 tk1-sr1acc01 Te0/23, tk1-sr1acc01 Te0/24 | 【図】【推測：対称性】 |  |
| 4 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/1・Te0/2 にまたがる（R5）。対向 tk1-core02 Te0/3, tk1-core02 Te0/4 | 【図】【推測：対称性】 |  |
| 5 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr101 eth2 | 【図】【推測：対称性】 |  |
| 6 | Te0/4 access <TBD:APx_PROD_VLAN> | Te0/4 が APx_PROD の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr102 eth2。APx_PROD は VLAN 範囲なので access の VLAN は <TBD> | 【図】【推測：対称性】 |  |
| 7 | Te0/10 access <TBD:APx_DEV_VLAN> | Te0/10 が APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr108 eth2。APx_DEV は VLAN 範囲なので access の VLAN は <TBD> | 【図】【推測：対称性】 |  |
| 8 | 管理（oob） | vrf 箱（mgmt）と Mgmt ポート → OOB 管理 | 【図】 |  |
| 9 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

### 3.18 tk1-sr1acc02-dup2（C社 L2switch 3000-24、L2SW）

ファイル: `configs/tk1-sr1acc02-dup2.cfg`

```
! ==== tk1-sr1acc02-dup2 ====
! 生成: nwdiag2cfg 0.1.0 / 入力: diagrams.drawio.svg / タブ: 物理・論理合成図_4C
! 記法: Cisco IOS-XE（特定不能）
! <TBD:...> は投入前に置換が必要（configs.md の TBD 一覧）
!
hostname tk1-sr1acc02-dup2 ! WARN R-034
!
vrf definition mgmt
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst ! 【一般】L2 ループがあるため（V-06）
!
vlan 10
 name DMZ
vlan 11
 name COMMON
vlan 100-199 ! APx_PROD（集約表現: 個々の VLAN 名は <TBD>）
vlan 200-299 ! APx_DEV（集約表現: 個々の VLAN 名は <TBD>）
!
interface Port-channel1
 description to tk1-sr1acc01-dup2 Po1
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface Port-channel2
 description to tk1-core02 Po3
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
!
interface GigabitEthernet0/0 ! 図の「Mgmt」
 description to tk1-mgmt02 Gi0/4 [RJ45 1000BASE-T(Cat6a)]
 vrf forwarding mgmt
 ip address <TBD:MGMT_IP_tk1-sr1acc02-dup2> 255.255.255.0
!
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/5 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/2
 description to tk1-core02 Te0/6 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 2 mode active
!
interface TenGigabitEthernet0/3
 description to tk1-svr201 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11
 spanning-tree portfast trunk
!
interface TenGigabitEthernet0/4
 description to tk1-svr202 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_PROD_VLAN>
 ! APx_PROD は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/10
 description to tk1-svr208 eth2 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode access
 switchport access vlan <TBD:APx_DEV_VLAN>
 ! APx_DEV は VLAN 範囲なので access の VLAN は <TBD>
 spanning-tree portfast
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc01-dup2 Te0/23 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc01-dup2 Te0/24 [SFP+/LC 10GBASE-SR(OM3)]
 switchport mode trunk
 switchport trunk allowed vlan 10-11,100-299
 channel-group 1 mode active
!
ip route vrf mgmt 0.0.0.0 0.0.0.0 172.17.1.3 ! 【推測】 mgmt default
!
!
ntp server <TBD:NTP_SERVER>
logging host <TBD:SYSLOG_SERVER>
!
end
```

| # | 設定 | 図の何を見たか / どう判断したか | 根拠ラベル | 指摘ID |
|---|---|---|---|---|
| 1 | hostname tk1-sr1acc02-dup2 | Host 欄「tk1-sr1acc02 / C社 L2switch 3000-24」（cell 9BYiFAK1cGA9hBdD1Cum-447）。同名の機器があるため仮称 | 【図】【推測】 | R-034 |
| 2 | 記法（iosxe） | 図の Vendor Model「C社 L2switch 3000-24」は実在のベンダー名・型番として読めない。L2スイッチとして Catalyst 9200/9300 系 IOS-XE を採用（管理用 VRF の概念がある）。ポート名の形式（Te/Gi/Po）も Cisco 形式。機種確定後にポート番号体系・管理IF名・冗長化プロトコルの書式を見直す | 【推測】 |  |
| 3 | Po1 trunk 10-11,100-299 | Po1 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/23・Te0/24 にまたがる（R5）。対向 tk1-sr1acc01-dup2 Te0/23, tk1-sr1acc01-dup2 Te0/24 | 【図】【推測：対称性】 |  |
| 4 | Po2 trunk 10-11,100-299 | Po2 が DMZ・COMMON・APx_PROD・APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。Po 箱が Te0/1・Te0/2 にまたがる（R5）。対向 tk1-core02 Te0/5, tk1-core02 Te0/6 | 【図】【推測：対称性】 |  |
| 5 | Te0/3 trunk 10-11 | Te0/3 が DMZ・COMMON の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr201 eth2 | 【図】【推測：対称性】 |  |
| 6 | Te0/4 access <TBD:APx_PROD_VLAN> | Te0/4 が APx_PROD の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr202 eth2。APx_PROD は VLAN 範囲なので access の VLAN は <TBD> | 【図】【推測：対称性】 |  |
| 7 | Te0/10 access <TBD:APx_DEV_VLAN> | Te0/10 が APx_DEV の横線に所属（冗長ペアの対称性【推測：対称性】）。対向 tk1-svr208 eth2。APx_DEV は VLAN 範囲なので access の VLAN は <TBD> | 【図】【推測：対称性】 |  |
| 8 | 管理（oob） | vrf 箱（mgmt）と Mgmt ポート → OOB 管理 | 【図】 |  |
| 9 | route 0.0.0.0/0 → 172.17.1.3 (vrf mgmt) | 管理 VRF のデフォルト経路（6.2）。next-hop は MGMT の VIP .3 | 【推測】 |  |

## 4. 推測で補った項目

| # | 機器 | 項目 | 採用値 | 推論の根拠 | 確認すべき人/情報 |
|---|---|---|---|---|---|
| 1 | tk1-sr1acc01-dup2 | hostname | tk1-sr1acc01-dup2 | 図のホスト名 tk1-sr1acc01 が重複しているため自動の仮称（D7） | 設計者 |
| 2 | tk1-fnacc01-dup2 | hostname | tk1-fnacc01-dup2 | 図のホスト名 tk1-fnacc01 が重複しているため自動の仮称（D7） | 設計者 |
| 3 | tk1-sr1acc02-dup2 | hostname | tk1-sr1acc02-dup2 | 図のホスト名 tk1-sr1acc02 が重複しているため自動の仮称（D7） | 設計者 |
| 4 | os1-core02 | 未接続線 9BYiFAK1cGA9hBdD1Cum-758 | os1-core02 Te0/4 と tk1-svr101-dup3 eth2 のケーブル | 未接続端が eth2（cell 9BYiFAK1cGA9hBdD1Cum-553）の上で終わっている（距離 0.0）。裏付け: 冗長ペアの os1-core01 Te0/4 が tk1-svr101-dup3 eth1 に接続（同じ拠点のペアの対称性） | 設計者 |
| 5 | os1-core02 | VLAN 所属・L3 の対称コピー | os1-core01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 6 | tk1-core02 | VLAN 所属・L3 の対称コピー | tk1-core01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 7 | tk1-sr1acc02 | VLAN 所属・L3 の対称コピー | tk1-sr1acc01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 8 | tk1-sr1acc02-dup2 | VLAN 所属・L3 の対称コピー | tk1-sr1acc01-dup2 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 9 | tk1-fnacc01-dup2 | VLAN 所属・L3 の対称コピー | tk1-fnacc01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 10 | tk1-mgmt02 | VLAN 所属・L3 の対称コピー | tk1-mgmt01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 11 | os1-fmacc02 | VLAN 所属・L3 の対称コピー | os1-fmacc01 と同じ | 冗長ペアの片方の省略（2.10） | 設計者 |
| 12 | os1-core01 | 未接続線 9BYiFAK1cGA9hBdD1Cum-119 | os1-core01 GRT と横線（EXT）の所属線 | 未接続端が GRT（cell 9BYiFAK1cGA9hBdD1Cum-122）の上で終わっている（距離 0.0）。裏付け: 同じ機器に #CC0000 の IP バッジ（.4）がある | 設計者 |
| 13 | tk1-svr108 | 未接続線 9BYiFAK1cGA9hBdD1Cum-472 | tk1-svr108 eth1 と横線（APx_DEV）の所属線 | 未接続端が eth1（cell 9BYiFAK1cGA9hBdD1Cum-128）の上で終わっている（距離 0.0）。裏付け: 接続先の tk1-sr1acc01 Te0/10 が同じ色のセグメントに所属 | 設計者 |
| 14 | tk1-svr108 | 未接続線 9BYiFAK1cGA9hBdD1Cum-473 | tk1-svr108 eth2 と横線（APx_DEV）の所属線 | 未接続端が eth2（cell 9BYiFAK1cGA9hBdD1Cum-127）の上で終わっている（距離 0.0）。裏付け: 接続先の tk1-sr1acc02 Te0/10 が同じ色のセグメントに所属 | 設計者 |
| 15 | tk1-core02 | Mgmt を管理 VRF mgmt に入れる | IP は <TBD> | Mgmt ポートが管理SWにつながるが vrf 箱もバッジも無い（R12） | 設計者 |
| 16 | tk1-core01 | Mgmt を管理 VRF mgmt に入れる | IP は <TBD> | Mgmt ポートが管理SWにつながるが vrf 箱もバッジも無い（R12） | 設計者 |
| 17 | tk1-sr1acc02 | Mgmt を vrf mgmt に入れる |  | vrf 箱と Mgmt ポートの間の線が無い（省略と推定） | 設計者 |
| 18 | tk1-sr1acc02-dup2 | Mgmt を vrf mgmt に入れる |  | vrf 箱と Mgmt ポートの間の線が無い（省略と推定） | 設計者 |
| 19 | os1 | 拠点ブロック | 172.18.0.0/16 | 拠点内のセグメント（VLAN あり）の多くが含まれる /16（4 件） | 設計者 |
| 20 | tk1 | 拠点ブロック | 172.17.0.0/16 | 拠点内のセグメント（VLAN あり）の多くが含まれる /16（7 件） | 設計者 |
| 21 | - | 拠点名「東京」 | tk1 | 論理構成図で別拠点の機器に向かう矢印のラベル（cell J5z6EYH7W0RdXeQXPurJ-133） | 設計者 |
| 22 | - | 拠点名「大阪」 | os1 | 論理構成図で別拠点の機器に向かう矢印のラベル（cell J5z6EYH7W0RdXeQXPurJ-135） | 設計者 |

## 5. 既定値を使った項目（既定値ファイルで未指定だった項目）

| # | 項目 | 採用した既定値 | 説明 | ナレッジの参照箇所 | 影響する機器 |
|---|---|---|---|---|---|
| 1 | mgmt_vrf_name | mgmt | 管理 VRF の名前（図に vrf 箱が無い場合） | 1.1 / R12 | tk1-core01, tk1-core02 |
| 2 | stp_mode | rapid-pvst | STP モード（冗長経路がある場合） | 6.2 | os1-core01, os1-core02, os1-fmacc01, os1-fmacc02, os1-rt01, tk1-core01, tk1-core02, tk1-fnacc01, tk1-fnacc01-dup2, tk1-mgmt01, tk1-mgmt02, tk1-rt01, tk1-sr1acc01, tk1-sr1acc01-dup2, tk1-sr1acc02, tk1-sr1acc02-dup2 |
| 3 | fhrp_protocol | legend | 冗長化プロトコル（legend=凡例の表記、vrrp、hsrp） | 1.1 / 2.7 | os1-core01, os1-core02, tk1-core01, tk1-core02 |
| 4 | fhrp_format | vrrpv3 | VRRP の書式（vrrpv3、legacy=旧 IOS 書式） | 1.1 / 10.1 | os1-core01, os1-core02, tk1-core01, tk1-core02 |
| 5 | fhrp_group | vlan_id | グループ番号の規則（vlan_id） | 6.2 | os1-core01, os1-core02, tk1-core01, tk1-core02 |
| 6 | fhrp_priority_primary | 110 | 01号機の優先度 | 1.1 / 6.2 | os1-core01, os1-core02, tk1-core01, tk1-core02 |
| 7 | fhrp_preempt | True | プリエンプト | 1.1 / 6.2 | os1-core01, os1-core02, tk1-core01, tk1-core02 |
| 8 | trunk_extra | [] | trunk に付ける追加コマンド | 1.1 / 10.1 | os1-core01, os1-core02, os1-fmacc01, os1-fmacc02, tk1-core01, tk1-core02, tk1-fnacc01, tk1-fnacc01-dup2, tk1-sr1acc01, tk1-sr1acc01-dup2, tk1-sr1acc02, tk1-sr1acc02-dup2 |
| 9 | lag_mode | active | LAG モード（active=LACP, on=static） | 1.1 / R5 / 6.2 | os1-core01, os1-core02, os1-fmacc01, os1-fmacc02, tk1-core01, tk1-core02, tk1-fnacc01, tk1-fnacc01-dup2, tk1-mgmt01, tk1-mgmt02, tk1-sr1acc01, tk1-sr1acc01-dup2, tk1-sr1acc02, tk1-sr1acc02-dup2 |

## 6. 未確定値（TBD）一覧

`<TBD:...>` は有効な設定行のまま置いているので、すべて**投入前に置換が必要**です（構文エラーになるため置換漏れに気付けます）。同じ識別子は同じ値に置き換えてください（対向・冗長ペアで一致させる値）。

| # | 機器 | 設定行 | プレースホルダ | 必要な情報 | 投入前に置換 |
|---|---|---|---|---|---|
| 1 | os1-core01 | interface Vlan<TBD:OFFICE_Fn_VLAN_ID> | <TBD:OFFICE_Fn_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 2 | os1-core01 | ip address <TBD:OFFICE_Fn_IP_os1-core01> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_IP_os1-core01> | IP 管理表 | 必須 |
| 3 | os1-core01 | ip address <TBD:OFFICE_Fn_IP_os1-core01> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_MASK> | IP 管理表 | 必須 |
| 4 | os1-core01 | vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4 | <TBD:OFFICE_Fn_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 5 | os1-core01 | address <TBD:OFFICE_Fn_VIP> primary | <TBD:OFFICE_Fn_VIP> | IP 管理表 | 必須 |
| 6 | os1-core01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 7 | os1-core01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 8 | os1-core01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 9 | os1-core02 | interface Vlan<TBD:OFFICE_Fn_VLAN_ID> | <TBD:OFFICE_Fn_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 10 | os1-core02 | ip address <TBD:OFFICE_Fn_IP_os1-core02> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_IP_os1-core02> | IP 管理表 | 必須 |
| 11 | os1-core02 | ip address <TBD:OFFICE_Fn_IP_os1-core02> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_MASK> | IP 管理表 | 必須 |
| 12 | os1-core02 | vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4 | <TBD:OFFICE_Fn_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 13 | os1-core02 | address <TBD:OFFICE_Fn_VIP> primary | <TBD:OFFICE_Fn_VIP> | IP 管理表 | 必須 |
| 14 | os1-core02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 15 | os1-core02 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 16 | os1-core02 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 17 | os1-fmacc01 | ip address <TBD:MGMT_IP_os1-fmacc01> 255.255.255.0 | <TBD:MGMT_IP_os1-fmacc01> | IP 管理表 | 必須 |
| 18 | os1-fmacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 19 | os1-fmacc01 | switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 20 | os1-fmacc01 | switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 21 | os1-fmacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 22 | os1-fmacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 23 | os1-fmacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 24 | os1-fmacc01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 25 | os1-fmacc01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 26 | os1-fmacc02 | ip address <TBD:MGMT_IP_os1-fmacc02> 255.255.255.0 | <TBD:MGMT_IP_os1-fmacc02> | IP 管理表 | 必須 |
| 27 | os1-fmacc02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 28 | os1-fmacc02 | switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 29 | os1-fmacc02 | switchport access vlan <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 30 | os1-fmacc02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 31 | os1-fmacc02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 32 | os1-fmacc02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@os1-fmacc01> | <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 33 | os1-fmacc02 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 34 | os1-fmacc02 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 35 | os1-fw01 | ip address <TBD:OS-INET_IP_os1-fw01> 255.255.255.128 | <TBD:OS-INET_IP_os1-fw01> | IP 管理表 | 必須 |
| 36 | os1-fw01 | route outside 0.0.0.0 0.0.0.0 <TBD:Internet_GW> | <TBD:Internet_GW> | 回線契約（ISP 側 GW） | 必須 |
| 37 | os1-fw01 | access-list OUTSIDE-IN extended <TBD:FW_POLICY> | <TBD:FW_POLICY> | セキュリティポリシー | 必須 |
| 38 | os1-fw01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 39 | os1-rt01 | ip address <TBD:INTER-BLDG_IP_os1-rt01> 255.255.255.0 | <TBD:INTER-BLDG_IP_os1-rt01> | IP 管理表 | 必須 |
| 40 | os1-rt01 | ip route 172.17.0.0 255.255.0.0 <TBD:INTER-BLDG_IP_tk1-rt01> | <TBD:INTER-BLDG_IP_tk1-rt01> | IP 管理表 | 必須 |
| 41 | os1-rt01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 42 | os1-rt01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 43 | tk1-core01 | interface Vlan<TBD:APx_PROD_VLAN_ID> | <TBD:APx_PROD_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 44 | tk1-core01 | ip address <TBD:APx_PROD_IP_tk1-core01> <TBD:APx_PROD_MASK> | <TBD:APx_PROD_IP_tk1-core01> | IP 管理表 | 必須 |
| 45 | tk1-core01 | ip address <TBD:APx_PROD_IP_tk1-core01> <TBD:APx_PROD_MASK> | <TBD:APx_PROD_MASK> | IP 管理表 | 必須 |
| 46 | tk1-core01 | vrrp <TBD:APx_PROD_VRRP_GROUP> address-family ipv4 | <TBD:APx_PROD_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 47 | tk1-core01 | address <TBD:APx_PROD_VIP> primary | <TBD:APx_PROD_VIP> | IP 管理表 | 必須 |
| 48 | tk1-core01 | interface Vlan<TBD:APx_DEV_VLAN_ID> | <TBD:APx_DEV_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 49 | tk1-core01 | ip address <TBD:APx_DEV_IP_tk1-core01> <TBD:APx_DEV_MASK> | <TBD:APx_DEV_IP_tk1-core01> | IP 管理表 | 必須 |
| 50 | tk1-core01 | ip address <TBD:APx_DEV_IP_tk1-core01> <TBD:APx_DEV_MASK> | <TBD:APx_DEV_MASK> | IP 管理表 | 必須 |
| 51 | tk1-core01 | vrrp <TBD:APx_DEV_VRRP_GROUP> address-family ipv4 | <TBD:APx_DEV_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 52 | tk1-core01 | address <TBD:APx_DEV_VIP> primary | <TBD:APx_DEV_VIP> | IP 管理表 | 必須 |
| 53 | tk1-core01 | interface Vlan<TBD:OFFICE_Fn_VLAN_ID> | <TBD:OFFICE_Fn_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 54 | tk1-core01 | ip address <TBD:OFFICE_Fn_IP_tk1-core01> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_IP_tk1-core01> | IP 管理表 | 必須 |
| 55 | tk1-core01 | ip address <TBD:OFFICE_Fn_IP_tk1-core01> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_MASK> | IP 管理表 | 必須 |
| 56 | tk1-core01 | vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4 | <TBD:OFFICE_Fn_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 57 | tk1-core01 | address <TBD:OFFICE_Fn_VIP> primary | <TBD:OFFICE_Fn_VIP> | IP 管理表 | 必須 |
| 58 | tk1-core01 | ip address <TBD:MGMT_IP_tk1-core01> 255.255.255.0 | <TBD:MGMT_IP_tk1-core01> | IP 管理表 | 必須 |
| 59 | tk1-core01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 60 | tk1-core01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 61 | tk1-core01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 62 | tk1-core02 | interface Vlan<TBD:APx_PROD_VLAN_ID> | <TBD:APx_PROD_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 63 | tk1-core02 | ip address <TBD:APx_PROD_IP_tk1-core02> <TBD:APx_PROD_MASK> | <TBD:APx_PROD_IP_tk1-core02> | IP 管理表 | 必須 |
| 64 | tk1-core02 | ip address <TBD:APx_PROD_IP_tk1-core02> <TBD:APx_PROD_MASK> | <TBD:APx_PROD_MASK> | IP 管理表 | 必須 |
| 65 | tk1-core02 | vrrp <TBD:APx_PROD_VRRP_GROUP> address-family ipv4 | <TBD:APx_PROD_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 66 | tk1-core02 | address <TBD:APx_PROD_VIP> primary | <TBD:APx_PROD_VIP> | IP 管理表 | 必須 |
| 67 | tk1-core02 | interface Vlan<TBD:APx_DEV_VLAN_ID> | <TBD:APx_DEV_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 68 | tk1-core02 | ip address <TBD:APx_DEV_IP_tk1-core02> <TBD:APx_DEV_MASK> | <TBD:APx_DEV_IP_tk1-core02> | IP 管理表 | 必須 |
| 69 | tk1-core02 | ip address <TBD:APx_DEV_IP_tk1-core02> <TBD:APx_DEV_MASK> | <TBD:APx_DEV_MASK> | IP 管理表 | 必須 |
| 70 | tk1-core02 | vrrp <TBD:APx_DEV_VRRP_GROUP> address-family ipv4 | <TBD:APx_DEV_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 71 | tk1-core02 | address <TBD:APx_DEV_VIP> primary | <TBD:APx_DEV_VIP> | IP 管理表 | 必須 |
| 72 | tk1-core02 | interface Vlan<TBD:OFFICE_Fn_VLAN_ID> | <TBD:OFFICE_Fn_VLAN_ID> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 73 | tk1-core02 | ip address <TBD:OFFICE_Fn_IP_tk1-core02> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_IP_tk1-core02> | IP 管理表 | 必須 |
| 74 | tk1-core02 | ip address <TBD:OFFICE_Fn_IP_tk1-core02> <TBD:OFFICE_Fn_MASK> | <TBD:OFFICE_Fn_MASK> | IP 管理表 | 必須 |
| 75 | tk1-core02 | vrrp <TBD:OFFICE_Fn_VRRP_GROUP> address-family ipv4 | <TBD:OFFICE_Fn_VRRP_GROUP> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 76 | tk1-core02 | address <TBD:OFFICE_Fn_VIP> primary | <TBD:OFFICE_Fn_VIP> | IP 管理表 | 必須 |
| 77 | tk1-core02 | ip address <TBD:MGMT_IP_tk1-core02> 255.255.255.0 | <TBD:MGMT_IP_tk1-core02> | IP 管理表 | 必須 |
| 78 | tk1-core02 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 79 | tk1-core02 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 80 | tk1-core02 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 81 | tk1-fnacc01 | ip address <TBD:MGMT_IP_tk1-fnacc01> 255.255.255.0 | <TBD:MGMT_IP_tk1-fnacc01> | IP 管理表 | 必須 |
| 82 | tk1-fnacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 83 | tk1-fnacc01 | switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 84 | tk1-fnacc01 | switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 85 | tk1-fnacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 86 | tk1-fnacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 87 | tk1-fnacc01 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 88 | tk1-fnacc01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 89 | tk1-fnacc01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 90 | tk1-fnacc01-dup2 | ip address <TBD:MGMT_IP_tk1-fnacc01-dup2> 255.255.255.0 | <TBD:MGMT_IP_tk1-fnacc01-dup2> | IP 管理表 | 必須 |
| 91 | tk1-fnacc01-dup2 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 92 | tk1-fnacc01-dup2 | switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 93 | tk1-fnacc01-dup2 | switchport access vlan <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 94 | tk1-fnacc01-dup2 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 95 | tk1-fnacc01-dup2 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 96 | tk1-fnacc01-dup2 | switchport trunk allowed vlan 9,<TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | 設計ルール（単位ごとの VLAN 払い出し） | 必須 |
| 97 | tk1-fnacc01-dup2 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 98 | tk1-fnacc01-dup2 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 99 | tk1-fw01 | ip address <TBD:TK-INET_IP_tk1-fw01> 255.255.255.128 | <TBD:TK-INET_IP_tk1-fw01> | IP 管理表 | 必須 |
| 100 | tk1-fw01 | route outside 0.0.0.0 0.0.0.0 <TBD:Internet_GW> | <TBD:Internet_GW> | 回線契約（ISP 側 GW） | 必須 |
| 101 | tk1-fw01 | access-list OUTSIDE-IN extended <TBD:FW_POLICY> | <TBD:FW_POLICY> | セキュリティポリシー | 必須 |
| 102 | tk1-fw01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 103 | tk1-mgmt01 | ip address <TBD:MGMT_IP_tk1-mgmt01> 255.255.255.0 | <TBD:MGMT_IP_tk1-mgmt01> | IP 管理表 | 必須 |
| 104 | tk1-mgmt01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 105 | tk1-mgmt01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 106 | tk1-mgmt02 | ip address <TBD:MGMT_IP_tk1-mgmt02> 255.255.255.0 | <TBD:MGMT_IP_tk1-mgmt02> | IP 管理表 | 必須 |
| 107 | tk1-mgmt02 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 108 | tk1-mgmt02 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 109 | tk1-rt01 | ip address <TBD:INTER-BLDG_IP_tk1-rt01> 255.255.255.0 | <TBD:INTER-BLDG_IP_tk1-rt01> | IP 管理表 | 必須 |
| 110 | tk1-rt01 | ip route 172.18.0.0 255.255.0.0 <TBD:INTER-BLDG_IP_os1-rt01> | <TBD:INTER-BLDG_IP_os1-rt01> | IP 管理表 | 必須 |
| 111 | tk1-rt01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 112 | tk1-rt01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 113 | tk1-sr1acc01 | ip address <TBD:MGMT_IP_tk1-sr1acc01> 255.255.255.0 | <TBD:MGMT_IP_tk1-sr1acc01> | IP 管理表 | 必須 |
| 114 | tk1-sr1acc01 | switchport access vlan <TBD:APx_PROD_VLAN> | <TBD:APx_PROD_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 115 | tk1-sr1acc01 | switchport access vlan <TBD:APx_DEV_VLAN> | <TBD:APx_DEV_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 116 | tk1-sr1acc01 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 117 | tk1-sr1acc01 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 118 | tk1-sr1acc01-dup2 | ip address <TBD:MGMT_IP_tk1-sr1acc01-dup2> 255.255.255.0 | <TBD:MGMT_IP_tk1-sr1acc01-dup2> | IP 管理表 | 必須 |
| 119 | tk1-sr1acc01-dup2 | switchport access vlan <TBD:APx_PROD_VLAN> | <TBD:APx_PROD_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 120 | tk1-sr1acc01-dup2 | switchport access vlan <TBD:APx_DEV_VLAN> | <TBD:APx_DEV_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 121 | tk1-sr1acc01-dup2 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 122 | tk1-sr1acc01-dup2 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 123 | tk1-sr1acc02 | ip address <TBD:MGMT_IP_tk1-sr1acc02> 255.255.255.0 | <TBD:MGMT_IP_tk1-sr1acc02> | IP 管理表 | 必須 |
| 124 | tk1-sr1acc02 | switchport access vlan <TBD:APx_PROD_VLAN> | <TBD:APx_PROD_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 125 | tk1-sr1acc02 | switchport access vlan <TBD:APx_DEV_VLAN> | <TBD:APx_DEV_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 126 | tk1-sr1acc02 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 127 | tk1-sr1acc02 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 128 | tk1-sr1acc02-dup2 | ip address <TBD:MGMT_IP_tk1-sr1acc02-dup2> 255.255.255.0 | <TBD:MGMT_IP_tk1-sr1acc02-dup2> | IP 管理表 | 必須 |
| 129 | tk1-sr1acc02-dup2 | switchport access vlan <TBD:APx_PROD_VLAN> | <TBD:APx_PROD_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 130 | tk1-sr1acc02-dup2 | switchport access vlan <TBD:APx_DEV_VLAN> | <TBD:APx_DEV_VLAN> | 設計ルール（VLAN ID / VRRP グループ） | 必須 |
| 131 | tk1-sr1acc02-dup2 | ntp server <TBD:NTP_SERVER> | <TBD:NTP_SERVER> | 運用設計（管理サーバーの IP） | 必須 |
| 132 | tk1-sr1acc02-dup2 | logging host <TBD:SYSLOG_SERVER> | <TBD:SYSLOG_SERVER> | 運用設計（管理サーバーの IP） | 必須 |

**決める情報源ごとのまとめ**

- IP 管理表: `<TBD:APx_DEV_IP_tk1-core01>`, `<TBD:APx_DEV_IP_tk1-core02>`, `<TBD:APx_DEV_MASK>`, `<TBD:APx_DEV_VIP>`, `<TBD:APx_PROD_IP_tk1-core01>`, `<TBD:APx_PROD_IP_tk1-core02>`, `<TBD:APx_PROD_MASK>`, `<TBD:APx_PROD_VIP>`, `<TBD:INTER-BLDG_IP_os1-rt01>`, `<TBD:INTER-BLDG_IP_tk1-rt01>`, `<TBD:MGMT_IP_os1-fmacc01>`, `<TBD:MGMT_IP_os1-fmacc02>`, `<TBD:MGMT_IP_tk1-core01>`, `<TBD:MGMT_IP_tk1-core02>`, `<TBD:MGMT_IP_tk1-fnacc01-dup2>`, `<TBD:MGMT_IP_tk1-fnacc01>`, `<TBD:MGMT_IP_tk1-mgmt01>`, `<TBD:MGMT_IP_tk1-mgmt02>`, `<TBD:MGMT_IP_tk1-sr1acc01-dup2>`, `<TBD:MGMT_IP_tk1-sr1acc01>`, `<TBD:MGMT_IP_tk1-sr1acc02-dup2>`, `<TBD:MGMT_IP_tk1-sr1acc02>`, `<TBD:OFFICE_Fn_IP_os1-core01>`, `<TBD:OFFICE_Fn_IP_os1-core02>`, `<TBD:OFFICE_Fn_IP_tk1-core01>`, `<TBD:OFFICE_Fn_IP_tk1-core02>`, `<TBD:OFFICE_Fn_MASK>`, `<TBD:OFFICE_Fn_VIP>`, `<TBD:OS-INET_IP_os1-fw01>`, `<TBD:TK-INET_IP_tk1-fw01>`
- セキュリティポリシー: `<TBD:FW_POLICY>`
- 回線契約（ISP 側 GW）: `<TBD:Internet_GW>`
- 設計ルール（VLAN ID / VRRP グループ）: `<TBD:APx_DEV_VLAN>`, `<TBD:APx_DEV_VLAN_ID>`, `<TBD:APx_DEV_VRRP_GROUP>`, `<TBD:APx_PROD_VLAN>`, `<TBD:APx_PROD_VLAN_ID>`, `<TBD:APx_PROD_VRRP_GROUP>`, `<TBD:OFFICE_Fn_VLAN_ID>`, `<TBD:OFFICE_Fn_VRRP_GROUP>`
- 設計ルール（単位ごとの VLAN 払い出し）: `<TBD:OFFICE_Fn_VLAN@os1-fmacc01>`, `<TBD:OFFICE_Fn_VLAN@tk1-fnacc01>`
- 運用設計（管理サーバーの IP）: `<TBD:NTP_SERVER>`, `<TBD:SYSLOG_SERVER>`

## 7. 図との差分（図と違う設定にした箇所。V-09 の結果）

| # | 機器 | ポート/項目 | 図の記載 | コンフィグ | 理由 |
|---|---|---|---|---|---|
| 1 | os1-core02 | Gi0/1 | OFFICE_Fn(300-399), MGMT(9) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 2 | tk1-core02 | Te0/7 | OFFICE_Fn(300-399), MGMT(9) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 3 | tk1-core01 | Te0/7 | OFFICE_Fn(300-399), MGMT(9) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 4 | os1-core01 | Te0/5 | OFFICE_Fn(300-399), MGMT(9) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 5 | tk1-sr1acc01 | Te0/4 | APx_PROD(100-199) | 100-199 の範囲 → <TBD:APx_PROD_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 6 | tk1-sr1acc01 | Te0/10 | APx_DEV(200-299) | 200-299 の範囲 → <TBD:APx_DEV_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 7 | tk1-fnacc01 | Gi0/1 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 8 | tk1-fnacc01 | Gi0/24 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 9 | tk1-fnacc01 | Gi0/23 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 10 | tk1-fnacc01 | Te0/1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 11 | tk1-fnacc01 | Gi0/3-20 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 12 | tk1-fnacc01 | Po1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 13 | tk1-sr1acc02 | Te0/4 | APx_PROD(100-199) | 100-199 の範囲 → <TBD:APx_PROD_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 14 | tk1-sr1acc02 | Te0/10 | APx_DEV(200-299) | 200-299 の範囲 → <TBD:APx_DEV_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 15 | tk1-sr1acc01-dup2 | Te0/4 | APx_PROD(100-199) | 100-199 の範囲 → <TBD:APx_PROD_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 16 | tk1-sr1acc01-dup2 | Te0/10 | APx_DEV(200-299) | 200-299 の範囲 → <TBD:APx_DEV_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 17 | tk1-sr1acc02-dup2 | Te0/4 | APx_PROD(100-199) | 100-199 の範囲 → <TBD:APx_PROD_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 18 | tk1-sr1acc02-dup2 | Te0/10 | APx_DEV(200-299) | 200-299 の範囲 → <TBD:APx_DEV_VLAN>（access に範囲は書けない） | 5.4 集約 VLAN の扱い |
| 19 | tk1-fnacc01-dup2 | Gi0/1 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 20 | tk1-fnacc01-dup2 | Te0/1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 21 | tk1-fnacc01-dup2 | Gi0/3-20 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 22 | tk1-fnacc01-dup2 | Gi0/23 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 23 | tk1-fnacc01-dup2 | Gi0/24 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 24 | tk1-fnacc01-dup2 | Po1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@tk1-fnacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 25 | os1-fmacc01 | Gi0/1 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 26 | os1-fmacc01 | Gi0/24 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 27 | os1-fmacc01 | Gi0/23 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 28 | os1-fmacc01 | Te0/1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 29 | os1-fmacc01 | Gi0/3-20 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 30 | os1-fmacc01 | Po1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 31 | os1-fmacc02 | Gi0/1 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 32 | os1-fmacc02 | Te0/1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 33 | os1-fmacc02 | Gi0/3-20 | OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 34 | os1-fmacc02 | Gi0/23 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 35 | os1-fmacc02 | Gi0/24 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |
| 36 | os1-fmacc02 | Po1 | MGMT(9), OFFICE_Fn(300-399) | 300-399 の範囲 → <TBD:OFFICE_Fn_VLAN@os1-fmacc01>（払い出し単位） | 5.4 集約 VLAN の扱い |

理由の記載が無い差分: なし

## 8. チェック実施結果

| チェックID | 内容 | 結果 |
|---|---|---|
| N-01 | ホスト名の重複 | 該当あり（R-016, R-017, R-018, R-019, R-020, R-021） |
| N-02 | ホスト名の命名規則違反 | 該当あり（R-022, R-023） |
| N-03 | ページ間での名前の違い | 該当あり（R-024） |
| N-04 | ラック・フロア名の重複・誤記 | 該当なし |
| N-05 | ポート名の重複（同一機器内） | 該当なし |
| A-01 | セグメント間のアドレス重複・包含 | 該当あり（R-001, R-002, R-003） |
| A-02 | 拠点ブロック外のアドレス | 該当あり（R-005） |
| A-03 | バッジのIPがサブネット外・NW/BCアドレス | 該当なし |
| A-04 | 同一セグメントで同じIP | 該当なし |
| A-05 | 冗長ペアのIP規則の不一致 | 該当あり（R-006, R-007） |
| A-06 | バッジの表記揺れ | 該当あり（R-043） |
| A-07 | 拠点間のラベルの使い回し | 該当あり（R-004） |
| V-01 | VLAN ID の重複 | 該当なし |
| V-02 | 同じセグメント名で VLAN ID が違う | 該当なし |
| V-03 | ラベルの無い横線・横線につながらないラベル | 該当あり（R-031） |
| V-04 | リンク両端の VLAN 所属の不一致 | 該当なし |
| V-05 | VLAN の通り道の断絶 | 該当あり（R-057） |
| V-06 | L2 ループ | 該当あり（R-032, R-033, R-034, R-035, R-036, R-037） |
| V-07 | VRRP グループ番号の制約 | 該当あり（R-038, R-039, R-040） |
| V-08 | VLAN の孤立（自己点検） | 該当なし |
| V-09 | 図とコンフィグの VLAN 所属の差分（自己点検） | 該当なし |
| P-01 | 線の未接続 | 該当あり（R-025, R-026, R-027, R-028） |
| P-02 | 1つの物理ポートに複数のケーブル | 該当なし |
| P-03 | ポート名と線種（速度）の矛盾 | 該当あり（R-029） |
| P-04 | 両端のコネクタ・ケーブル種別の不一致 | 該当なし |
| P-05 | 機種のポート数・種類との整合 | 該当なし |
| P-06 | LAG メンバーの対向不一致 | 該当なし |
| P-07 | LAG 番号・メンバー数の両端不一致 | 該当あり（R-030, R-048, R-049） |
| P-08 | 冗長化の片肺 | 該当あり（R-050, R-051, R-052, R-053, R-054, R-055, R-056） |
| L-01 | ゲートウェイの無いセグメント | 該当なし |
| L-02 | 冗長ペアの片方にしか SVI/バッジが無い | 該当なし |
| L-03 | 冗長化プロトコルの不一致 | 該当なし |
| L-04 | next-hop が直接接続セグメント上に無い | 該当なし |
| L-05 | 経路の欠落・非対称 | 該当あり（R-044） |
| L-06 | VRF 間の到達性 | 対象外（管理サービス（NTP/DNS/Syslog）の IP が図にも既定値ファイルにも無い） |
| L-07 | 冗長ペアのセグメントの L2 連続性 | 該当あり（R-014, R-045） |
| M-01 | 管理IFの無い機器 | 該当あり（R-015） |
| M-02 | 管理経路の単一障害点 | 該当なし |
| M-03 | OOB とインバンドの混在 | 該当あり（R-046） |
| M-04 | 管理サービスの所在 | 該当あり（R-047） |
| X-01 | 合成図と論理構成図のセグメント一致 | 該当あり（R-041, R-042, R-058） |
| X-02 | 合成図と物理構成図の機器・結線の一致 | 対象外（物理構成図ページの指定なし） |
| X-03 | カラー版とモノクロ版のラベル差分 | 対象外（カラー版だけで処理する設定（D12）） |
| D-01 | 凡例に無い色・線種 | 該当なし |
| D-02 | 線の交差でつながりが曖昧な箇所 | 対象外（線の経路の交差は本ツールでは判定しない（目視で確認）） |
| D-03 | 所属線の色の不一致 | 該当あり（R-008, R-009, R-010, R-011） |
| D-04 | 所属線がラベルにつながっている | 該当あり（R-012, R-013） |

## 9. 対象外とした要素

### 9.1 無線AP の設定項目表（コンフィグは作らない。ナレッジ 1.2）

| AP | 機種 | 接続先 | 給電 | スイッチ側の VLAN | 管理IP（バッジ） | 未確定事項 |
|---|---|---|---|---|---|---|
| os1-fmap01 | Wifi AP | os1-fmacc01 Gi0/1 | PoE | access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | .x（OFFICE_Fn） | SSID と VLAN の対応、管理 IP、コントローラー |
| os1-fmap02 | Wifi AP | os1-fmacc02 Gi0/1 | PoE | access <TBD:OFFICE_Fn_VLAN@os1-fmacc01> | .x（OFFICE_Fn） | SSID と VLAN の対応、管理 IP、コントローラー |
| tk1-f6ap01 | Wifi AP | tk1-fnacc01 Gi0/1 | PoE | access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | .x（OFFICE_Fn） | SSID と VLAN の対応、管理 IP、コントローラー |
| tk1-f6ap02 | Wifi AP | tk1-fnacc01-dup2 Gi0/1 | PoE | access <TBD:OFFICE_Fn_VLAN@tk1-fnacc01> | .x（#333333） | SSID と VLAN の対応、管理 IP、コントローラー |

### 9.2 サーバー・その他

| 機器 | 機種 | 役割 | 扱い |
|---|---|---|---|
| tk1-cdns01 | Linux/djbdns | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-cdns01-dup2 | Linux/djbdns | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-proxy01 | Linux/Squid | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-proxy01-dup2 | Linux/Squid | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr101 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr101-dup2 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr101-dup3 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr102 | D社 RackMountServer X100V社 Hypervisor (業務アプリ/本番系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr108 | D社 RackMountServer X100V社 Hypervisor (業務アプリ/開発系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr201 | D社 RackMountServer X100V社 Hypervisor (共通サービス系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr202 | D社 RackMountServer X100V社 Hypervisor (業務アプリ/本番系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |
| tk1-svr208 | D社 RackMountServer X100V社 Hypervisor (業務アプリ/開発系) | サーバー | スイッチ側の所属の根拠と、描画ミスのチェックにだけ使用 |


# 物理・論理合成図からのコンフィグ書き起こし

作成日 2026-11-23。対象は diagrams.drawio.svg の「物理・論理合成図_4C」。1C版の合成図とカラー版の論理構成図・物理構成図を補助に使用しました。変換ナレッジは1.1版です。

## 確認が必要な項目

- **R-001** 両拠点の管理VLAN9ラベルが東京DMZと重複。論理図の東京172.17.1.0/24、大阪172.18.1.0/24を採用。
- **R-003** 大阪コア02のGi0/1と10GBASE-SRが矛盾。図のIF名を保持し、実機のポートと光モジュールを要確認。
- **R-009 / R-010** 大阪EXTと東京VLAN9のVRRPは迂回L2経路に依存します。各拠点のSTP収束とASA経由のBPDU・VRRP転送を実機で要確認。
- **R-013 / R-011 / R-012** ISP・拠点間IP、個別VLAN割当、VRRPグループ番号、FWの許可条件を確定する必要があります。
- インターフェース番号体系とCisco機種固有の構文を実機で検証してください。有効行のTBDは投入前に置換必須です。

## 1. 機種判定と台帳

図の「C社」の機種名から実機型番・OSは特定できません。Te/Gi/Poの表記と、SVI・VRRP・VRF・LAG・BVIの要件に基づき、役割別のCisco記法を適用しました。

| 出力ホスト名 | 図のホスト名 | 図の機種 | 拠点 | 役割 | 冗長ペア | 採用記法 | cell id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| os1-core01 | os1-core01 | C社 L3switch 9000-24 | 大阪 | L3SW | os1-core02 | IOS-XE / Catalyst 9000 | 9BYiFAK1cGA9hBdD1Cum-162 |
| os1-core02 | os1-core02 | C社 L3switch 9000-24 | 大阪 | L3SW | os1-core01 | IOS-XE / Catalyst 9000 | 9BYiFAK1cGA9hBdD1Cum-142 |
| os1-fmacc01 | os1-fmacc01 | C社 L2switch 1000-24 | 大阪 | アクセスSW | os1-fmacc02 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-521 |
| os1-fmacc02 | os1-fmacc02 | C社 L2switch 1000-24 | 大阪 | アクセスSW | os1-fmacc01 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-581 |
| os1-fw01 | os1-fw01 | C社 Firewall 3000 | 大阪 | FW | — | Cisco Secure Firewall ASA | 9BYiFAK1cGA9hBdD1Cum-143 |
| os1-rt01 | os1-rt01 | C社 Router 1000 | 大阪 | RT | — | IOS-XE / ISR EtherSwitch＋SVI | 9BYiFAK1cGA9hBdD1Cum-144 |
| tk1-core01 | tk1-core01 | C社 L3switch 9000-24 | 東京 | L3SW | tk1-core02 | IOS-XE / Catalyst 9000 | 9BYiFAK1cGA9hBdD1Cum-148 |
| tk1-core02 | tk1-core02 | C社 L3switch 9000-24 | 東京 | L3SW | tk1-core01 | IOS-XE / Catalyst 9000 | 9BYiFAK1cGA9hBdD1Cum-147 |
| tk1-fnacc01 | tk1-fnacc01 | C社 L2switch 1000-24 | 東京 | アクセスSW | tk1-fnacc02 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-374 |
| tk1-fnacc02 | tk1-fnacc01 | C社 L2switch 1000-24 | 東京 | アクセスSW | tk1-fnacc01 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-488 |
| tk1-fw01 | tk1-fw01 | C社 Firewall 3000 | 東京 | FW | — | Cisco Secure Firewall ASA | 9BYiFAK1cGA9hBdD1Cum-145 |
| tk1-mgmt01 | tk1-mgmt01 | C社 L2switch 1000-48 | 東京 | 管理SW | tk1-mgmt02 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-360 |
| tk1-mgmt02 | tk1-mgmt02 | C社 L2switch 1000-48 | 東京 | 管理SW | tk1-mgmt01 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-503 |
| tk1-rt01 | tk1-rt01 | C社 Router 1000 | 東京 | RT | — | IOS-XE / ISR EtherSwitch＋SVI | 9BYiFAK1cGA9hBdD1Cum-146 |
| tk1-sr1acc01 | tk1-sr1acc01 | C社 L2switch 3000-24 | 東京 | アクセスSW | tk1-sr1acc02 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-231 |
| tk1-sr1acc02 | tk1-sr1acc02 | C社 L2switch 3000-24 | 東京 | アクセスSW | tk1-sr1acc01 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-392 |
| tk1-sr2acc01 | tk1-sr1acc01 | C社 L2switch 3000-24 | 東京 | アクセスSW | tk1-sr2acc02 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-406 |
| tk1-sr2acc02 | tk1-sr1acc02 | C社 L2switch 3000-24 | 東京 | アクセスSW | tk1-sr2acc01 | IOS-XE / Catalyst 9200/9300 | 9BYiFAK1cGA9hBdD1Cum-447 |

## 2. 抽出サマリ

### 2.1 セグメント台帳

| 拠点 | 色 | セグメント | VLAN | CIDR | L3実IP | VIP |
| --- | --- | --- | --- | --- | --- | --- |
| tk1 | #FF66FF | INET | — | 198.51.100.0/25 | FW .x | — |
| tk1 | #9999FF | INTER-BLDG | — | 172.16.0.0/24 | 両RT .x | — |
| tk1 | #CC0000 | EXT | 2 | 172.17.0.0/27 | FW .1、RT .2、core01 .4、core02 .5 | 172.17.0.6 |
| tk1 | #6600CC | MGMT | 9 | 172.17.1.0/24 | core01 .1、core02 .2 | 172.17.1.3 |
| tk1 | #CC6600 | DMZ | 10 | 172.17.2.0/24 | core01 .1、core02 .2 | 172.17.2.3 |
| tk1 | #007FFF | COMMON | 11 | 172.17.3.0/24 | core01 .1、core02 .2 | 172.17.3.3 |
| tk1 | #009900 | APx_PROD | 100-199 | 172.17.128.0/18 | VLANごとに払い出し | VLANごとに確定 |
| tk1 | #66CC00 | APx_DEV | 200-299 | 172.17.192.0/18 | VLANごとに払い出し | VLANごとに確定 |
| tk1 | #999900 | OFFICE | 300-399 | 172.17.64.0/18 | VLANごとに払い出し | VLANごとに確定 |
| os1 | #FF66FF | INET | — | 203.0.113.0/25 | FW .x | — |
| os1 | #9999FF | INTER-BLDG | — | 172.16.0.0/24 | 両RT .x | — |
| os1 | #CC0000 | EXT | 2 | 172.18.0.0/27 | FW .1、RT .2、core01 .4、core02 .5 | 172.18.0.6 |
| os1 | #6600CC | MGMT | 9 | 172.18.1.0/24 | core01 .1、core02 .2 | 172.18.1.3 |
| os1 | #CC6600 | DMZ | 10 | 172.18.2.0/24 | core01 .1、core02 .2 | 172.18.2.3 |
| os1 | #007FFF | COMMON | 11 | 172.18.3.0/24 | core01 .1、core02 .2 | 172.18.3.3 |
| os1 | #999900 | OFFICE | 300-399 | 172.18.64.0/18 | VLANごとに払い出し | VLANごとに確定 |

### 2.2 結線表

凡例の丸と線幅で媒体を判定しました。大阪サーバーの推定リンクは R-004 参照。

| A機器・ポート | A端点 | B機器・ポート | B端点 | 媒体 | A/B LAG | cell id |
| --- | --- | --- | --- | --- | --- | --- |
| os1-rt01 Gi0/3 | — | os1-core02 Te0/2 | ○ | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-101 |
| os1-core01 Te0/24 | ● | os1-core02 Te0/24 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-106 |
| os1-core01 Te0/23 | ● | os1-core02 Te0/23 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-108 |
| tk1-core01 Te0/24 | ● | tk1-core02 Te0/24 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-184 |
| tk1-core01 Te0/23 | ● | tk1-core02 Te0/23 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-186 |
| tk1-core01 Mgmt | — | tk1-mgmt01 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-200 |
| tk1-core01 Te0/2 | ○ | tk1-rt01 Gi0/2 | — | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-22 |
| tk1-svr101 BMC | — | tk1-mgmt01 Gi0/5 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-303 |
| tk1-svr102 BMC | — | tk1-mgmt01 Gi0/6 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-305 |
| tk1-svr108 BMC | — | tk1-mgmt01 Gi0/12 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-307 |
| tk1-core01 Te0/1 | ● | tk1-fw01 Te0/2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-309 |
| tk1-sr1acc01 Te0/24 | ● | tk1-sr1acc02 Te0/24 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-31 |
| tk1-sr1acc02 Mgmt | — | tk1-mgmt02 Gi0/3 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-313 |
| tk1-sr1acc01 Te0/23 | ● | tk1-sr1acc02 Te0/23 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-32 |
| tk1-svr208 BMC | — | tk1-mgmt02 Gi0/12 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-327 |
| tk1-svr202 BMC | — | tk1-mgmt02 Gi0/6 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-329 |
| tk1-sr1acc01 Te0/1 | ● | tk1-core01 Te0/3 | ● | 10GBASE-SR OM3 | Po2 / Po2 | 9BYiFAK1cGA9hBdD1Cum-33 |
| tk1-svr201 BMC | — | tk1-mgmt02 Gi0/5 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-331 |
| tk1-mgmt01 Gi0/47 | — | tk1-mgmt02 Gi0/47 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-334 |
| tk1-sr1acc01 Mgmt | — | tk1-mgmt01 Gi0/3 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-338 |
| tk1-core02 Mgmt | — | tk1-mgmt02 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-345 |
| tk1-sr2acc02 Mgmt | — | tk1-mgmt02 Gi0/4 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-347 |
| tk1-core01 Te0/22 | ○ | tk1-mgmt01 Gi0/2 | — | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-350 |
| tk1-core02 Te0/22 | ○ | tk1-mgmt02 Gi0/2 | — | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-357 |
| tk1-sr1acc01 Te0/2 | ● | tk1-core01 Te0/4 | ● | 10GBASE-SR OM3 | Po2 / Po2 | 9BYiFAK1cGA9hBdD1Cum-36 |
| tk1-fnacc01 Gi0/3-20 | — | オフィス端末  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-385 |
| tk1-fnacc02 Gi0/3-20 | — | オフィス端末  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-386 |
| tk1-sr2acc01 Te0/24 | ● | tk1-sr2acc02 Te0/24 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-395 |
| tk1-sr2acc01 Te0/23 | ● | tk1-sr2acc02 Te0/23 | ● | 10GBASE-SR OM3 | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-396 |
| tk1-sr1acc02 Te0/1 | ● | tk1-core02 Te0/3 | ● | 10GBASE-SR OM3 | Po2 / Po2 | 9BYiFAK1cGA9hBdD1Cum-41 |
| tk1-sr1acc02 Te0/2 | ● | tk1-core02 Te0/4 | ● | 10GBASE-SR OM3 | Po2 / Po2 | 9BYiFAK1cGA9hBdD1Cum-43 |
| tk1-sr2acc01 Mgmt | — | tk1-mgmt01 Gi0/4 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-440 |
| tk1-sr2acc01 Te0/3 | ● | tk1-svr201 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-448 |
| tk1-sr2acc01 Te0/4 | ● | tk1-svr202 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-449 |
| tk1-sr2acc02 Te0/3 | ● | tk1-svr201 eth2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-450 |
| tk1-sr2acc02 Te0/4 | ● | tk1-svr202 eth2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-451 |
| tk1-svr208 eth2 | ● | tk1-sr2acc02 Te0/10 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-452 |
| tk1-svr208 eth1 | ● | tk1-sr2acc01 Te0/10 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-453 |
| tk1-sr2acc01 Te0/1 | ● | tk1-core01 Te0/5 | ● | 10GBASE-SR OM3 | Po2 / Po3 | 9BYiFAK1cGA9hBdD1Cum-468 |
| tk1-sr2acc02 Te0/2 | ● | tk1-core02 Te0/6 | ● | 10GBASE-SR OM3 | Po2 / Po3 | 9BYiFAK1cGA9hBdD1Cum-469 |
| tk1-core01 Te0/6 | ● | tk1-sr2acc01 Te0/2 | ● | 10GBASE-SR OM3 | Po3 / Po2 | 9BYiFAK1cGA9hBdD1Cum-470 |
| tk1-core02 Te0/5 | ● | tk1-sr2acc02 Te0/1 | ● | 10GBASE-SR OM3 | Po3 / Po2 | 9BYiFAK1cGA9hBdD1Cum-471 |
| tk1-fnacc01 Gi0/23 | — | tk1-fnacc02 Gi0/23 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-499 |
| tk1-fnacc01 Gi0/24 | — | tk1-fnacc02 Gi0/24 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-500 |
| tk1-mgmt01 Gi0/48 | — | tk1-mgmt02 Gi0/48 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-502 |
| os1-fmacc01 Gi0/1 | — | os1-fmap01 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-507 |
| os1-fmacc02 Gi0/1 | — | os1-fmap02 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-511 |
| os1-fmacc01 Gi0/3-20 | — | オフィス端末  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-527 |
| os1-fmacc02 Gi0/3-20 | — | オフィス端末  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-528 |
| os1-fmacc01 Gi0/23 | — | os1-fmacc02 Gi0/23 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-543 |
| os1-fmacc01 Gi0/24 | — | os1-fmacc02 Gi0/24 | — | 1000BASE-T Cat6a | Po1 / Po1 | 9BYiFAK1cGA9hBdD1Cum-544 |
| os1-fw01 Te0/2 | ● | os1-core01 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-580 |
| os1-core02 Gi0/1 | ● | os1-fmacc02 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-582 |
| os1-fmacc01 Gi0/21 | — | os1-svr101 BMC | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-604 |
| os1-fmacc02 Gi0/21 | — | os1-svr102 BMC | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-605 |
| tk1-rt01 Gi0/1 | — | 回線終端装置  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-64 |
| tk1-fw01 Te0/3 | ● | tk1-core02 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-66 |
| tk1-rt01 Gi0/3 | — | tk1-core02 Te0/2 | ○ | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-68 |
| 回線終端装置  | ● | tk1-fw01 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-70 |
| tk1-fnacc01 Gi0/1 | — | tk1-f6ap01 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-74 |
| os1-core01 Te0/2 | ○ | os1-rt01 Gi0/2 | — | 1000BASE-T Cat6a, SFP+ copper | — / — | 9BYiFAK1cGA9hBdD1Cum-754 |
| os1-fw01 Te0/3 | ● | os1-core02 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-755 |
| tk1-fnacc01 Te0/1 | ● | tk1-core01 Te0/7 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-756 |
| os1-core01 Te0/4 | ● | os1-svr102 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-757 |
| os1-core01 Te0/5 | ● | os1-fmacc01 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-759 |
| os1-svr101 eth1 | ● | os1-core01 Te0/3 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-760 |
| os1-svr101 eth2 | ● | os1-core02 Te0/3 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-761 |
| tk1-sr1acc02 Te0/3 | ● | tk1-svr101 eth2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-762 |
| tk1-sr1acc01 Te0/4 | ● | tk1-svr102 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-763 |
| tk1-sr1acc02 Te0/4 | ● | tk1-svr102 eth2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-764 |
| tk1-svr108 eth2 | ● | tk1-sr1acc02 Te0/10 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-765 |
| tk1-sr1acc01 Te0/10 | ● | tk1-svr108 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-766 |
| tk1-sr1acc01 Te0/3 | ● | tk1-svr101 eth1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-767 |
| tk1-core02 Te0/7 | ● | tk1-fnacc02 Te0/1 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-768 |
| tk1-fnacc02 Gi0/1 | — | tk1-f6ap02 Gi0/1 | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-79 |
| os1-fw01 Te0/1 | ● | 回線終端装置  | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-92 |
| os1-rt01 Gi0/1 | — | 回線終端装置  | — | 1000BASE-T Cat6a | — / — | 9BYiFAK1cGA9hBdD1Cum-97 |
| os1-core02 Te0/4 | ● | os1-svr102 eth2 | ● | 10GBASE-SR OM3 | — / — | 9BYiFAK1cGA9hBdD1Cum-758 |

### 2.3 ポート所属表

FW側はタグなしEXTのBVIメンバー。専用Mgmt IFのVLAN9は対向管理SW側で収容します。

| 機器 | 図のポート | モード | 所属VLAN | 根拠 | cell id |
| --- | --- | --- | --- | --- | --- |
| os1-core01 | Po1 | trunk | 9,10,11,300-399 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-124 |
| os1-core01 | Te0/1 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-111 |
| os1-core01 | Te0/2 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-113 |
| os1-core01 | Te0/3 | trunk | 10,11 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-164 |
| os1-core01 | Te0/4 | trunk | 10,11 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-166 |
| os1-core01 | Te0/5 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-168 |
| os1-core01 | Te0/23 | trunk | 9,10,11,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-109 |
| os1-core01 | Te0/24 | trunk | 9,10,11,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-107 |
| os1-core02 | Gi0/1 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-116 |
| os1-core02 | Po1 | trunk | 9,10,11,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-594 |
| os1-core02 | Te0/1 | access | 2 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-117 |
| os1-core02 | Te0/2 | access | 2 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-118 |
| os1-core02 | Te0/3 | trunk | 10,11 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-114 |
| os1-core02 | Te0/4 | trunk | 10,11 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-115 |
| os1-core02 | Te0/23 | trunk | 9,10,11,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-592 |
| os1-core02 | Te0/24 | trunk | 9,10,11,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-593 |
| os1-fmacc01 | Gi0/1 | access | \<TBD:VLAN_OFFICE_OS_FM> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-506 |
| os1-fmacc01 | Gi0/21 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-602 |
| os1-fmacc01 | Gi0/23 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-509 |
| os1-fmacc01 | Gi0/24 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-508 |
| os1-fmacc01 | Gi0/3-20 | access | \<TBD:VLAN_OFFICE_OS_FM> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-526 |
| os1-fmacc01 | Po1 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-533 |
| os1-fmacc01 | Te0/1 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-510 |
| os1-fmacc02 | Gi0/1 | access | \<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-512 |
| os1-fmacc02 | Gi0/21 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-603 |
| os1-fmacc02 | Gi0/23 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-540 |
| os1-fmacc02 | Gi0/24 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-541 |
| os1-fmacc02 | Gi0/3-20 | access | \<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-529 |
| os1-fmacc02 | Po1 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-542 |
| os1-fmacc02 | Te0/1 | trunk | 9,\<TBD:VLAN_OFFICE_OS_FM> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-513 |
| os1-fw01 | Te0/2 | bridge-group 2 | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-91 |
| os1-fw01 | Te0/3 | bridge-group 2 | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-100 |
| os1-rt01 | Gi0/2 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-96 |
| os1-rt01 | Gi0/3 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-102 |
| tk1-core01 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-201 |
| tk1-core01 | Po1 | trunk | 2,10,11,100-199,200-299,300-399 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-198 |
| tk1-core01 | Po2 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-300 |
| tk1-core01 | Po3 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-302 |
| tk1-core01 | Te0/1 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-21 |
| tk1-core01 | Te0/2 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-23 |
| tk1-core01 | Te0/3 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-217 |
| tk1-core01 | Te0/4 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-218 |
| tk1-core01 | Te0/5 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-222 |
| tk1-core01 | Te0/6 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-223 |
| tk1-core01 | Te0/7 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-83 |
| tk1-core01 | Te0/22 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-351 |
| tk1-core01 | Te0/23 | trunk | 2,10,11,100-199,200-299,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-187 |
| tk1-core01 | Te0/24 | trunk | 2,10,11,100-199,200-299,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-185 |
| tk1-core02 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-346 |
| tk1-core02 | Po1 | trunk | 2,10,11,100-199,200-299,300-399 | 対称性、Poまたは対向から継承 | — |
| tk1-core02 | Po2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-454 |
| tk1-core02 | Po3 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-455 |
| tk1-core02 | Te0/1 | access | 2 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-28 |
| tk1-core02 | Te0/2 | access | 2 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-29 |
| tk1-core02 | Te0/3 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-24 |
| tk1-core02 | Te0/4 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-25 |
| tk1-core02 | Te0/5 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-26 |
| tk1-core02 | Te0/6 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-27 |
| tk1-core02 | Te0/7 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-84 |
| tk1-core02 | Te0/22 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-358 |
| tk1-core02 | Te0/23 | trunk | 2,10,11,100-199,200-299,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-467 |
| tk1-core02 | Te0/24 | trunk | 2,10,11,100-199,200-299,300-399 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-466 |
| tk1-fnacc01 | Gi0/1 | access | \<TBD:VLAN_OFFICE_TK_F6> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-73 |
| tk1-fnacc01 | Gi0/23 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-76 |
| tk1-fnacc01 | Gi0/24 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-75 |
| tk1-fnacc01 | Gi0/3-20 | access | \<TBD:VLAN_OFFICE_TK_F6> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-384 |
| tk1-fnacc01 | Po1 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-489 |
| tk1-fnacc01 | Te0/1 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-77 |
| tk1-fnacc02 | Gi0/1 | access | \<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-80 |
| tk1-fnacc02 | Gi0/23 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-496 |
| tk1-fnacc02 | Gi0/24 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-497 |
| tk1-fnacc02 | Gi0/3-20 | access | \<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-387 |
| tk1-fnacc02 | Po1 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-498 |
| tk1-fnacc02 | Te0/1 | trunk | 9,\<TBD:VLAN_OFFICE_TK_F6> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-81 |
| tk1-fw01 | Te0/2 | bridge-group 2 | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-49 |
| tk1-fw01 | Te0/3 | bridge-group 2 | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-67 |
| tk1-mgmt01 | Gi0/1 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-321 |
| tk1-mgmt01 | Gi0/2 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-344 |
| tk1-mgmt01 | Gi0/3 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-342 |
| tk1-mgmt01 | Gi0/4 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-478 |
| tk1-mgmt01 | Gi0/5 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-312 |
| tk1-mgmt01 | Gi0/6 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-317 |
| tk1-mgmt01 | Gi0/12 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-319 |
| tk1-mgmt01 | Gi0/47 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-335 |
| tk1-mgmt01 | Gi0/48 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-333 |
| tk1-mgmt01 | Po1 | access | 9 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-337 |
| tk1-mgmt02 | Gi0/1 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-349 |
| tk1-mgmt02 | Gi0/2 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-348 |
| tk1-mgmt02 | Gi0/3 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-325 |
| tk1-mgmt02 | Gi0/4 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-326 |
| tk1-mgmt02 | Gi0/5 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-322 |
| tk1-mgmt02 | Gi0/6 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-323 |
| tk1-mgmt02 | Gi0/12 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-324 |
| tk1-mgmt02 | Gi0/47 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-479 |
| tk1-mgmt02 | Gi0/48 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-480 |
| tk1-mgmt02 | Po1 | access | 9 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-481 |
| tk1-rt01 | Gi0/2 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-63 |
| tk1-rt01 | Gi0/3 | access | 2 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-69 |
| tk1-sr1acc01 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-340 |
| tk1-sr1acc01 | Po1 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-238 |
| tk1-sr1acc01 | Po2 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-301 |
| tk1-sr1acc01 | Te0/1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-35 |
| tk1-sr1acc01 | Te0/2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-37 |
| tk1-sr1acc01 | Te0/3 | trunk | 10,11 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-255 |
| tk1-sr1acc01 | Te0/4 | trunk | \<TBD:PROD_VLAN_LIST_TK1_SVR102> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-257 |
| tk1-sr1acc01 | Te0/10 | trunk | 200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-259 |
| tk1-sr1acc01 | Te0/23 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-237 |
| tk1-sr1acc01 | Te0/24 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-236 |
| tk1-sr1acc02 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-314 |
| tk1-sr1acc02 | Po1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-390 |
| tk1-sr1acc02 | Po2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-391 |
| tk1-sr1acc02 | Te0/1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-42 |
| tk1-sr1acc02 | Te0/2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-44 |
| tk1-sr1acc02 | Te0/3 | trunk | 10,11 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-38 |
| tk1-sr1acc02 | Te0/4 | trunk | \<TBD:PROD_VLAN_LIST_TK1_SVR102> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-39 |
| tk1-sr1acc02 | Te0/10 | trunk | 200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-40 |
| tk1-sr1acc02 | Te0/23 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-388 |
| tk1-sr1acc02 | Te0/24 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-389 |
| tk1-sr2acc01 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-441 |
| tk1-sr2acc01 | Po1 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-412 |
| tk1-sr2acc01 | Po2 | trunk | 10,11,100-199,200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-436 |
| tk1-sr2acc01 | Te0/1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-398 |
| tk1-sr2acc01 | Te0/2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-400 |
| tk1-sr2acc01 | Te0/3 | trunk | 10,11 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-430 |
| tk1-sr2acc01 | Te0/4 | trunk | \<TBD:PROD_VLAN_LIST_TK1_SVR202> | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-432 |
| tk1-sr2acc01 | Te0/10 | trunk | 200-299 | 図の横線 | 9BYiFAK1cGA9hBdD1Cum-434 |
| tk1-sr2acc01 | Te0/23 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-411 |
| tk1-sr2acc01 | Te0/24 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-410 |
| tk1-sr2acc02 | Mgmt | L3 / Mgmt-vrf | 9 | Mgmtケーブル | 9BYiFAK1cGA9hBdD1Cum-437 |
| tk1-sr2acc02 | Po1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-445 |
| tk1-sr2acc02 | Po2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-446 |
| tk1-sr2acc02 | Te0/1 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-404 |
| tk1-sr2acc02 | Te0/2 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-405 |
| tk1-sr2acc02 | Te0/3 | trunk | 10,11 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-401 |
| tk1-sr2acc02 | Te0/4 | trunk | \<TBD:PROD_VLAN_LIST_TK1_SVR202> | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-402 |
| tk1-sr2acc02 | Te0/10 | trunk | 200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-403 |
| tk1-sr2acc02 | Te0/23 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-443 |
| tk1-sr2acc02 | Te0/24 | trunk | 10,11,100-199,200-299 | 対称性、Poまたは対向から継承 | 9BYiFAK1cGA9hBdD1Cum-444 |

### 2.4 経路

自拠点・対向拠点の宛先はセグメントの最小共通プレフィックスから東京172.17.0.0/16、大阪172.18.0.0/16と推定しました。

| 設定機器 | 宛先 | next-hop | 根拠 |
| --- | --- | --- | --- |
| 各拠点コア | default／対向拠点 /16 | 同拠点FWのEXT .1／同拠点RTのEXT .2 | 論理図 |
| 各拠点RT | 自拠点 /16／対向拠点 /16 | 自拠点コアEXT VIP .6／対向RTの拠点間IP | 論理図 |
| 各拠点FW | default／自拠点 /16 | ローカルISP GW／自拠点コアEXT VIP .6 | 論理図、大阪のdefault終点は要確認 |
| 東京OOB・管理SW・フロアSW | 管理default | VLAN9 VIP .3 | 既定値 |

## 3. 機器別コンフィグと設定根拠

### os1-core01

[os1-core01.cfg](os1-core01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-core01
!
ip routing
spanning-tree mode rapid-pvst
fhrp version vrrp v3
spanning-tree vlan 2,9-11,300-399 root primary
!
vlan 2
 name EXT
!
vlan 9
 name MGMT
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 300-399
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.18.0.4 255.255.255.224
 no shutdown
 vrrp 2 address-family ipv4
  address 172.18.0.6 primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-001 verify values in conversion report
interface Vlan9
 ip address 172.18.1.1 255.255.255.0
 no shutdown
 vrrp 9 address-family ipv4
  address 172.18.1.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
interface Vlan10
 ip address 172.18.2.1 255.255.255.0
 no shutdown
 vrrp 10 address-family ipv4
  address 172.18.2.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
interface Vlan11
 ip address 172.18.3.1 255.255.255.0
 no shutdown
 vrrp 11 address-family ipv4
  address 172.18.3.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-011 verify values in conversion report
interface Vlan<TBD:OFFICE_VLAN_ID>
 ip address <TBD:OFFICE_LOCAL_IP_1> 255.255.255.0
 no shutdown
 ip helper-address <TBD:OFFICE_DHCP_SERVER>
 vrrp <TBD:OFFICE_VRID> address-family ipv4
  address <TBD:OFFICE_VIP> primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to os1-core02 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 no shutdown
!
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/1
 description to os1-fw01 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/2
 description to os1-rt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
interface TenGigabitEthernet0/3
 description to os1-svr101 eth1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/4
 description to os1-svr102 eth1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/5
 description to os1-fmacc01 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
interface TenGigabitEthernet0/23
 description to os1-core02 Te0/23 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to os1-core02 Te0/24 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 channel-group 1 mode active
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 172.18.0.1
ip route 172.17.0.0 255.255.0.0 172.18.0.2
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-core01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-162 | — |
| 4 | ip routing | 【図】GRT | 9BYiFAK1cGA9hBdD1Cum-122 | — |
| 5 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-162 | — |
| 6 | fhrp version vrrp v3 | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 7 | spanning-tree vlan 2,9-11,300-399 root primary | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 9 | vlan 2 | 【図】セグメントラベル | — | — |
| 10 | name EXT | 【図】セグメントラベル | — | — |
| 12 | vlan 9 | 【図】セグメントラベル | — | — |
| 13 | name MGMT | 【図】セグメントラベル | — | — |
| 15 | vlan 10 | 【図】セグメントラベル | — | — |
| 16 | name DMZ | 【図】セグメントラベル | — | — |
| 18 | vlan 11 | 【図】セグメントラベル | — | — |
| 19 | name COMMON | 【図】セグメントラベル | — | — |
| 21 | vlan 300-399 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 24 | interface Vlan2 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 25 | ip address 172.18.0.4 255.255.255.224 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 26 | no shutdown | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 27 | vrrp 2 address-family ipv4 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 28 | address 172.18.0.6 primary | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 29 | priority 110 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 30 | preempt delay minimum 0 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 31 | exit | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-122 | R-009 |
| 34 | interface Vlan9 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 35 | ip address 172.18.1.1 255.255.255.0 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 36 | no shutdown | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 37 | vrrp 9 address-family ipv4 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 38 | address 172.18.1.3 primary | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 39 | priority 110 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 40 | preempt delay minimum 0 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 41 | exit | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 43 | interface Vlan10 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 44 | ip address 172.18.2.1 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 45 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 46 | vrrp 10 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 47 | address 172.18.2.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 48 | priority 110 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 49 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 50 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 52 | interface Vlan11 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 53 | ip address 172.18.3.1 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 54 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 55 | vrrp 11 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 56 | address 172.18.3.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 57 | priority 110 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 58 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 59 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 62 | interface Vlan\<TBD:OFFICE_VLAN_ID> | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 63 | ip address \<TBD:OFFICE_LOCAL_IP_1> 255.255.255.0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 64 | no shutdown | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 65 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | 【論・推測】DHCPサーバーとオフィス端末 | J5z6EYH7W0RdXeQXPurJ-87 | — |
| 66 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 67 | address \<TBD:OFFICE_VIP> primary | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 68 | priority 110 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 69 | preempt delay minimum 0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 70 | exit | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 73 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-124, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 74 | description to os1-core02 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-124, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 75 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-124, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 76 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-124, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 77 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-124, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 80 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 81 | description to os1-fw01 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 82 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 83 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 84 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 85 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-111, 9BYiFAK1cGA9hBdD1Cum-580 | — |
| 89 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 90 | description to os1-rt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 91 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 92 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 93 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 94 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-113, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 96 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 97 | description to os1-svr101 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 98 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 99 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 100 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 101 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 102 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-164, 9BYiFAK1cGA9hBdD1Cum-760 | — |
| 104 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 105 | description to os1-svr102 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 106 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 107 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 108 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 109 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 110 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-166, 9BYiFAK1cGA9hBdD1Cum-757 | — |
| 112 | interface TenGigabitEthernet0/5 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 113 | description to os1-fmacc01 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 114 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 115 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 116 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 117 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-168, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 119 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 120 | description to os1-core02 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 121 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 122 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 123 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 124 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 125 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-109, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 127 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 128 | description to os1-core02 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 129 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 130 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 131 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 132 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 133 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-107, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 135 | ip route 0.0.0.0 0.0.0.0 172.18.0.1 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-53, J5z6EYH7W0RdXeQXPurJ-105 | — |
| 136 | ip route 172.17.0.0 255.255.0.0 172.18.0.2 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-53, J5z6EYH7W0RdXeQXPurJ-105 | — |
| 140 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### os1-core02

[os1-core02.cfg](os1-core02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-core02
!
ip routing
spanning-tree mode rapid-pvst
fhrp version vrrp v3
spanning-tree vlan 2,9-11,300-399 root secondary
!
vlan 2
 name EXT
!
vlan 9
 name MGMT
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 300-399
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.18.0.5 255.255.255.224
 no shutdown
 vrrp 2 address-family ipv4
  address 172.18.0.6 primary
  preempt delay minimum 0
 exit
!
! WARN R-001 verify values in conversion report
interface Vlan9
 ip address 172.18.1.2 255.255.255.0
 no shutdown
 vrrp 9 address-family ipv4
  address 172.18.1.3 primary
  preempt delay minimum 0
 exit
!
interface Vlan10
 ip address 172.18.2.2 255.255.255.0
 no shutdown
 vrrp 10 address-family ipv4
  address 172.18.2.3 primary
  preempt delay minimum 0
 exit
!
interface Vlan11
 ip address 172.18.3.2 255.255.255.0
 no shutdown
 vrrp 11 address-family ipv4
  address 172.18.3.3 primary
  preempt delay minimum 0
 exit
!
! WARN R-011 verify values in conversion report
interface Vlan<TBD:OFFICE_VLAN_ID>
 ip address <TBD:OFFICE_LOCAL_IP_2> 255.255.255.0
 no shutdown
 ip helper-address <TBD:OFFICE_DHCP_SERVER>
 vrrp <TBD:OFFICE_VRID> address-family ipv4
  address <TBD:OFFICE_VIP> primary
  preempt delay minimum 0
 exit
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to os1-core01 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 no shutdown
!
! WARN R-003 drawing Gi0/1 versus 10GBASE-SR
interface GigabitEthernet0/1
 description to os1-fmacc02 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/1
 description to os1-fw01 Te0/3 [10GBASE-SR OM3]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/2
 description to os1-rt01 Gi0/3 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
interface TenGigabitEthernet0/3
 description to os1-svr101 eth2 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
! WARN R-004 remote port inferred
interface TenGigabitEthernet0/4
 description to os1-svr102 eth2 [10GBASE-SR OM3] (inferred)
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/23
 description to os1-core01 Te0/23 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to os1-core01 Te0/24 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,10,11,300-399
 channel-group 1 mode active
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 172.18.0.1
ip route 172.17.0.0 255.255.0.0 172.18.0.2
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-core02 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-142 | — |
| 4 | ip routing | 【図】GRT | Rl40HBUQi0JMIVKS_C4F-18 | — |
| 5 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-142 | — |
| 6 | fhrp version vrrp v3 | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 7 | spanning-tree vlan 2,9-11,300-399 root secondary | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 9 | vlan 2 | 【図】セグメントラベル | — | — |
| 10 | name EXT | 【図】セグメントラベル | — | — |
| 12 | vlan 9 | 【図】セグメントラベル | — | — |
| 13 | name MGMT | 【図】セグメントラベル | — | — |
| 15 | vlan 10 | 【図】セグメントラベル | — | — |
| 16 | name DMZ | 【図】セグメントラベル | — | — |
| 18 | vlan 11 | 【図】セグメントラベル | — | — |
| 19 | name COMMON | 【図】セグメントラベル | — | — |
| 21 | vlan 300-399 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 24 | interface Vlan2 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 25 | ip address 172.18.0.5 255.255.255.224 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 26 | no shutdown | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 27 | vrrp 2 address-family ipv4 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 28 | address 172.18.0.6 primary | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 29 | preempt delay minimum 0 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 30 | exit | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-150, Rl40HBUQi0JMIVKS_C4F-18 | R-009 |
| 33 | interface Vlan9 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 34 | ip address 172.18.1.2 255.255.255.0 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 35 | no shutdown | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 36 | vrrp 9 address-family ipv4 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 37 | address 172.18.1.3 primary | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 38 | preempt delay minimum 0 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 39 | exit | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-645 | R-001 |
| 41 | interface Vlan10 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 42 | ip address 172.18.2.2 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 43 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 44 | vrrp 10 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 45 | address 172.18.2.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 46 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 47 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-169 | — |
| 49 | interface Vlan11 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 50 | ip address 172.18.3.2 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 51 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 52 | vrrp 11 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 53 | address 172.18.3.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 54 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 55 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-170 | — |
| 58 | interface Vlan\<TBD:OFFICE_VLAN_ID> | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 59 | ip address \<TBD:OFFICE_LOCAL_IP_2> 255.255.255.0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 60 | no shutdown | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 61 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | 【論・推測】DHCPサーバーとオフィス端末 | J5z6EYH7W0RdXeQXPurJ-87 | — |
| 62 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 63 | address \<TBD:OFFICE_VIP> primary | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 64 | preempt delay minimum 0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 65 | exit | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-171 | R-011 |
| 68 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-594, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 69 | description to os1-core01 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-594, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 70 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-594, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 71 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-594, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 72 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-594, 9BYiFAK1cGA9hBdD1Cum-108, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 75 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 76 | description to os1-fmacc02 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 77 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 78 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 79 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 80 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-116, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 83 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 84 | description to os1-fw01 Te0/3 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 85 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 86 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 87 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 88 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-117, 9BYiFAK1cGA9hBdD1Cum-755 | — |
| 92 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 93 | description to os1-rt01 Gi0/3 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 94 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 95 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 96 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 97 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-118, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 99 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 100 | description to os1-svr101 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 101 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 102 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 103 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 104 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 105 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-114, 9BYiFAK1cGA9hBdD1Cum-761 | — |
| 108 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 109 | description to os1-svr102 eth2 [10GBASE-SR OM3] (inferred) | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 110 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 111 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 112 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 113 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 114 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-115, 9BYiFAK1cGA9hBdD1Cum-758 | — |
| 116 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 117 | description to os1-core01 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 118 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 119 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 120 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 121 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 122 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-592, 9BYiFAK1cGA9hBdD1Cum-108 | — |
| 124 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 125 | description to os1-core01 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 126 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 127 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 128 | switchport trunk allowed vlan 9,10,11,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 129 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 130 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-593, 9BYiFAK1cGA9hBdD1Cum-106 | — |
| 132 | ip route 0.0.0.0 0.0.0.0 172.18.0.1 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-53, J5z6EYH7W0RdXeQXPurJ-105 | — |
| 133 | ip route 172.17.0.0 255.255.0.0 172.18.0.2 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-53, J5z6EYH7W0RdXeQXPurJ-105 | — |
| 137 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### os1-fmacc01

[os1-fmacc01.cfg](os1-fmacc01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-fmacc01
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
vlan <TBD:VLAN_OFFICE_OS_FM>
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to os1-fmacc02 Gi0/23,Gi0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
interface GigabitEthernet0/1
 description to os1-fmap01 Gi0/1 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_OS_FM>
 spanning-tree portfast
 power inline auto
 no shutdown
!
interface GigabitEthernet0/2
 description Reserved PoE
 shutdown
!
interface GigabitEthernet0/21
 description to os1-svr101 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/23
 description to os1-fmacc02 Gi0/23 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/24
 description to os1-fmacc02 Gi0/24 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 channel-group 1 mode active
 no shutdown
!
interface range GigabitEthernet0/3 - 20
 description to office endpoints [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_OS_FM>
 spanning-tree portfast
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/1
 description to os1-core01 Te0/5 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
ip default-gateway 172.18.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-fmacc01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-521 | — |
| 4 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-521 | — |
| 6 | vlan 9 | 【図】セグメントラベル | — | — |
| 7 | name MGMT | 【図】セグメントラベル | — | — |
| 9 | vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 11 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-521 | — |
| 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-521 | — |
| 13 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-521 | — |
| 16 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-533, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 17 | description to os1-fmacc02 Gi0/23,Gi0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-533, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 18 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-533, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-533, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 20 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-533, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 22 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 23 | description to os1-fmap01 Gi0/1 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 24 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 25 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 26 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 27 | power inline auto | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 28 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-506, 9BYiFAK1cGA9hBdD1Cum-507 | — |
| 30 | interface GigabitEthernet0/2 | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-596 | — |
| 31 | description Reserved PoE | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-596 | — |
| 32 | shutdown | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-596 | — |
| 34 | interface GigabitEthernet0/21 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 35 | description to os1-svr101 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 36 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 37 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 38 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-602, 9BYiFAK1cGA9hBdD1Cum-604 | — |
| 41 | interface GigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 42 | description to os1-fmacc02 Gi0/23 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 43 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 45 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-509, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 48 | interface GigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 49 | description to os1-fmacc02 Gi0/24 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 50 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 51 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 52 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-508, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 55 | interface range GigabitEthernet0/3 - 20 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 56 | description to office endpoints [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 57 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 58 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 59 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-526, 9BYiFAK1cGA9hBdD1Cum-527 | — |
| 63 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-510, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 64 | description to os1-core01 Te0/5 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-510, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 65 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-510, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 66 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-510, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 67 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-510, 9BYiFAK1cGA9hBdD1Cum-759 | — |
| 69 | ip default-gateway 172.18.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 73 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### os1-fmacc02

[os1-fmacc02.cfg](os1-fmacc02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-fmacc02
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
vlan <TBD:VLAN_OFFICE_OS_FM>
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to os1-fmacc01 Gi0/23,Gi0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
interface GigabitEthernet0/1
 description to os1-fmap02 Gi0/1 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_OS_FM>
 spanning-tree portfast
 power inline auto
 no shutdown
!
interface GigabitEthernet0/2
 description Reserved PoE
 shutdown
!
interface GigabitEthernet0/21
 description to os1-svr102 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/23
 description to os1-fmacc01 Gi0/23 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/24
 description to os1-fmacc01 Gi0/24 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 channel-group 1 mode active
 no shutdown
!
interface range GigabitEthernet0/3 - 20
 description to office endpoints [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_OS_FM>
 spanning-tree portfast
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/1
 description to os1-core02 Gi0/1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_OS_FM>
 no shutdown
!
ip default-gateway 172.18.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-fmacc02 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-581 | — |
| 4 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-581 | — |
| 6 | vlan 9 | 【図】セグメントラベル | — | — |
| 7 | name MGMT | 【図】セグメントラベル | — | — |
| 9 | vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 11 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-581 | — |
| 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-581 | — |
| 13 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-581 | — |
| 16 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-542, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 17 | description to os1-fmacc01 Gi0/23,Gi0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-542, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 18 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-542, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-542, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 20 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-542, 9BYiFAK1cGA9hBdD1Cum-543, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 22 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 23 | description to os1-fmap02 Gi0/1 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 24 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 25 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 26 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 27 | power inline auto | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 28 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-512, 9BYiFAK1cGA9hBdD1Cum-511 | — |
| 30 | interface GigabitEthernet0/2 | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-597 | — |
| 31 | description Reserved PoE | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-597 | — |
| 32 | shutdown | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-597 | — |
| 34 | interface GigabitEthernet0/21 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 35 | description to os1-svr102 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 36 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 37 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 38 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-603, 9BYiFAK1cGA9hBdD1Cum-605 | — |
| 41 | interface GigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 42 | description to os1-fmacc01 Gi0/23 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 43 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 45 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-540, 9BYiFAK1cGA9hBdD1Cum-543 | — |
| 48 | interface GigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 49 | description to os1-fmacc01 Gi0/24 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 50 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 51 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 52 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-541, 9BYiFAK1cGA9hBdD1Cum-544 | — |
| 55 | interface range GigabitEthernet0/3 - 20 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 56 | description to office endpoints [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 57 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 58 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 59 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-529, 9BYiFAK1cGA9hBdD1Cum-528 | — |
| 63 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-513, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 64 | description to os1-core02 Gi0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-513, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 65 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-513, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 66 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-513, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 67 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-513, 9BYiFAK1cGA9hBdD1Cum-582 | — |
| 69 | ip default-gateway 172.18.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 73 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### os1-fw01

[os1-fw01.cfg](os1-fw01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-fw01
!
! Expected firewall mode: routed
interface TenGigabitEthernet0/1
 description to carrier handoff [10GBASE-SR OM3]
 nameif outside
 security-level 0
 ip address <TBD:OUTSIDE_IP_203.0.113.0_25> 255.255.255.128
 no shutdown
!
! WARN R-009 EXT L2 forwarding and BPDU transport
interface TenGigabitEthernet0/2
 description to os1-core01 Te0/1 [10GBASE-SR OM3]
 nameif ext_core01
 security-level 100
 bridge-group 2
 no shutdown
!
! WARN R-009 EXT L2 forwarding and BPDU transport
interface TenGigabitEthernet0/3
 description to os1-core02 Te0/1 [10GBASE-SR OM3]
 nameif ext_core02
 security-level 100
 bridge-group 2
 no shutdown
!
interface BVI2
 nameif ext
 security-level 100
 ip address 172.18.0.1 255.255.255.224
 no shutdown
!
same-security-traffic permit inter-interface
! WARN R-013 verify that ISP next hop is on the local outside subnet
route outside 0.0.0.0 0.0.0.0 <TBD:LOCAL_ISP_GATEWAY> 1
route ext 172.18.0.0 255.255.0.0 172.18.0.6 1
nat (<TBD:NAT_INGRESS_IF>,outside) source dynamic <TBD:NAT_SOURCE_OBJECT> <TBD:NAT_TRANSLATED_TARGET>
access-list <TBD:ACL_NAME> extended <TBD:ACL_RULE>
access-group <TBD:ACL_NAME> in interface <TBD:ACL_INGRESS_IF>
!
! Management services: populate after approval of the management plan
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-fw01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-143 | — |
| 5 | interface TenGigabitEthernet0/1 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 6 | description to carrier handoff [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 7 | nameif outside | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 8 | security-level 0 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 9 | ip address \<TBD:OUTSIDE_IP_203.0.113.0_25> 255.255.255.128 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 10 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-92, 9BYiFAK1cGA9hBdD1Cum-94 | — |
| 13 | interface TenGigabitEthernet0/2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 14 | description to os1-core01 Te0/1 [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 15 | nameif ext_core01 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 16 | security-level 100 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 17 | bridge-group 2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 18 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-580, 9BYiFAK1cGA9hBdD1Cum-91 | — |
| 21 | interface TenGigabitEthernet0/3 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 22 | description to os1-core02 Te0/1 [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 23 | nameif ext_core02 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 24 | security-level 100 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 25 | bridge-group 2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 26 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-755, 9BYiFAK1cGA9hBdD1Cum-100 | — |
| 28 | interface BVI2 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 29 | nameif ext | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 30 | security-level 100 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 31 | ip address 172.18.0.1 255.255.255.224 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 32 | no shutdown | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 34 | same-security-traffic permit inter-interface | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-150 | R-009 |
| 36 | route outside 0.0.0.0 0.0.0.0 \<TBD:LOCAL_ISP_GATEWAY> 1 | 【論】defaultと自拠点経路の矢印／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-139, J5z6EYH7W0RdXeQXPurJ-141 | R-013 |
| 37 | route ext 172.18.0.0 255.255.0.0 172.18.0.6 1 | 【論】defaultと自拠点経路の矢印／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-139, J5z6EYH7W0RdXeQXPurJ-141 | R-013 |
| 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 43 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### os1-rt01

[os1-rt01.cfg](os1-rt01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname os1-rt01
!
ip routing
spanning-tree mode rapid-pvst
!
vlan 2
 name EXT
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.18.0.2 255.255.255.224
 no shutdown
!
interface GigabitEthernet0/1
 description to interbuilding carrier handoff [1000BASE-T Cat6a]
 ip address <TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface GigabitEthernet0/2
 description to os1-core01 Te0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface GigabitEthernet0/3
 description to os1-core02 Te0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 2
 no shutdown
!
ip route 172.18.0.0 255.255.0.0 172.18.0.6
ip route 172.17.0.0 255.255.0.0 <TBD:INTER_BLDG_REMOTE_RT_IP>
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname os1-rt01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-144 | — |
| 4 | ip routing | 【図】GRT | 9BYiFAK1cGA9hBdD1Cum-636 | — |
| 5 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-144 | — |
| 7 | vlan 2 | 【図】セグメントラベル | — | — |
| 8 | name EXT | 【図】セグメントラベル | — | — |
| 11 | interface Vlan2 | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-636 | R-009 |
| 12 | ip address 172.18.0.2 255.255.255.224 | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-636 | R-009 |
| 13 | no shutdown | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-150, 9BYiFAK1cGA9hBdD1Cum-636 | R-009 |
| 15 | interface GigabitEthernet0/1 | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-97, 9BYiFAK1cGA9hBdD1Cum-634 | — |
| 16 | description to interbuilding carrier handoff [1000BASE-T Cat6a] | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-97, 9BYiFAK1cGA9hBdD1Cum-634 | — |
| 17 | ip address \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0 | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-97, 9BYiFAK1cGA9hBdD1Cum-634 | — |
| 18 | no shutdown | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-97, 9BYiFAK1cGA9hBdD1Cum-634 | — |
| 22 | interface GigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-96, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 23 | description to os1-core01 Te0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-96, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 24 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-96, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 25 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-96, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 26 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-96, 9BYiFAK1cGA9hBdD1Cum-754 | — |
| 30 | interface GigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-102, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 31 | description to os1-core02 Te0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-102, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 32 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-102, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 33 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-102, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 34 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-102, 9BYiFAK1cGA9hBdD1Cum-101 | — |
| 36 | ip route 172.18.0.0 255.255.0.0 172.18.0.6 | 【論】自拠点と対向拠点への経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-143, J5z6EYH7W0RdXeQXPurJ-133 | R-013 |
| 37 | ip route 172.17.0.0 255.255.0.0 \<TBD:INTER_BLDG_REMOTE_RT_IP> | 【論】自拠点と対向拠点への経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-143, J5z6EYH7W0RdXeQXPurJ-133 | R-013 |
| 41 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-core01

[tk1-core01.cfg](tk1-core01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-core01
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
ip routing
spanning-tree mode rapid-pvst
fhrp version vrrp v3
spanning-tree vlan 2,9-11,100-399 root primary
!
vlan 2
 name EXT
!
vlan 9
 name MGMT
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
vlan 300-399
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.17.0.4 255.255.255.224
 no shutdown
 vrrp 2 address-family ipv4
  address 172.17.0.6 primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-001 verify values in conversion report
interface Vlan9
 ip address 172.17.1.1 255.255.255.0
 no shutdown
 vrrp 9 address-family ipv4
  address 172.17.1.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
interface Vlan10
 ip address 172.17.2.1 255.255.255.0
 no shutdown
 vrrp 10 address-family ipv4
  address 172.17.2.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
interface Vlan11
 ip address 172.17.3.1 255.255.255.0
 no shutdown
 vrrp 11 address-family ipv4
  address 172.17.3.3 primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-012 verify values in conversion report
interface Vlan<TBD:PROD_VLAN_ID>
 ip address <TBD:PROD_LOCAL_IP_1> <TBD:PROD_MASK>
 no shutdown
 vrrp <TBD:PROD_VRID> address-family ipv4
  address <TBD:PROD_VIP> primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-012 verify values in conversion report
interface Vlan<TBD:DEV_VLAN_ID>
 ip address <TBD:DEV_LOCAL_IP_1> <TBD:DEV_MASK>
 no shutdown
 vrrp <TBD:DEV_VRID> address-family ipv4
  address <TBD:DEV_VIP> primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-011 verify values in conversion report
interface Vlan<TBD:OFFICE_VLAN_ID>
 ip address <TBD:OFFICE_LOCAL_IP_1> 255.255.255.0
 no shutdown
 ip helper-address <TBD:OFFICE_DHCP_SERVER>
 vrrp <TBD:OFFICE_VRID> address-family ipv4
  address <TBD:OFFICE_VIP> primary
  priority 110
  preempt delay minimum 0
 exit
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-core02 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-sr1acc01 Te0/1,Te0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel3
 description to tk1-sr2acc01 Te0/1,Te0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/1
 description to tk1-fw01 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/2
 description to tk1-rt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-sr1acc01 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-sr1acc01 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/5
 description to tk1-sr2acc01 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 3 mode active
 no shutdown
!
interface TenGigabitEthernet0/6
 description to tk1-sr2acc01 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 3 mode active
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/7
 description to tk1-fnacc01 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/22
 description to tk1-mgmt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-core02 Te0/23 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-core02 Te0/24 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt01 Gi0/1
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 172.17.0.1
ip route 172.18.0.0 255.255.0.0 172.17.0.2
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-core01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-148 | — |
| 4 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-201 | — |
| 5 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-201 | — |
| 6 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-201 | — |
| 8 | ip routing | 【図】GRT | 9BYiFAK1cGA9hBdD1Cum-196 | — |
| 9 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-148 | — |
| 10 | fhrp version vrrp v3 | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 11 | spanning-tree vlan 2,9-11,100-399 root primary | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 13 | vlan 2 | 【図】セグメントラベル | — | — |
| 14 | name EXT | 【図】セグメントラベル | — | — |
| 16 | vlan 9 | 【図】セグメントラベル | — | — |
| 17 | name MGMT | 【図】セグメントラベル | — | — |
| 19 | vlan 10 | 【図】セグメントラベル | — | — |
| 20 | name DMZ | 【図】セグメントラベル | — | — |
| 22 | vlan 11 | 【図】セグメントラベル | — | — |
| 23 | name COMMON | 【図】セグメントラベル | — | — |
| 25 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 27 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 29 | vlan 300-399 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 32 | interface Vlan2 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 33 | ip address 172.17.0.4 255.255.255.224 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 34 | no shutdown | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 35 | vrrp 2 address-family ipv4 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 36 | address 172.17.0.6 primary | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 37 | priority 110 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 38 | preempt delay minimum 0 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 39 | exit | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-196 | R-009 |
| 42 | interface Vlan9 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 43 | ip address 172.17.1.1 255.255.255.0 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 44 | no shutdown | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 45 | vrrp 9 address-family ipv4 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 46 | address 172.17.1.3 primary | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 47 | priority 110 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 48 | preempt delay minimum 0 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 49 | exit | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 51 | interface Vlan10 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 52 | ip address 172.17.2.1 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 53 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 54 | vrrp 10 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 55 | address 172.17.2.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 56 | priority 110 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 57 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 58 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 60 | interface Vlan11 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 61 | ip address 172.17.3.1 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 62 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 63 | vrrp 11 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 64 | address 172.17.3.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 65 | priority 110 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 66 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 67 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 70 | interface Vlan\<TBD:PROD_VLAN_ID> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 71 | ip address \<TBD:PROD_LOCAL_IP_1> \<TBD:PROD_MASK> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 72 | no shutdown | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 73 | vrrp \<TBD:PROD_VRID> address-family ipv4 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 74 | address \<TBD:PROD_VIP> primary | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 75 | priority 110 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 76 | preempt delay minimum 0 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 77 | exit | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 80 | interface Vlan\<TBD:DEV_VLAN_ID> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 81 | ip address \<TBD:DEV_LOCAL_IP_1> \<TBD:DEV_MASK> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 82 | no shutdown | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 83 | vrrp \<TBD:DEV_VRID> address-family ipv4 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 84 | address \<TBD:DEV_VIP> primary | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 85 | priority 110 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 86 | preempt delay minimum 0 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 87 | exit | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 90 | interface Vlan\<TBD:OFFICE_VLAN_ID> | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 91 | ip address \<TBD:OFFICE_LOCAL_IP_1> 255.255.255.0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 92 | no shutdown | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 93 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | 【論・推測】DHCPサーバーとオフィス端末 | J5z6EYH7W0RdXeQXPurJ-39 | — |
| 94 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 95 | address \<TBD:OFFICE_VIP> primary | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 96 | priority 110 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 97 | preempt delay minimum 0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 98 | exit | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 101 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-198, 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 102 | description to tk1-core02 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-198, 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 103 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-198, 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 104 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-198, 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 105 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-198, 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 108 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-300, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 109 | description to tk1-sr1acc01 Te0/1,Te0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-300, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 110 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-300, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 111 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-300, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 112 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-300, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 115 | interface Port-channel3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-302, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 116 | description to tk1-sr2acc01 Te0/1,Te0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-302, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 117 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-302, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 118 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-302, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 119 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-302, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 122 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 123 | description to tk1-fw01 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 124 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 125 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 126 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 127 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-21, 9BYiFAK1cGA9hBdD1Cum-309 | — |
| 131 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 132 | description to tk1-rt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 133 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 134 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 135 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 136 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-23, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 138 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 139 | description to tk1-sr1acc01 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 140 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 141 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 142 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 143 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 144 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-217, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 146 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 147 | description to tk1-sr1acc01 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 148 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 149 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 150 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 151 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 152 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-218, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 154 | interface TenGigabitEthernet0/5 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 155 | description to tk1-sr2acc01 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 156 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 157 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 158 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 159 | channel-group 3 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 160 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-222, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 162 | interface TenGigabitEthernet0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 163 | description to tk1-sr2acc01 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 164 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 165 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 166 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 167 | channel-group 3 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 168 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-223, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 171 | interface TenGigabitEthernet0/7 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 172 | description to tk1-fnacc01 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 173 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 174 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 175 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 176 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-83, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 180 | interface TenGigabitEthernet0/22 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 181 | description to tk1-mgmt01 Gi0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 182 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 183 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 184 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 185 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-351, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 187 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 188 | description to tk1-core02 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 189 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 190 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 191 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 192 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 193 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-187, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 195 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 196 | description to tk1-core02 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 197 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 198 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 199 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 200 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 201 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-185, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 203 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-200, 9BYiFAK1cGA9hBdD1Cum-201 | R-018 |
| 204 | description Diagram Mgmt to tk1-mgmt01 Gi0/1 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-200, 9BYiFAK1cGA9hBdD1Cum-201 | R-018 |
| 205 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-200, 9BYiFAK1cGA9hBdD1Cum-201 | R-018 |
| 206 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-200, 9BYiFAK1cGA9hBdD1Cum-201 | R-018 |
| 207 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-200, 9BYiFAK1cGA9hBdD1Cum-201 | R-018 |
| 209 | ip route 0.0.0.0 0.0.0.0 172.17.0.1 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-107, J5z6EYH7W0RdXeQXPurJ-109 | — |
| 210 | ip route 172.18.0.0 255.255.0.0 172.17.0.2 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-107, J5z6EYH7W0RdXeQXPurJ-109 | — |
| 211 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 215 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-core02

[tk1-core02.cfg](tk1-core02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-core02
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
ip routing
spanning-tree mode rapid-pvst
fhrp version vrrp v3
spanning-tree vlan 2,9-11,100-399 root secondary
!
vlan 2
 name EXT
!
vlan 9
 name MGMT
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
vlan 300-399
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.17.0.5 255.255.255.224
 no shutdown
 vrrp 2 address-family ipv4
  address 172.17.0.6 primary
  preempt delay minimum 0
 exit
!
! WARN R-001 verify values in conversion report
interface Vlan9
 ip address 172.17.1.2 255.255.255.0
 no shutdown
 vrrp 9 address-family ipv4
  address 172.17.1.3 primary
  preempt delay minimum 0
 exit
!
interface Vlan10
 ip address 172.17.2.2 255.255.255.0
 no shutdown
 vrrp 10 address-family ipv4
  address 172.17.2.3 primary
  preempt delay minimum 0
 exit
!
interface Vlan11
 ip address 172.17.3.2 255.255.255.0
 no shutdown
 vrrp 11 address-family ipv4
  address 172.17.3.3 primary
  preempt delay minimum 0
 exit
!
! WARN R-012 verify values in conversion report
interface Vlan<TBD:PROD_VLAN_ID>
 ip address <TBD:PROD_LOCAL_IP_2> <TBD:PROD_MASK>
 no shutdown
 vrrp <TBD:PROD_VRID> address-family ipv4
  address <TBD:PROD_VIP> primary
  preempt delay minimum 0
 exit
!
! WARN R-012 verify values in conversion report
interface Vlan<TBD:DEV_VLAN_ID>
 ip address <TBD:DEV_LOCAL_IP_2> <TBD:DEV_MASK>
 no shutdown
 vrrp <TBD:DEV_VRID> address-family ipv4
  address <TBD:DEV_VIP> primary
  preempt delay minimum 0
 exit
!
! WARN R-011 verify values in conversion report
interface Vlan<TBD:OFFICE_VLAN_ID>
 ip address <TBD:OFFICE_LOCAL_IP_2> 255.255.255.0
 no shutdown
 ip helper-address <TBD:OFFICE_DHCP_SERVER>
 vrrp <TBD:OFFICE_VRID> address-family ipv4
  address <TBD:OFFICE_VIP> primary
  preempt delay minimum 0
 exit
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-core01 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-sr1acc02 Te0/1,Te0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel3
 description to tk1-sr2acc02 Te0/1,Te0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/1
 description to tk1-fw01 Te0/3 [10GBASE-SR OM3]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface TenGigabitEthernet0/2
 description to tk1-rt01 Gi0/3 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 2
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-sr1acc02 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-sr1acc02 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/5
 description to tk1-sr2acc02 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 3 mode active
 no shutdown
!
interface TenGigabitEthernet0/6
 description to tk1-sr2acc02 Te0/2 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 3 mode active
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/7
 description to tk1-fnacc02 Te0/1 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/22
 description to tk1-mgmt02 Gi0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-core01 Te0/23 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-core01 Te0/24 [10GBASE-SR OM3]
 switchport
 switchport mode trunk
 switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt02 Gi0/1
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 172.17.0.1
ip route 172.18.0.0 255.255.0.0 172.17.0.2
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-core02 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-147 | — |
| 4 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-346 | — |
| 5 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-346 | — |
| 6 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-346 | — |
| 8 | ip routing | 【図】GRT | 9BYiFAK1cGA9hBdD1Cum-299 | — |
| 9 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-147 | — |
| 10 | fhrp version vrrp v3 | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 11 | spanning-tree vlan 2,9-11,100-399 root secondary | 【図】VRRP凡例／【推測】VRRPv3とSTPルート | 9BYiFAK1cGA9hBdD1Cum-628 | — |
| 13 | vlan 2 | 【図】セグメントラベル | — | — |
| 14 | name EXT | 【図】セグメントラベル | — | — |
| 16 | vlan 9 | 【図】セグメントラベル | — | — |
| 17 | name MGMT | 【図】セグメントラベル | — | — |
| 19 | vlan 10 | 【図】セグメントラベル | — | — |
| 20 | name DMZ | 【図】セグメントラベル | — | — |
| 22 | vlan 11 | 【図】セグメントラベル | — | — |
| 23 | name COMMON | 【図】セグメントラベル | — | — |
| 25 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 27 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 29 | vlan 300-399 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 32 | interface Vlan2 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 33 | ip address 172.17.0.5 255.255.255.224 | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 34 | no shutdown | 【図】横線、バッジ、冗長化線 | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 35 | vrrp 2 address-family ipv4 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 36 | address 172.17.0.6 primary | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 37 | preempt delay minimum 0 | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 38 | exit | 【図】横線、バッジ、冗長化線／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-199, 9BYiFAK1cGA9hBdD1Cum-299 | R-009 |
| 41 | interface Vlan9 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 42 | ip address 172.17.1.2 255.255.255.0 | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 43 | no shutdown | 【論】管理CIDR／【図】バッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 44 | vrrp 9 address-family ipv4 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 45 | address 172.17.1.3 primary | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 46 | preempt delay minimum 0 | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 47 | exit | 【論】管理CIDR／【図】バッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-359 | R-001 |
| 49 | interface Vlan10 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 50 | ip address 172.17.2.2 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 51 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 52 | vrrp 10 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 53 | address 172.17.2.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 54 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 55 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-224 | — |
| 57 | interface Vlan11 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 58 | ip address 172.17.3.2 255.255.255.0 | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 59 | no shutdown | 【図】セグメントとバッジ、VIP | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 60 | vrrp 11 address-family ipv4 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 61 | address 172.17.3.3 primary | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 62 | preempt delay minimum 0 | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 63 | exit | 【図】セグメントとバッジ、VIP／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-225 | — |
| 66 | interface Vlan\<TBD:PROD_VLAN_ID> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 67 | ip address \<TBD:PROD_LOCAL_IP_2> \<TBD:PROD_MASK> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 68 | no shutdown | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 69 | vrrp \<TBD:PROD_VRID> address-family ipv4 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 70 | address \<TBD:PROD_VIP> primary | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 71 | preempt delay minimum 0 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 72 | exit | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-226 | R-012 |
| 75 | interface Vlan\<TBD:DEV_VLAN_ID> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 76 | ip address \<TBD:DEV_LOCAL_IP_2> \<TBD:DEV_MASK> | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 77 | no shutdown | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開 | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 78 | vrrp \<TBD:DEV_VRID> address-family ipv4 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 79 | address \<TBD:DEV_VIP> primary | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 80 | preempt delay minimum 0 | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 81 | exit | 【図】業務VLAN集約とバッジ／【推測】SVIをVLAN単位で展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-227 | R-012 |
| 84 | interface Vlan\<TBD:OFFICE_VLAN_ID> | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 85 | ip address \<TBD:OFFICE_LOCAL_IP_2> 255.255.255.0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 86 | no shutdown | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開 | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 87 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | 【論・推測】DHCPサーバーとオフィス端末 | J5z6EYH7W0RdXeQXPurJ-39 | — |
| 88 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 89 | address \<TBD:OFFICE_VIP> primary | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 90 | preempt delay minimum 0 | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 91 | exit | 【図】OFFICE集約／【論】フロアごと/24／【推測】1 VLAN分の展開／【推測】VRRPv3、グループ番号、優先度・プリエンプト | 9BYiFAK1cGA9hBdD1Cum-228 | R-011 |
| 94 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 95 | description to tk1-core01 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 96 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 97 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 98 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-186, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 101 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-454, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 102 | description to tk1-sr1acc02 Te0/1,Te0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-454, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 103 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-454, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 104 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-454, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 105 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-454, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 108 | interface Port-channel3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-455, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 109 | description to tk1-sr2acc02 Te0/1,Te0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-455, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 110 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-455, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 111 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-455, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 112 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-455, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 115 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 116 | description to tk1-fw01 Te0/3 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 117 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 118 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 119 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 120 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-28, 9BYiFAK1cGA9hBdD1Cum-66 | — |
| 124 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 125 | description to tk1-rt01 Gi0/3 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 126 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 127 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 128 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 129 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-29, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 131 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 132 | description to tk1-sr1acc02 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 133 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 134 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 135 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 136 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 137 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-24, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 139 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 140 | description to tk1-sr1acc02 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 141 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 142 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 143 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 144 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 145 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-25, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 147 | interface TenGigabitEthernet0/5 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 148 | description to tk1-sr2acc02 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 149 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 150 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 151 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 152 | channel-group 3 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 153 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-26, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 155 | interface TenGigabitEthernet0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 156 | description to tk1-sr2acc02 Te0/2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 157 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 158 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 159 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 160 | channel-group 3 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 161 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-27, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 164 | interface TenGigabitEthernet0/7 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 165 | description to tk1-fnacc02 Te0/1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 166 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 167 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 168 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 169 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-84, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 173 | interface TenGigabitEthernet0/22 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 174 | description to tk1-mgmt02 Gi0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 175 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 176 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 177 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 178 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-358, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 180 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 181 | description to tk1-core01 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 182 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 183 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 184 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 185 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 186 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-467, 9BYiFAK1cGA9hBdD1Cum-186 | — |
| 188 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 189 | description to tk1-core01 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 190 | switchport | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 191 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 192 | switchport trunk allowed vlan 2,10,11,100-199,200-299,300-399 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 193 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 194 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-466, 9BYiFAK1cGA9hBdD1Cum-184 | — |
| 196 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-345, 9BYiFAK1cGA9hBdD1Cum-346 | R-018 |
| 197 | description Diagram Mgmt to tk1-mgmt02 Gi0/1 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-345, 9BYiFAK1cGA9hBdD1Cum-346 | R-018 |
| 198 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-345, 9BYiFAK1cGA9hBdD1Cum-346 | R-018 |
| 199 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-345, 9BYiFAK1cGA9hBdD1Cum-346 | R-018 |
| 200 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-345, 9BYiFAK1cGA9hBdD1Cum-346 | R-018 |
| 202 | ip route 0.0.0.0 0.0.0.0 172.17.0.1 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-107, J5z6EYH7W0RdXeQXPurJ-109 | — |
| 203 | ip route 172.18.0.0 255.255.0.0 172.17.0.2 | 【論】defaultと対向拠点経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-107, J5z6EYH7W0RdXeQXPurJ-109 | — |
| 204 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 208 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-fnacc01

[tk1-fnacc01.cfg](tk1-fnacc01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-fnacc01
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
vlan <TBD:VLAN_OFFICE_TK_F6>
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-fnacc02 Gi0/23,Gi0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
interface GigabitEthernet0/1
 description to tk1-f6ap01 Gi0/1 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_TK_F6>
 spanning-tree portfast
 power inline auto
 no shutdown
!
interface GigabitEthernet0/2
 description Reserved PoE
 shutdown
!
interface GigabitEthernet0/23
 description to tk1-fnacc02 Gi0/23 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/24
 description to tk1-fnacc02 Gi0/24 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 channel-group 1 mode active
 no shutdown
!
interface range GigabitEthernet0/3 - 20
 description to office endpoints [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_TK_F6>
 spanning-tree portfast
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/7 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
ip default-gateway 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-fnacc01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-374 | — |
| 4 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-374 | — |
| 6 | vlan 9 | 【図】セグメントラベル | — | — |
| 7 | name MGMT | 【図】セグメントラベル | — | — |
| 9 | vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 11 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-374 | — |
| 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-374 | — |
| 13 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-374 | — |
| 16 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-489, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 17 | description to tk1-fnacc02 Gi0/23,Gi0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-489, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 18 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-489, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-489, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 20 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-489, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 22 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 23 | description to tk1-f6ap01 Gi0/1 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 24 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 25 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 26 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 27 | power inline auto | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 28 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-73, 9BYiFAK1cGA9hBdD1Cum-74 | — |
| 30 | interface GigabitEthernet0/2 | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-504 | — |
| 31 | description Reserved PoE | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-504 | — |
| 32 | shutdown | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-504 | — |
| 34 | interface GigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 35 | description to tk1-fnacc02 Gi0/23 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 36 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 37 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 38 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-76, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 41 | interface GigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 42 | description to tk1-fnacc02 Gi0/24 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 43 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 45 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-75, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 48 | interface range GigabitEthernet0/3 - 20 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 49 | description to office endpoints [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 50 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 51 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 52 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-384, 9BYiFAK1cGA9hBdD1Cum-385 | — |
| 56 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-77, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 57 | description to tk1-core01 Te0/7 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-77, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 58 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-77, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 59 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-77, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-77, 9BYiFAK1cGA9hBdD1Cum-756 | — |
| 62 | ip default-gateway 172.17.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 66 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-fnacc02

[tk1-fnacc02.cfg](tk1-fnacc02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
! WARN R-002 hostname resolved using the physical diagram
hostname tk1-fnacc02
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
vlan <TBD:VLAN_OFFICE_TK_F6>
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-fnacc01 Gi0/23,Gi0/24
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
interface GigabitEthernet0/1
 description to tk1-f6ap02 Gi0/1 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_TK_F6>
 spanning-tree portfast
 power inline auto
 no shutdown
!
interface GigabitEthernet0/2
 description Reserved PoE
 shutdown
!
interface GigabitEthernet0/23
 description to tk1-fnacc01 Gi0/23 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/24
 description to tk1-fnacc01 Gi0/24 [1000BASE-T Cat6a]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 channel-group 1 mode active
 no shutdown
!
interface range GigabitEthernet0/3 - 20
 description to office endpoints [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan <TBD:VLAN_OFFICE_TK_F6>
 spanning-tree portfast
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/7 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 9,<TBD:VLAN_OFFICE_TK_F6>
 no shutdown
!
ip default-gateway 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 3 | hostname tk1-fnacc02 | 【物】重複解消 | 9BYiFAK1cGA9hBdD1Cum-488 | — |
| 5 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-488 | — |
| 7 | vlan 9 | 【図】セグメントラベル | — | — |
| 8 | name MGMT | 【図】セグメントラベル | — | — |
| 10 | vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 12 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-488 | — |
| 13 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-488 | — |
| 14 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-488 | — |
| 17 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-498, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 18 | description to tk1-fnacc01 Gi0/23,Gi0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-498, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 19 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-498, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 20 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-498, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 21 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-498, 9BYiFAK1cGA9hBdD1Cum-499, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 23 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 24 | description to tk1-f6ap02 Gi0/1 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 25 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 26 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 27 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 28 | power inline auto | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 29 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-80, 9BYiFAK1cGA9hBdD1Cum-79 | — |
| 31 | interface GigabitEthernet0/2 | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-595 | — |
| 32 | description Reserved PoE | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-595 | — |
| 33 | shutdown | 【図】PoE予備 | 9BYiFAK1cGA9hBdD1Cum-595 | — |
| 35 | interface GigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 36 | description to tk1-fnacc01 Gi0/23 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 37 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 38 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 39 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 40 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-496, 9BYiFAK1cGA9hBdD1Cum-499 | — |
| 42 | interface GigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 43 | description to tk1-fnacc01 Gi0/24 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 44 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 45 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 46 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 47 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-497, 9BYiFAK1cGA9hBdD1Cum-500 | — |
| 49 | interface range GigabitEthernet0/3 - 20 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 50 | description to office endpoints [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 51 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 52 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 53 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 54 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-387, 9BYiFAK1cGA9hBdD1Cum-386 | — |
| 57 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-81, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 58 | description to tk1-core02 Te0/7 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-81, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 59 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-81, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 60 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-81, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 61 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-81, 9BYiFAK1cGA9hBdD1Cum-768 | — |
| 63 | ip default-gateway 172.17.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 67 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-fw01

[tk1-fw01.cfg](tk1-fw01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-fw01
!
! Expected firewall mode: routed
interface TenGigabitEthernet0/1
 description to carrier handoff [10GBASE-SR OM3]
 nameif outside
 security-level 0
 ip address <TBD:OUTSIDE_IP_198.51.100.0_25> 255.255.255.128
 no shutdown
!
! WARN R-009 EXT L2 forwarding and BPDU transport
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/1 [10GBASE-SR OM3]
 nameif ext_core01
 security-level 100
 bridge-group 2
 no shutdown
!
! WARN R-009 EXT L2 forwarding and BPDU transport
interface TenGigabitEthernet0/3
 description to tk1-core02 Te0/1 [10GBASE-SR OM3]
 nameif ext_core02
 security-level 100
 bridge-group 2
 no shutdown
!
interface BVI2
 nameif ext
 security-level 100
 ip address 172.17.0.1 255.255.255.224
 no shutdown
!
same-security-traffic permit inter-interface
! WARN R-013 verify that ISP next hop is on the local outside subnet
route outside 0.0.0.0 0.0.0.0 <TBD:LOCAL_ISP_GATEWAY> 1
route ext 172.17.0.0 255.255.0.0 172.17.0.6 1
nat (<TBD:NAT_INGRESS_IF>,outside) source dynamic <TBD:NAT_SOURCE_OBJECT> <TBD:NAT_TRANSLATED_TARGET>
access-list <TBD:ACL_NAME> extended <TBD:ACL_RULE>
access-group <TBD:ACL_NAME> in interface <TBD:ACL_INGRESS_IF>
!
! Management services: populate after approval of the management plan
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-fw01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-145 | — |
| 5 | interface TenGigabitEthernet0/1 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 6 | description to carrier handoff [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 7 | nameif outside | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 8 | security-level 0 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 9 | ip address \<TBD:OUTSIDE_IP_198.51.100.0_25> 255.255.255.128 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 10 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-70, 9BYiFAK1cGA9hBdD1Cum-61 | — |
| 13 | interface TenGigabitEthernet0/2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 14 | description to tk1-core01 Te0/1 [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 15 | nameif ext_core01 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 16 | security-level 100 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 17 | bridge-group 2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 18 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-309, 9BYiFAK1cGA9hBdD1Cum-49 | — |
| 21 | interface TenGigabitEthernet0/3 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 22 | description to tk1-core02 Te0/1 [10GBASE-SR OM3] | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 23 | nameif ext_core02 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 24 | security-level 100 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 25 | bridge-group 2 | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 26 | no shutdown | 【図】外側／EXT接続／【推測】ASAのBVI、インターフェース名とsecurity-level | 9BYiFAK1cGA9hBdD1Cum-66, 9BYiFAK1cGA9hBdD1Cum-67 | — |
| 28 | interface BVI2 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 29 | nameif ext | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 30 | security-level 100 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 31 | ip address 172.17.0.1 255.255.255.224 | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 32 | no shutdown | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 34 | same-security-traffic permit inter-interface | 【図】EXT .1／【推測】ルーティングモードBVIと同レベルメンバー間転送 | 9BYiFAK1cGA9hBdD1Cum-288 | R-009 |
| 36 | route outside 0.0.0.0 0.0.0.0 \<TBD:LOCAL_ISP_GATEWAY> 1 | 【論】defaultと自拠点経路の矢印／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-137, J5z6EYH7W0RdXeQXPurJ-147 | R-013 |
| 37 | route ext 172.17.0.0 255.255.0.0 172.17.0.6 1 | 【論】defaultと自拠点経路の矢印／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-137, J5z6EYH7W0RdXeQXPurJ-147 | R-013 |
| 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | 【一般】外向けNATとFWポリシー確認用の雛形 | — | — |
| 43 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-mgmt01

[tk1-mgmt01.cfg](tk1-mgmt01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-mgmt01
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-mgmt02 Gi0/47,Gi0/48
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface GigabitEthernet0/1
 description to tk1-core01 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
interface GigabitEthernet0/2
 description to tk1-core01 Te0/22 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface GigabitEthernet0/3
 description to tk1-sr1acc01 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/4
 description to tk1-sr2acc01 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/5
 description to tk1-svr101 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/6
 description to tk1-svr102 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/12
 description to tk1-svr108 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/47
 description to tk1-mgmt02 Gi0/47 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/48
 description to tk1-mgmt02 Gi0/48 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
 no shutdown
!
ip default-gateway 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-mgmt01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-360 | — |
| 4 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-360 | — |
| 6 | vlan 9 | 【図】セグメントラベル | — | — |
| 7 | name MGMT | 【図】セグメントラベル | — | — |
| 9 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-360 | — |
| 10 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-360 | — |
| 11 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-360 | — |
| 14 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-337, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 15 | description to tk1-mgmt02 Gi0/47,Gi0/48 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-337, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 16 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-337, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 17 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-337, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 18 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-337, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 20 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 21 | description to tk1-core01 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 22 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 23 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 24 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 25 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-321, 9BYiFAK1cGA9hBdD1Cum-200 | — |
| 28 | interface GigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-344, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 29 | description to tk1-core01 Te0/22 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-344, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 30 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-344, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 31 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-344, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 32 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-344, 9BYiFAK1cGA9hBdD1Cum-350 | — |
| 34 | interface GigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 35 | description to tk1-sr1acc01 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 36 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 37 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 38 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-342, 9BYiFAK1cGA9hBdD1Cum-338 | — |
| 41 | interface GigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 42 | description to tk1-sr2acc01 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 43 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 44 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 45 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-478, 9BYiFAK1cGA9hBdD1Cum-440 | — |
| 48 | interface GigabitEthernet0/5 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 49 | description to tk1-svr101 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 50 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 51 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 52 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-312, 9BYiFAK1cGA9hBdD1Cum-303 | — |
| 55 | interface GigabitEthernet0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 56 | description to tk1-svr102 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 57 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 58 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 59 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-317, 9BYiFAK1cGA9hBdD1Cum-305 | — |
| 62 | interface GigabitEthernet0/12 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 63 | description to tk1-svr108 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 64 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 65 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 66 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 67 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-319, 9BYiFAK1cGA9hBdD1Cum-307 | — |
| 69 | interface GigabitEthernet0/47 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 70 | description to tk1-mgmt02 Gi0/47 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 71 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 72 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 73 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 74 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-335, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 76 | interface GigabitEthernet0/48 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 77 | description to tk1-mgmt02 Gi0/48 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 78 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 79 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 80 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 81 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-333, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 83 | ip default-gateway 172.17.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 87 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-mgmt02

[tk1-mgmt02.cfg](tk1-mgmt02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-mgmt02
!
spanning-tree mode rapid-pvst
!
vlan 9
 name MGMT
!
interface Vlan9
 ip address <TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-mgmt01 Gi0/47,Gi0/48
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface GigabitEthernet0/1
 description to tk1-core02 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
interface GigabitEthernet0/2
 description to tk1-core02 Te0/22 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 9
 no shutdown
!
interface GigabitEthernet0/3
 description to tk1-sr1acc02 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/4
 description to tk1-sr2acc02 Mgmt [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/5
 description to tk1-svr201 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/6
 description to tk1-svr202 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/12
 description to tk1-svr208 BMC [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 spanning-tree portfast
 no shutdown
!
interface GigabitEthernet0/47
 description to tk1-mgmt01 Gi0/47 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/48
 description to tk1-mgmt01 Gi0/48 [1000BASE-T Cat6a]
 switchport mode access
 switchport access vlan 9
 channel-group 1 mode active
 no shutdown
!
ip default-gateway 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-mgmt02 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-503 | — |
| 4 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-503 | — |
| 6 | vlan 9 | 【図】セグメントラベル | — | — |
| 7 | name MGMT | 【図】セグメントラベル | — | — |
| 9 | interface Vlan9 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-503 | — |
| 10 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-503 | — |
| 11 | no shutdown | 【図】管理VLAN9の .x／【論】管理サブネット | 9BYiFAK1cGA9hBdD1Cum-503 | — |
| 14 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-481, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 15 | description to tk1-mgmt01 Gi0/47,Gi0/48 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-481, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 16 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-481, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 17 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-481, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 18 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-481, 9BYiFAK1cGA9hBdD1Cum-334, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 20 | interface GigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 21 | description to tk1-core02 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 22 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 23 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 24 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 25 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-349, 9BYiFAK1cGA9hBdD1Cum-345 | — |
| 28 | interface GigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-348, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 29 | description to tk1-core02 Te0/22 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-348, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 30 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-348, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 31 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-348, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 32 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-348, 9BYiFAK1cGA9hBdD1Cum-357 | — |
| 34 | interface GigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 35 | description to tk1-sr1acc02 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 36 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 37 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 38 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-325, 9BYiFAK1cGA9hBdD1Cum-313 | — |
| 41 | interface GigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 42 | description to tk1-sr2acc02 Mgmt [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 43 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 44 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 45 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-326, 9BYiFAK1cGA9hBdD1Cum-347 | — |
| 48 | interface GigabitEthernet0/5 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 49 | description to tk1-svr201 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 50 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 51 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 52 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-322, 9BYiFAK1cGA9hBdD1Cum-331 | — |
| 55 | interface GigabitEthernet0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 56 | description to tk1-svr202 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 57 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 58 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 59 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-323, 9BYiFAK1cGA9hBdD1Cum-329 | — |
| 62 | interface GigabitEthernet0/12 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 63 | description to tk1-svr208 BMC [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 64 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 65 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 66 | spanning-tree portfast | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 67 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-324, 9BYiFAK1cGA9hBdD1Cum-327 | — |
| 69 | interface GigabitEthernet0/47 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 70 | description to tk1-mgmt01 Gi0/47 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 71 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 72 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 73 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 74 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-479, 9BYiFAK1cGA9hBdD1Cum-334 | — |
| 76 | interface GigabitEthernet0/48 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 77 | description to tk1-mgmt01 Gi0/48 [1000BASE-T Cat6a] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 78 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 79 | switchport access vlan 9 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 80 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 81 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-480, 9BYiFAK1cGA9hBdD1Cum-502 | — |
| 83 | ip default-gateway 172.17.1.3 | 【推測】インバンド管理の管理VIP | — | R-018 |
| 87 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-rt01

[tk1-rt01.cfg](tk1-rt01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-rt01
!
ip routing
spanning-tree mode rapid-pvst
!
vlan 2
 name EXT
!
! WARN R-009 verify values in conversion report
interface Vlan2
 ip address 172.17.0.2 255.255.255.224
 no shutdown
!
interface GigabitEthernet0/1
 description to interbuilding carrier handoff [1000BASE-T Cat6a]
 ip address <TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface GigabitEthernet0/2
 description to tk1-core01 Te0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 2
 no shutdown
!
! Verify SFP+ copper module and 1G interoperability
! WARN R-009 EXT bridge path / verify STP and VRRP
interface GigabitEthernet0/3
 description to tk1-core02 Te0/2 [1000BASE-T Cat6a, SFP+ copper]
 switchport mode access
 switchport access vlan 2
 no shutdown
!
ip route 172.17.0.0 255.255.0.0 172.17.0.6
ip route 172.18.0.0 255.255.0.0 <TBD:INTER_BLDG_REMOTE_RT_IP>
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-rt01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-146 | — |
| 4 | ip routing | 【図】GRT | 9BYiFAK1cGA9hBdD1Cum-456 | — |
| 5 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-146 | — |
| 7 | vlan 2 | 【図】セグメントラベル | — | — |
| 8 | name EXT | 【図】セグメントラベル | — | — |
| 11 | interface Vlan2 | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-465, 9BYiFAK1cGA9hBdD1Cum-456 | R-009 |
| 12 | ip address 172.17.0.2 255.255.255.224 | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-465, 9BYiFAK1cGA9hBdD1Cum-456 | R-009 |
| 13 | no shutdown | 【図】EXT .2／【推測】L2スイッチポートとSVI | 9BYiFAK1cGA9hBdD1Cum-465, 9BYiFAK1cGA9hBdD1Cum-456 | R-009 |
| 15 | interface GigabitEthernet0/1 | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-64, 9BYiFAK1cGA9hBdD1Cum-464 | — |
| 16 | description to interbuilding carrier handoff [1000BASE-T Cat6a] | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-64, 9BYiFAK1cGA9hBdD1Cum-464 | — |
| 17 | ip address \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0 | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-64, 9BYiFAK1cGA9hBdD1Cum-464 | — |
| 18 | no shutdown | 【図】拠点間回線・バッジ .x | 9BYiFAK1cGA9hBdD1Cum-64, 9BYiFAK1cGA9hBdD1Cum-464 | — |
| 22 | interface GigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-63, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 23 | description to tk1-core01 Te0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-63, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 24 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-63, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 25 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-63, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 26 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-63, 9BYiFAK1cGA9hBdD1Cum-22 | — |
| 30 | interface GigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-69, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 31 | description to tk1-core02 Te0/2 [1000BASE-T Cat6a, SFP+ copper] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-69, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 32 | switchport mode access | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-69, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 33 | switchport access vlan 2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-69, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 34 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-69, 9BYiFAK1cGA9hBdD1Cum-68 | — |
| 36 | ip route 172.17.0.0 255.255.0.0 172.17.0.6 | 【論】自拠点と対向拠点への経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-145, J5z6EYH7W0RdXeQXPurJ-135 | R-013 |
| 37 | ip route 172.18.0.0 255.255.0.0 \<TBD:INTER_BLDG_REMOTE_RT_IP> | 【論】自拠点と対向拠点への経路／【推測】拠点集約 /16 | J5z6EYH7W0RdXeQXPurJ-145, J5z6EYH7W0RdXeQXPurJ-135 | R-013 |
| 41 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-sr1acc01

[tk1-sr1acc01.cfg](tk1-sr1acc01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-sr1acc01
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-sr1acc02 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-core01 Te0/3,Te0/4
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/3 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/4 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-svr101 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-svr102 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan <TBD:PROD_VLAN_LIST_TK1_SVR102>
 spanning-tree portfast trunk
 no shutdown
!
! WARN R-006 development VLAN membership checked against server links
interface TenGigabitEthernet0/10
 description to tk1-svr108 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 200-299
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc02 Te0/23 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc02 Te0/24 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt01 Gi0/3
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-sr1acc01 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-231 | — |
| 4 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-340 | — |
| 5 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-340 | — |
| 6 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-340 | — |
| 8 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-231 | — |
| 10 | vlan 10 | 【図】セグメントラベル | — | — |
| 11 | name DMZ | 【図】セグメントラベル | — | — |
| 13 | vlan 11 | 【図】セグメントラベル | — | — |
| 14 | name COMMON | 【図】セグメントラベル | — | — |
| 16 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 18 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 21 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-238, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 22 | description to tk1-sr1acc02 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-238, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 23 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-238, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 24 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-238, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 25 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-238, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 28 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-301, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 29 | description to tk1-core01 Te0/3,Te0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-301, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 30 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-301, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 31 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-301, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 32 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-301, 9BYiFAK1cGA9hBdD1Cum-33, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 34 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 35 | description to tk1-core01 Te0/3 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 36 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 37 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 38 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-35, 9BYiFAK1cGA9hBdD1Cum-33 | — |
| 41 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 42 | description to tk1-core01 Te0/4 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 43 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 44 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 45 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-37, 9BYiFAK1cGA9hBdD1Cum-36 | — |
| 48 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 49 | description to tk1-svr101 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 50 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 51 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 52 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-255, 9BYiFAK1cGA9hBdD1Cum-767 | — |
| 55 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 56 | description to tk1-svr102 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 57 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 58 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR102> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 59 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-257, 9BYiFAK1cGA9hBdD1Cum-763 | — |
| 63 | interface TenGigabitEthernet0/10 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 64 | description to tk1-svr108 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 65 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 66 | switchport trunk allowed vlan 200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 67 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 68 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-259, 9BYiFAK1cGA9hBdD1Cum-766 | — |
| 70 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 71 | description to tk1-sr1acc02 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 72 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 73 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 74 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 75 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-237, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 77 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 78 | description to tk1-sr1acc02 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 79 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 80 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 81 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 82 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-236, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 84 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-338, 9BYiFAK1cGA9hBdD1Cum-340 | R-018 |
| 85 | description Diagram Mgmt to tk1-mgmt01 Gi0/3 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-338, 9BYiFAK1cGA9hBdD1Cum-340 | R-018 |
| 86 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-338, 9BYiFAK1cGA9hBdD1Cum-340 | R-018 |
| 87 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-338, 9BYiFAK1cGA9hBdD1Cum-340 | R-018 |
| 88 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-338, 9BYiFAK1cGA9hBdD1Cum-340 | R-018 |
| 90 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 94 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-sr1acc02

[tk1-sr1acc02.cfg](tk1-sr1acc02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
hostname tk1-sr1acc02
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-sr1acc01 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-core02 Te0/3,Te0/4
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/3 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/2
 description to tk1-core02 Te0/4 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-svr101 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-svr102 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan <TBD:PROD_VLAN_LIST_TK1_SVR102>
 spanning-tree portfast trunk
 no shutdown
!
! WARN R-006 development VLAN membership checked against server links
interface TenGigabitEthernet0/10
 description to tk1-svr108 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 200-299
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-sr1acc01 Te0/23 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-sr1acc01 Te0/24 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt02 Gi0/3
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 2 | hostname tk1-sr1acc02 | 【図】機器名 | 9BYiFAK1cGA9hBdD1Cum-392 | — |
| 4 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-314 | — |
| 5 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-314 | — |
| 6 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-314 | — |
| 8 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-392 | — |
| 10 | vlan 10 | 【図】セグメントラベル | — | — |
| 11 | name DMZ | 【図】セグメントラベル | — | — |
| 13 | vlan 11 | 【図】セグメントラベル | — | — |
| 14 | name COMMON | 【図】セグメントラベル | — | — |
| 16 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 18 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 21 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-390, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 22 | description to tk1-sr1acc01 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-390, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 23 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-390, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 24 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-390, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 25 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-390, 9BYiFAK1cGA9hBdD1Cum-32, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 28 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-391, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 29 | description to tk1-core02 Te0/3,Te0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-391, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 30 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-391, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 31 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-391, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 32 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-391, 9BYiFAK1cGA9hBdD1Cum-41, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 34 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 35 | description to tk1-core02 Te0/3 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 36 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 37 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 38 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 39 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-42, 9BYiFAK1cGA9hBdD1Cum-41 | — |
| 41 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 42 | description to tk1-core02 Te0/4 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 43 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 44 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 45 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 46 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-44, 9BYiFAK1cGA9hBdD1Cum-43 | — |
| 48 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 49 | description to tk1-svr101 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 50 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 51 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 52 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 53 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-38, 9BYiFAK1cGA9hBdD1Cum-762 | — |
| 55 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 56 | description to tk1-svr102 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 57 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 58 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR102> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 59 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 60 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-39, 9BYiFAK1cGA9hBdD1Cum-764 | — |
| 63 | interface TenGigabitEthernet0/10 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 64 | description to tk1-svr108 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 65 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 66 | switchport trunk allowed vlan 200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 67 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 68 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-40, 9BYiFAK1cGA9hBdD1Cum-765 | — |
| 70 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 71 | description to tk1-sr1acc01 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 72 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 73 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 74 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 75 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-388, 9BYiFAK1cGA9hBdD1Cum-32 | — |
| 77 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 78 | description to tk1-sr1acc01 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 79 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 80 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 81 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 82 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-389, 9BYiFAK1cGA9hBdD1Cum-31 | — |
| 84 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-313, 9BYiFAK1cGA9hBdD1Cum-314 | R-018 |
| 85 | description Diagram Mgmt to tk1-mgmt02 Gi0/3 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-313, 9BYiFAK1cGA9hBdD1Cum-314 | R-018 |
| 86 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-313, 9BYiFAK1cGA9hBdD1Cum-314 | R-018 |
| 87 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-313, 9BYiFAK1cGA9hBdD1Cum-314 | R-018 |
| 88 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-313, 9BYiFAK1cGA9hBdD1Cum-314 | R-018 |
| 90 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 94 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-sr2acc01

[tk1-sr2acc01.cfg](tk1-sr2acc01.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
! WARN R-002 hostname resolved using the physical diagram
hostname tk1-sr2acc01
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-sr2acc02 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-core01 Te0/5,Te0/6
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
interface TenGigabitEthernet0/1
 description to tk1-core01 Te0/5 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/2
 description to tk1-core01 Te0/6 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-svr201 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-svr202 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan <TBD:PROD_VLAN_LIST_TK1_SVR202>
 spanning-tree portfast trunk
 no shutdown
!
! WARN R-006 development VLAN membership checked against server links
interface TenGigabitEthernet0/10
 description to tk1-svr208 eth1 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 200-299
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-sr2acc02 Te0/23 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-sr2acc02 Te0/24 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt01 Gi0/4
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 3 | hostname tk1-sr2acc01 | 【物】重複解消 | 9BYiFAK1cGA9hBdD1Cum-406 | — |
| 5 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-441 | — |
| 6 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-441 | — |
| 7 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-441 | — |
| 9 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-406 | — |
| 11 | vlan 10 | 【図】セグメントラベル | — | — |
| 12 | name DMZ | 【図】セグメントラベル | — | — |
| 14 | vlan 11 | 【図】セグメントラベル | — | — |
| 15 | name COMMON | 【図】セグメントラベル | — | — |
| 17 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 19 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 22 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-412, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 23 | description to tk1-sr2acc02 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-412, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 24 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-412, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 25 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-412, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 26 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-412, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 29 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-436, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 30 | description to tk1-core01 Te0/5,Te0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-436, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 31 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-436, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 32 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-436, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 33 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-436, 9BYiFAK1cGA9hBdD1Cum-468, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 35 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 36 | description to tk1-core01 Te0/5 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 37 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 38 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 39 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 40 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-398, 9BYiFAK1cGA9hBdD1Cum-468 | — |
| 42 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 43 | description to tk1-core01 Te0/6 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 44 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 45 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 46 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 47 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-400, 9BYiFAK1cGA9hBdD1Cum-470 | — |
| 49 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 50 | description to tk1-svr201 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 51 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 52 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 53 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 54 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-430, 9BYiFAK1cGA9hBdD1Cum-448 | — |
| 56 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 57 | description to tk1-svr202 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 58 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 59 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR202> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 60 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 61 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-432, 9BYiFAK1cGA9hBdD1Cum-449 | — |
| 64 | interface TenGigabitEthernet0/10 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 65 | description to tk1-svr208 eth1 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 66 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 67 | switchport trunk allowed vlan 200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 68 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 69 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-434, 9BYiFAK1cGA9hBdD1Cum-453 | — |
| 71 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 72 | description to tk1-sr2acc02 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 73 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 74 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 75 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 76 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-411, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 78 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 79 | description to tk1-sr2acc02 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 80 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 81 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 82 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 83 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-410, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 85 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-440, 9BYiFAK1cGA9hBdD1Cum-441 | R-018 |
| 86 | description Diagram Mgmt to tk1-mgmt01 Gi0/4 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-440, 9BYiFAK1cGA9hBdD1Cum-441 | R-018 |
| 87 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-440, 9BYiFAK1cGA9hBdD1Cum-441 | R-018 |
| 88 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-440, 9BYiFAK1cGA9hBdD1Cum-441 | R-018 |
| 89 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-440, 9BYiFAK1cGA9hBdD1Cum-441 | R-018 |
| 91 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 95 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

### tk1-sr2acc02

[tk1-sr2acc02.cfg](tk1-sr2acc02.cfg)

```text
! Diagram-derived configuration draft. Resolve all TBD values.
! WARN R-002 hostname resolved using the physical diagram
hostname tk1-sr2acc02
!
vrf definition Mgmt-vrf
 address-family ipv4
 exit-address-family
!
spanning-tree mode rapid-pvst
!
vlan 10
 name DMZ
!
vlan 11
 name COMMON
!
vlan 100-199
!
vlan 200-299
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel1
 description to tk1-sr2acc01 Te0/23,Te0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
! WARN R-010 verify VLAN forwarding and STP topology
interface Port-channel2
 description to tk1-core02 Te0/5,Te0/6
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 no shutdown
!
interface TenGigabitEthernet0/1
 description to tk1-core02 Te0/5 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/2
 description to tk1-core02 Te0/6 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 2 mode active
 no shutdown
!
interface TenGigabitEthernet0/3
 description to tk1-svr201 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/4
 description to tk1-svr202 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan <TBD:PROD_VLAN_LIST_TK1_SVR202>
 spanning-tree portfast trunk
 no shutdown
!
! WARN R-006 development VLAN membership checked against server links
interface TenGigabitEthernet0/10
 description to tk1-svr208 eth2 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 200-299
 spanning-tree portfast trunk
 no shutdown
!
interface TenGigabitEthernet0/23
 description to tk1-sr2acc01 Te0/23 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface TenGigabitEthernet0/24
 description to tk1-sr2acc01 Te0/24 [10GBASE-SR OM3]
 switchport mode trunk
 switchport trunk allowed vlan 10,11,100-199,200-299
 channel-group 1 mode active
 no shutdown
!
interface GigabitEthernet0/0
 description Diagram Mgmt to tk1-mgmt02 Gi0/4
 vrf forwarding Mgmt-vrf
 ip address <TBD:OOB_MANAGEMENT_IP> 255.255.255.0
 no shutdown
!
ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3
! Management options (populate only approved services)
! Optional service templates: ntp server {NTP_SERVER}; ip name-server {DEVICE_DNS_RESOLVER}
! Optional service templates: logging host {SYSLOG_SERVER}; SNMP and SSH per policy
end
```

| 行 | 設定 | 根拠 | cell id | 指摘ID |
| --- | --- | --- | --- | --- |
| 3 | hostname tk1-sr2acc02 | 【物】重複解消 | 9BYiFAK1cGA9hBdD1Cum-447 | — |
| 5 | vrf definition Mgmt-vrf | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-437 | — |
| 6 | address-family ipv4 | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-437 | — |
| 7 | exit-address-family | 【図】Mgmtと管理SWの接続／【推測】Catalyst管理VRFの名前 | 9BYiFAK1cGA9hBdD1Cum-437 | — |
| 9 | spanning-tree mode rapid-pvst | 【一般・推測】冗長L2リンク | 9BYiFAK1cGA9hBdD1Cum-447 | — |
| 11 | vlan 10 | 【図】セグメントラベル | — | — |
| 12 | name DMZ | 【図】セグメントラベル | — | — |
| 14 | vlan 11 | 【図】セグメントラベル | — | — |
| 15 | name COMMON | 【図】セグメントラベル | — | — |
| 17 | vlan 100-199 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 19 | vlan 200-299 | 【図】集約VLAN、【論】フロア単位の割当 | — | — |
| 22 | interface Port-channel1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-445, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 23 | description to tk1-sr2acc01 Te0/23,Te0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-445, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 24 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-445, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 25 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-445, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 26 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-445, 9BYiFAK1cGA9hBdD1Cum-396, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 29 | interface Port-channel2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-446, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 30 | description to tk1-core02 Te0/5,Te0/6 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-446, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 31 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-446, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 32 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-446, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 33 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-446, 9BYiFAK1cGA9hBdD1Cum-471, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 35 | interface TenGigabitEthernet0/1 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 36 | description to tk1-core02 Te0/5 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 37 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 38 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 39 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 40 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-404, 9BYiFAK1cGA9hBdD1Cum-471 | — |
| 42 | interface TenGigabitEthernet0/2 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 43 | description to tk1-core02 Te0/6 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 44 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 45 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 46 | channel-group 2 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 47 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-405, 9BYiFAK1cGA9hBdD1Cum-469 | — |
| 49 | interface TenGigabitEthernet0/3 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 50 | description to tk1-svr201 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 51 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 52 | switchport trunk allowed vlan 10,11 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 53 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 54 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-401, 9BYiFAK1cGA9hBdD1Cum-450 | — |
| 56 | interface TenGigabitEthernet0/4 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 57 | description to tk1-svr202 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 58 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 59 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR202> | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 60 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 61 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-402, 9BYiFAK1cGA9hBdD1Cum-451 | — |
| 64 | interface TenGigabitEthernet0/10 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 65 | description to tk1-svr208 eth2 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 66 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 67 | switchport trunk allowed vlan 200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 68 | spanning-tree portfast trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 69 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-403, 9BYiFAK1cGA9hBdD1Cum-452 | — |
| 71 | interface TenGigabitEthernet0/23 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 72 | description to tk1-sr2acc01 Te0/23 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 73 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 74 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 75 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 76 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-443, 9BYiFAK1cGA9hBdD1Cum-396 | — |
| 78 | interface TenGigabitEthernet0/24 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 79 | description to tk1-sr2acc01 Te0/24 [10GBASE-SR OM3] | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 80 | switchport mode trunk | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 81 | switchport trunk allowed vlan 10,11,100-199,200-299 | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 82 | channel-group 1 mode active | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 83 | no shutdown | 【図】接続先横線／【推測：規則性】02側省略／【図注記・論】フロア／アプリ単位のVLAN／【推測】LACP・STP | 9BYiFAK1cGA9hBdD1Cum-444, 9BYiFAK1cGA9hBdD1Cum-395 | — |
| 85 | interface GigabitEthernet0/0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-347, 9BYiFAK1cGA9hBdD1Cum-437 | R-018 |
| 86 | description Diagram Mgmt to tk1-mgmt02 Gi0/4 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-347, 9BYiFAK1cGA9hBdD1Cum-437 | R-018 |
| 87 | vrf forwarding Mgmt-vrf | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-347, 9BYiFAK1cGA9hBdD1Cum-437 | R-018 |
| 88 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-347, 9BYiFAK1cGA9hBdD1Cum-437 | R-018 |
| 89 | no shutdown | 【図】管理SWへのMgmt／【論】VLAN9 CIDR／【推測】Catalyst管理IF | 9BYiFAK1cGA9hBdD1Cum-347, 9BYiFAK1cGA9hBdD1Cum-437 | R-018 |
| 91 | ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 172.17.1.3 | 【推測】管理VRFの既定経路は管理VIP | — | R-018 |
| 95 | end | 【一般】 IOS-XE/ASAの構文 | — | — |

## 4. 推測で補った項目

| 項目 | 適用・根拠 | 確認元 |
| --- | --- | --- |
| 02号機の所属線 | 01側から同じポート・Poの所属を展開。各号機の物理接続・アドレスバッジは個別に反映 R-021 | 配線台帳 |
| 大阪サーバーの接続 | os1-core02 Te0/4の座標ともう一方のコア／サーバーによる対称性 R-004 | 図の端点修正 |
| 大阪core01 のEXT所属 | GRTに達する線とバッジを根拠 R-005 | 図の端点修正 |
| EXTの実装 | RTはL2スイッチポートとSVI、FWはrouted BVI R-009 | 機器型番と機能表 |
| 拠点集約 | 東京172.17.0.0/16、大阪172.18.0.0/16 | アドレス管理表 |
| オフィス | フロア/24単位、VIPの候補.3、フロアSVIへのDHCP relay。集約範囲には個別のローリング割当を展開しない R-011 | IP管理表、DHCPサーバーアドレス |
| 業務アプリ | PRODホストはアプリ別allowedリスト。DEVは図の範囲を許可し、個別SVIを展開する雛形 R-012 | 業務アプリ/VLAN対応表 |
| 管理 | OOB管理VRF・管理SW・フロアSWのdefaultは各拠点の管理VIP | IP管理表と運用設計 |

## 5. 既定値を使った項目

| 項目 | 既定値・実装 | 影響 |
| --- | --- | --- |
| LAG | LACP active（R5） | 全Port-channel |
| 冗長化 | VRRPv3、01優先度110、02はOS既定100、プリエンプト有効（6.2） | コア4台 |
| VRID | VLAN番号。集約と255超のケースはTBD（6.2） | コア |
| STP | Rapid PVST+、01をprimary、02をsecondary（6.2） | L2収容のIOS-XE、rootはコア |
| 管理VRF | CatalystのMgmt-vrf、GigabitEthernet0/0（4.2） | 東京コアとサーバーアクセスSW |
| trunk付加コマンド | 省略（1.1） | trunk全体 |
| 02出力 | 全文（1.1） | 冗長ペア |
| RTのEXT側 | L2スイッチポート＋SVI（R10） | 両拠点RT |
| 未使用ポート | 図に「予備」とあるもののみshutdown（R14） | フロアSWのGi0/2 |

## 6. 未確定値

[diagrams_tbd.md](diagrams_tbd.md) に全設定行を列挙しました。OFFICEと業務用のSVI雛形は割当済みVLANごとに展開します。

## 7. 図との差分

| 対象 | 図の記載 | 設定の扱い | 根拠 |
| --- | --- | --- | --- |
| 管理VLAN9 | 両拠点で172.17.2.0/24 | 東京172.17.1.0/24、大阪172.18.1.0/24 | 論理図 R-001 |
| 東京ラック2・右側フロアSW | 左側と同名 | tk1-sr2acc01/02、tk1-fnacc02 | 物理図 R-002 |
| 大阪コアとサーバー | 2箇所で線の片端未接続 | Te0/4の対向とEXTの所属を補完 | R-004 / R-005 |
| 管理IF・VRF | Mgmt／mgmt | GigabitEthernet0/0／Mgmt-vrf | Catalyst管理IFの構文 |
| フロア・本番ホストの末端VLAN | 図では集約範囲 | 単位別VLANまたはリストをTBD | 論理図と注記 |
| 所属線の色・ラベル接続 | 横線の色と不一致など | 端点の指すセグメントに所属 | R-008 / R-007 |
| 設計上のループ・迂回 | 両側が同一VLANを収容 | 図の所属を保持してWARNを付記 | R-009 / R-010 |

### ページ間の照合

物理図は機器名、ラック配置、束線と端点の照合に使用しました。個別ポートの識別は合成図の記載を優先しています。モノクロ版とカラー版の全ラベルを個数込みで比較した差分を示します。

| 差分の側 | セルのテキスト | 個数 |
| --- | --- | --- |
| 1C | .1 | 1 |
| 1C | Server Rack2 | 2 |
| 1C | tk1-fnap01 / Wifi AP | 1 |
| 1C | tk1-fnap02 / Wifi AP | 1 |
| 1C | オフィス固定端末 x5-10 | 2 |
| 4C | Server Rack1 | 2 |
| 4C | tk1-f6ap01 / Wifi AP | 1 |
| 4C | tk1-f6ap02 / Wifi AP | 1 |

## 8. チェック実施結果

18台、物理リンク78本、所属が明示された論理ポート・Po 48件、設定対象機器間リンク42本を確認しました。冗長ペア間の静的なL2経路と確定next-hopの直接接続性を検査しました。実機での構文チェックとSTP/VRRP収束試験は未実施です。

| チェックID | 結果 | 補足 |
| --- | --- | --- |
| N-01 | 該当あり R-002 | 指摘一覧参照 |
| N-02 | 該当あり R-002 | 指摘一覧参照 |
| N-03 | 該当あり R-002 | 指摘一覧参照 |
| N-04 | 該当なし | 確認した図と既知設定の範囲 |
| N-05 | 該当なし | 確認した図と既知設定の範囲 |
| A-01 | 該当あり R-001 | 指摘一覧参照 |
| A-02 | 該当あり R-001 | 指摘一覧参照 |
| A-03 | 該当なし | 確認した図と既知設定の範囲 |
| A-04 | 該当なし | 既知IPv4に重複なし。未確定値は置換後に検査 |
| A-05 | 該当あり R-011, R-012 | 指摘一覧参照 |
| A-06 | 該当あり R-011, R-012 | 指摘一覧参照 |
| A-07 | 該当あり R-001 | 指摘一覧参照 |
| V-01 | 該当なし | 確認した図と既知設定の範囲 |
| V-02 | 該当なし | 確認した図と既知設定の範囲 |
| V-03 | 該当あり R-021 | 指摘一覧参照 |
| V-04 | 該当なし | 機器間リンクの両端VLAN/モードを照合。サーバーのタグは実機要確認 |
| V-05 | 該当なし | 図の連続性を確認。STP収束・末端タグの動作は未検証 |
| V-06 | 該当あり R-009, R-010 | 指摘一覧参照 |
| V-07 | 該当あり R-011, R-012 | 指摘一覧参照 |
| V-08 | 該当なし | 確定設定・集約雛形に図上のL2出口を確認 |
| V-09 | 該当なし | 明示所属の一致を検査。集約とフロア単位の差は7章 |
| P-01 | 該当あり R-004, R-005, R-006 | 指摘一覧参照 |
| P-02 | 該当なし | 確認した図と既知設定の範囲 |
| P-03 | 該当あり R-003 | 指摘一覧参照 |
| P-04 | 該当なし | 確認した図と既知設定の範囲 |
| P-05 | 該当あり R-003, R-020 | 指摘一覧参照 |
| P-06 | 該当なし | LAG両メンバーは同じ対向機器 |
| P-07 | 該当あり R-023 | 指摘一覧参照 |
| P-08 | 該当あり R-021 | 指摘一覧参照 |
| L-01 | 該当あり R-019 | 指摘一覧参照 |
| L-02 | 該当あり R-005 | 指摘一覧参照 |
| L-03 | 該当なし | 確認した図と既知設定の範囲 |
| L-04 | 該当あり R-013 | 指摘一覧参照 |
| L-05 | 該当あり R-013, R-022 | 指摘一覧参照 |
| L-06 | 該当あり R-018 | 指摘一覧参照 |
| L-07 | 該当あり R-009, R-010 | 静的な経路の存在を確認。迂回経路の転送は要実機確認 |
| M-01 | 該当あり R-014, R-015, R-016, R-017 | 指摘一覧参照 |
| M-02 | 該当あり R-018 | 指摘一覧参照 |
| M-03 | 該当あり R-018 | 指摘一覧参照 |
| M-04 | 該当あり R-018 | 指摘一覧参照 |
| X-01 | 該当あり R-001 | 指摘一覧参照 |
| X-02 | 該当あり R-002 | 指摘一覧参照 |
| X-03 | 該当あり R-024 | 指摘一覧参照 |
| D-01 | 該当あり R-019 | 指摘一覧参照 |
| D-02 | 該当なし | 交差する線は座標と端点で確認 |
| D-03 | 該当あり R-008 | 指摘一覧参照 |
| D-04 | 該当あり R-007 | 指摘一覧参照 |

## 9. 対象外とAP設定項目

サーバー・VM・仮想スイッチ・端末・回線終端装置・ISP機器は、対向ポート設定の根拠として参照しました。APは機種・管理方式が未確定です。

| AP | 対向SW/IF | 給電 | ポート所属 | 未確定 |
| --- | --- | --- | --- | --- |
| tk1-f6ap01 | tk1-fnacc01 Gi0/1 | PoE | 東京6F OFFICEのaccess | 管理IP、SSID/VLAN対応 |
| tk1-f6ap02 | tk1-fnacc02 Gi0/1 | PoE | 東京6F OFFICEのaccess | 同上 |
| os1-fmap01 | os1-fmacc01 Gi0/1 | PoE | 大阪対象フロア OFFICEのaccess | 同上 |
| os1-fmap02 | os1-fmacc02 Gi0/1 | PoE | 大阪対象フロア OFFICEのaccess | 同上 |

## Cisco構文の参照資料

[Catalyst 9300 IOS XE IP Addressing Services Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/26-x/configuration_guide/ip/b_26x_ip_9300_cg.pdf)

[Catalyst 9300 Ethernet Management Port](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-18/configuration_guide/int_hw/b_1718_int_and_hw_9300_cg/configuring_ethernet_management_port.html)

[Cisco ASA Routed and Transparent Mode Interfaces](https://www.cisco.com/c/en/us/td/docs/security/asa/asa923/configuration/general/asa-923-general-config/interface-routed-tfw.html)

[Cisco ASA Transparent or Routed Firewall Mode](https://www.cisco.com/c/en/us/td/docs/security/asa/asa923/configuration/general/asa-923-general-config/intro-fw.html)

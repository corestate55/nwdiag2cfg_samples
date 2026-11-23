# 未確定値一覧

同じ識別子が別の機器に出る場合、機器・拠点ごとに値を確認します。同一フロアの対向ポートのOFFICE VLAN ID、同一ホストに接続する2ポートの本番VLANリスト、VRRPペアのVIPとVRIDは一致させます。

- VRRPのグループ番号は1〜255です。
- 拠点間アドレスは両側ルーターのIFと対向next-hopを対にして確定します。
- オフィス・業務向け雛形は割当済みのVLANごとに展開します。
- オプションの管理サービスは各機器のコメントに記載しました。採用時にサーバー、送信元VRF、認証方式、許可元を決めます。

| 機器 | 設定行 | 設定 | TBD | 情報源 | 投入前に置換 |
| --- | --- | --- | --- | --- | --- |
| os1-core01 | 62 | interface Vlan\<TBD:OFFICE_VLAN_ID> | \<TBD:OFFICE_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core01 | 63 | ip address \<TBD:OFFICE_LOCAL_IP_1> 255.255.255.0 | \<TBD:OFFICE_LOCAL_IP_1> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core01 | 65 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | \<TBD:OFFICE_DHCP_SERVER> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core01 | 66 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | \<TBD:OFFICE_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core01 | 67 | address \<TBD:OFFICE_VIP> primary | \<TBD:OFFICE_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core01 | 116 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 58 | interface Vlan\<TBD:OFFICE_VLAN_ID> | \<TBD:OFFICE_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 59 | ip address \<TBD:OFFICE_LOCAL_IP_2> 255.255.255.0 | \<TBD:OFFICE_LOCAL_IP_2> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 61 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | \<TBD:OFFICE_DHCP_SERVER> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 62 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | \<TBD:OFFICE_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 63 | address \<TBD:OFFICE_VIP> primary | \<TBD:OFFICE_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-core02 | 79 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 9 | vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| os1-fmacc01 | 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 25 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 51 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 58 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc01 | 66 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 9 | vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| os1-fmacc02 | 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 25 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 51 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 58 | switchport access vlan \<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fmacc02 | 66 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_OS_FM> | \<TBD:VLAN_OFFICE_OS_FM> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| os1-fw01 | 9 | ip address \<TBD:OUTSIDE_IP_203.0.113.0_25> 255.255.255.128 | \<TBD:OUTSIDE_IP_203.0.113.0_25> | 回線契約・拠点間IP台帳 | 必須 |
| os1-fw01 | 36 | route outside 0.0.0.0 0.0.0.0 \<TBD:LOCAL_ISP_GATEWAY> 1 | \<TBD:LOCAL_ISP_GATEWAY> | 回線契約・拠点間IP台帳 | 必須 |
| os1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_INGRESS_IF> | セキュリティポリシー | 必須 |
| os1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_SOURCE_OBJECT> | セキュリティポリシー | 必須 |
| os1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_TRANSLATED_TARGET> | セキュリティポリシー | 必須 |
| os1-fw01 | 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | \<TBD:ACL_NAME> | セキュリティポリシー | 必須 |
| os1-fw01 | 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | \<TBD:ACL_RULE> | セキュリティポリシー | 必須 |
| os1-fw01 | 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | \<TBD:ACL_NAME> | セキュリティポリシー | 必須 |
| os1-fw01 | 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | \<TBD:ACL_INGRESS_IF> | セキュリティポリシー | 必須 |
| os1-rt01 | 17 | ip address \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0 | \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> | 回線契約・拠点間IP台帳 | 必須 |
| os1-rt01 | 37 | ip route 172.17.0.0 255.255.0.0 \<TBD:INTER_BLDG_REMOTE_RT_IP> | \<TBD:INTER_BLDG_REMOTE_RT_IP> | 回線契約・拠点間IP台帳 | 必須 |
| tk1-core01 | 70 | interface Vlan\<TBD:PROD_VLAN_ID> | \<TBD:PROD_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 71 | ip address \<TBD:PROD_LOCAL_IP_1> \<TBD:PROD_MASK> | \<TBD:PROD_LOCAL_IP_1> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 71 | ip address \<TBD:PROD_LOCAL_IP_1> \<TBD:PROD_MASK> | \<TBD:PROD_MASK> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 73 | vrrp \<TBD:PROD_VRID> address-family ipv4 | \<TBD:PROD_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 74 | address \<TBD:PROD_VIP> primary | \<TBD:PROD_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 80 | interface Vlan\<TBD:DEV_VLAN_ID> | \<TBD:DEV_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 81 | ip address \<TBD:DEV_LOCAL_IP_1> \<TBD:DEV_MASK> | \<TBD:DEV_LOCAL_IP_1> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 81 | ip address \<TBD:DEV_LOCAL_IP_1> \<TBD:DEV_MASK> | \<TBD:DEV_MASK> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 83 | vrrp \<TBD:DEV_VRID> address-family ipv4 | \<TBD:DEV_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 84 | address \<TBD:DEV_VIP> primary | \<TBD:DEV_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 90 | interface Vlan\<TBD:OFFICE_VLAN_ID> | \<TBD:OFFICE_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 91 | ip address \<TBD:OFFICE_LOCAL_IP_1> 255.255.255.0 | \<TBD:OFFICE_LOCAL_IP_1> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 93 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | \<TBD:OFFICE_DHCP_SERVER> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 94 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | \<TBD:OFFICE_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 95 | address \<TBD:OFFICE_VIP> primary | \<TBD:OFFICE_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 175 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core01 | 206 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-core02 | 66 | interface Vlan\<TBD:PROD_VLAN_ID> | \<TBD:PROD_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 67 | ip address \<TBD:PROD_LOCAL_IP_2> \<TBD:PROD_MASK> | \<TBD:PROD_LOCAL_IP_2> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 67 | ip address \<TBD:PROD_LOCAL_IP_2> \<TBD:PROD_MASK> | \<TBD:PROD_MASK> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 69 | vrrp \<TBD:PROD_VRID> address-family ipv4 | \<TBD:PROD_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 70 | address \<TBD:PROD_VIP> primary | \<TBD:PROD_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 75 | interface Vlan\<TBD:DEV_VLAN_ID> | \<TBD:DEV_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 76 | ip address \<TBD:DEV_LOCAL_IP_2> \<TBD:DEV_MASK> | \<TBD:DEV_LOCAL_IP_2> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 76 | ip address \<TBD:DEV_LOCAL_IP_2> \<TBD:DEV_MASK> | \<TBD:DEV_MASK> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 78 | vrrp \<TBD:DEV_VRID> address-family ipv4 | \<TBD:DEV_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 79 | address \<TBD:DEV_VIP> primary | \<TBD:DEV_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 84 | interface Vlan\<TBD:OFFICE_VLAN_ID> | \<TBD:OFFICE_VLAN_ID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 85 | ip address \<TBD:OFFICE_LOCAL_IP_2> 255.255.255.0 | \<TBD:OFFICE_LOCAL_IP_2> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 87 | ip helper-address \<TBD:OFFICE_DHCP_SERVER> | \<TBD:OFFICE_DHCP_SERVER> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 88 | vrrp \<TBD:OFFICE_VRID> address-family ipv4 | \<TBD:OFFICE_VRID> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 89 | address \<TBD:OFFICE_VIP> primary | \<TBD:OFFICE_VIP> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 168 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-core02 | 199 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-fnacc01 | 9 | vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 12 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-fnacc01 | 19 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 25 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 37 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 44 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 51 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc01 | 59 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 10 | vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 13 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-fnacc02 | 20 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 26 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 38 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 45 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 52 | switchport access vlan \<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fnacc02 | 60 | switchport trunk allowed vlan 9,\<TBD:VLAN_OFFICE_TK_F6> | \<TBD:VLAN_OFFICE_TK_F6> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-fw01 | 9 | ip address \<TBD:OUTSIDE_IP_198.51.100.0_25> 255.255.255.128 | \<TBD:OUTSIDE_IP_198.51.100.0_25> | 回線契約・拠点間IP台帳 | 必須 |
| tk1-fw01 | 36 | route outside 0.0.0.0 0.0.0.0 \<TBD:LOCAL_ISP_GATEWAY> 1 | \<TBD:LOCAL_ISP_GATEWAY> | 回線契約・拠点間IP台帳 | 必須 |
| tk1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_INGRESS_IF> | セキュリティポリシー | 必須 |
| tk1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_SOURCE_OBJECT> | セキュリティポリシー | 必須 |
| tk1-fw01 | 38 | nat (\<TBD:NAT_INGRESS_IF>,outside) source dynamic \<TBD:NAT_SOURCE_OBJECT> \<TBD:NAT_TRANSLATED_TARGET> | \<TBD:NAT_TRANSLATED_TARGET> | セキュリティポリシー | 必須 |
| tk1-fw01 | 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | \<TBD:ACL_NAME> | セキュリティポリシー | 必須 |
| tk1-fw01 | 39 | access-list \<TBD:ACL_NAME> extended \<TBD:ACL_RULE> | \<TBD:ACL_RULE> | セキュリティポリシー | 必須 |
| tk1-fw01 | 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | \<TBD:ACL_NAME> | セキュリティポリシー | 必須 |
| tk1-fw01 | 40 | access-group \<TBD:ACL_NAME> in interface \<TBD:ACL_INGRESS_IF> | \<TBD:ACL_INGRESS_IF> | セキュリティポリシー | 必須 |
| tk1-mgmt01 | 10 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-mgmt02 | 10 | ip address \<TBD:VLAN9_MANAGEMENT_IP> 255.255.255.0 | \<TBD:VLAN9_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-rt01 | 17 | ip address \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> 255.255.255.0 | \<TBD:INTER_BLDG_LOCAL_IP_172.16.0.0_24> | 回線契約・拠点間IP台帳 | 必須 |
| tk1-rt01 | 37 | ip route 172.18.0.0 255.255.0.0 \<TBD:INTER_BLDG_REMOTE_RT_IP> | \<TBD:INTER_BLDG_REMOTE_RT_IP> | 回線契約・拠点間IP台帳 | 必須 |
| tk1-sr1acc01 | 58 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR102> | \<TBD:PROD_VLAN_LIST_TK1_SVR102> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-sr1acc01 | 87 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-sr1acc02 | 58 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR102> | \<TBD:PROD_VLAN_LIST_TK1_SVR102> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-sr1acc02 | 87 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-sr2acc01 | 59 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR202> | \<TBD:PROD_VLAN_LIST_TK1_SVR202> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-sr2acc01 | 88 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |
| tk1-sr2acc02 | 59 | switchport trunk allowed vlan \<TBD:PROD_VLAN_LIST_TK1_SVR202> | \<TBD:PROD_VLAN_LIST_TK1_SVR202> | VLAN/IPの割当表、VRRP・DHCP設計 | 必須 |
| tk1-sr2acc02 | 88 | ip address \<TBD:OOB_MANAGEMENT_IP> 255.255.255.0 | \<TBD:OOB_MANAGEMENT_IP> | VLAN9のIP管理表 | 必須 |

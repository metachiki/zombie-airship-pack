# Xaero’s Mapの探索状況共有

Minecraft 1.20.1 / Forge 47.4.29を維持して、[Xaero's Maps: Multiplayer+](https://modrinth.com/mod/xaeros-maps-multiplayer-plus)を追加する。
共有するのは地図の探索状況。ウェイポイントセットの追加・削除を自動共有する機能は作者の計画項目であり、今回の導入で利用できるとは案内していない。

## 追加と必要な更新

| MOD | 変更前 | 採用版／正式配布 |
| --- | --- | --- |
| Xaero's Maps: Multiplayer+ | なし | [1.2.4+1.20.1-forge](https://modrinth.com/mod/xaeros-maps-multiplayer-plus/version/MJNQi4lm) |
| Xaero's World Map | 1.39.12 | [1.40.2](https://modrinth.com/mod/xaeros-world-map/version/U3stuFts) |
| Xaero's Minimap | 25.2.10 | [25.3.2](https://modrinth.com/mod/xaeros-minimap/version/33Ak0hoU) |
| Kotlin for Forge | 4.11.0 | [4.12.0](https://modrinth.com/mod/kotlin-for-forge/version/Zsh14XeQ) |
| YACL | 3.6.6 | [同じ3.6.6](https://modrinth.com/mod/yacl/version/sCWgXDYQ)を維持 |
| Open Parties and Claims | 0.25.8 | 同じ0.25.8を維持 |

共有MODのJARはWorld Map 1.40以上、Minimap 25以上、Kotlin言語ローダー4.12.0、YACL 3以上を指定している。
World Map 1.40.2はMinimap 25.3.2以上を、Minimap 25.3.2はWorld Map 1.40.2以上を要求するため、両方を揃える。
XaeroLib 1.0.42は地図JARに同梱されているので別のJARは追加しない。

最新のWorld Map 1.47.0 / Minimap 26.6.0も調べたが、導入済みの土地保護MODを0.32.4以上へ更新する必要が生じる。
今回は土地保護の版と設定を維持できる1.40.2 / 25.3.2を採用した。MODの削除はなく、定義数は307から308へ増える。
以前修正した7件の取得先とBee Fixの設定は維持する。

## 専用Forgeサーバーへの導入

管理画面を読み取り確認したところ、案内されたサーバーは停止中で、起動コマンドは `bash start.sh`。
そのスクリプトは `fabric-server-launch.jar` を起動し、packwiz URLも旧 `main` ブランチを参照していた。
この状態ではForge版JARを配置するだけでは使えない。Forge 47.4.29への移行はワールドと既存MODへ影響するため、別途方針確認が必要。
サーバーのファイル・起動設定・ワールドは変更していない。以下の手順はForge環境が用意された後に適用する。

PC側のpackwiz更新だけでは、専用サーバーのMODは更新されない。以下はサーバー管理者が実施する。

1. サーバーを停止し、ワールド・設定・現在のMOD構成をバックアップする。各プレイヤーも地図データをバックアップする。
2. サーバーの `mods` に次を配置する。リンクは作者が公開するModrinth CDNの固定ファイル。

| サーバーに必要なファイル | 正式ダウンロード |
| --- | --- |
| `xmmp-1.2.4+1.20.1-forge.jar` | [ダウンロード](https://cdn.modrinth.com/data/stTaMuWa/versions/MJNQi4lm/xmmp-1.2.4%2B1.20.1-forge.jar) |
| `kotlinforforge-4.12.0-all.jar` | [ダウンロード](https://cdn.modrinth.com/data/ordsPcFz/versions/Zsh14XeQ/kotlinforforge-4.12.0-all.jar) |
| `yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar` | [ダウンロード](https://cdn.modrinth.com/data/1eAoo2KR/versions/sCWgXDYQ/yet_another_config_lib_v3-3.6.6%2B1.20.1-forge.jar) |

3. 同じMODの旧JARを重複させない。Kotlin 4.11.0は4.12.0へ置き換え、YACL 3.6.6が既にあればそのまま使う。他のMODは削除しない。
4. サーバーにWorld Map / Minimapも導入済みなら、PC側と同じ1.40.2 / 25.3.2へ揃える。共有MOD1.2.4の内部条件では、専用サーバー上のWorld Map / Minimapは任意依存だが、存在する場合には版条件を満たす必要がある。
5. サーバーを起動し、共有するプレイヤー全員が更新済みパックで接続する。通常のMOD入りサーバーへの接続では、別途スタンドアローンサーバーのアドレスやポートを設定する必要はない。
6. 2人が別々の場所を探索し、お互いのWorld Mapへ反映されることを確認する。

サーバー本体への配置・起動と2人での実際の同期確認は別途必要。
公開範囲などの設定は作者の[公式説明](https://github.com/Alinco8/XaerosMaps-MultiplayerPlus)と、サーバー起動時に生成される設定に従う。

更新前の地図データは、インスタンス内の `XaeroWorldMap`、`XaeroWaypoints`、`xaero`（存在するフォルダー）をコピーして保管する。
packwizへ地図データや個人のウェイポイントは登録しない。

## 検証

- 4件の追加・更新はModrinth公式APIが返す固定URLとバージョンIDを使用。実ファイルのSHA-1・SHA-512・サイズ一致を確認。
- 既存YACL / Open Parties and Claimsの同一ファイルも取得して確認。
- JAR内の依存条件を読み取り、Forge 47.4.29 / Minecraft 1.20.1、Kotlin言語ローダー、地図同士、YACL、土地保護MOD、同梱XaeroLibの範囲がすべて整合することを確認。
- 元の307件を保持し、変更対象が上記3件と新規1件のみであることを基準コミット `5a73480` と比較。
- `packwiz refresh` 後の全インデックスハッシュとパックハッシュを検証。
- bootstrap.jar / installer v0.5.14を使い、旧版構成を再現した隔離パックから更新。共有MODと3件の更新を自動取得し、旧3JARが置き換わって重複しないことを確認。次回起動も正常終了。
- [実行ログ](xaero-map-sharing-install.log)。取得テスト用の最小構成では、旧版・未変更のサポートMODを同一ハッシュの正式Modrinthファイルへ向けて、CurseForge APIの影響を分離した。本番でYACL / Open Parties and Claimsの設定を変更したわけではない。
- Minecraft本体の起動や2人の実プレイによる同期は、この取得・依存条件テストには含まれない。

再検証（Python 3.11以上）:

```powershell
python scripts/verify_map_sharing.py
python scripts/verify_map_sharing.py --download-dir ../map-sharing-verified
```

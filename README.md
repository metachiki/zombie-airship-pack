# Zombie Airship Pack

Packwiz metadata for a Minecraft 1.20.1 Forge modpack.

- Forge: 47.4.29
- Mod metadata files: 307

This repository tracks Packwiz metadata: `pack.toml`, `index.toml`, and the files in `mods/`. Mod JARs are excluded from Git. The original Forge definitions were matched to fixed CurseForge project and file IDs; seven download entries now use byte-identical files from the authors' Modrinth projects.

## Working with the pack

After installing Packwiz, run these commands from the repository root:

```powershell
packwiz refresh
packwiz curseforge export
```

Review any proposed version changes before using `packwiz update`.

## PrismLauncherで友達と共有する

この変更を `forge-packwiz-conversion` に取り込んだ後、Minecraft **1.20.1 / Forge 47.4.29** のインスタンスで使用してください。

1. インスタンスのMinecraftフォルダー（`options.txt` と同じ場所）に、[公式のpackwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases)を置きます。
2. インスタンスの「編集」→「設定」→「カスタムコマンド」で、起動前コマンドに次を設定します。

```text
"$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/metachiki/zombie-airship-pack/forge-packwiz-conversion/pack.toml
```

3. 起動すると公開済みのパック構成を確認し、必要なMODを導入・更新します。

今回報告された8種類のうち7種類は、同一バージョン・同一SHA-1のModrinth配布ファイルへ切り替えました。**Bee Fixだけは初回に手動導入が必要です。** [指定ファイルの公式ページ](https://www.curseforge.com/minecraft/mc-mods/bee-fix/files/4618962)から `BeeFix-1.20-1.0.7.jar` を入手し、同じインスタンスのMinecraftフォルダー内の `mods` に置いてから再起動してください。同一ファイルがあればインストーラーが認識します。

友達には、Minecraft/Forgeと上記コマンドを設定したインスタンスをエクスポートして共有できます。MOD JAR・ワールド・個人設定を含めず、各自が正式配布元から取得する構成にしてください。Bee Fixは各自が上記手順で一度導入します。

[8種類の監査結果・残る制約・検証手順](docs/mod-download-audit.md)を参照してください。今回の取得テストは対象7種類の導入と再起動、および手動配置したBee Fixの認識までです。全307種類を揃えたMinecraftの起動確認は含みません。

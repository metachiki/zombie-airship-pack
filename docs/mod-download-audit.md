# 自動ダウンロード失敗8種類の監査

監査日: 2026-11-09（日本時間）。基準: `forge-packwiz-conversion` の `b572b5b`。
Minecraft 1.20.1 / Forge 47.4.29、307件のMOD定義を維持。

## 結果

7件の取得先を、作者のModrinthプロジェクトが公開する固定バージョンのCDN URLへ変更した。
APIが返すURL・プロジェクトID・バージョンIDを使用し、手作りのCurseForge CDN URLやミラーは使っていない。
元の `name`、`filename`、`side`、SHA-1はすべて維持した。
`[update.modrinth]` で更新元を記録し、`packwiz refresh` でパックのハッシュ連鎖を更新した。
JARをこのリポジトリに追加・再配布していない。

| MOD | 元のファイル／固定バージョン | 取得元・結果 |
| --- | --- | --- |
| Shots Fired | `shotsfired-1.20.1-0.2.2.jar` | [Modrinth VMWLdrAh](https://modrinth.com/mod/shots-fired/version/VMWLdrAh)、自動取得成功 |
| Plushie Buddies | `plushie_buddies-0.1.6-1.20.1.jar` | [Modrinth SlbwzuEh](https://modrinth.com/mod/plushie-buddies/version/SlbwzuEh)、自動取得成功 |
| Refined Storage (Fixes) Mixin | `MCT-RS-Mixin-1.20.1-1.0.0-b400-release.jar` | [Modrinth 34zUr1lG](https://modrinth.com/mod/mct-refined-storage-mixin/version/34zUr1lG)、自動取得成功 |
| Immersive Fixes | `immersivefixes-1.0.3-all.jar` | [Modrinth 3ZLqbGsf](https://modrinth.com/mod/immersive-fixes/version/3ZLqbGsf)、自動取得成功 |
| GPUTape | `GPUTape-1.18x-1.21x-1.0.5.1-forge.jar` | [Modrinth mMc55fB1](https://modrinth.com/mod/gputape/version/mMc55fB1)、自動取得成功 |
| Entity Culling Fabric/Forge | `entityculling-forge-1.9.4-mc1.20.1.jar` | [Modrinth GpUlMGON](https://modrinth.com/mod/entityculling/version/GpUlMGON)、自動取得成功 |
| Builder's Delight (Forge) | `BuildersDelight-1.20.1-v.1.3.jar` | [Modrinth o5hPmXN6](https://modrinth.com/mod/builders-delight/version/o5hPmXN6)、自動取得成功 |
| Bee Fix | `BeeFix-1.20-1.0.7.jar` | [CurseForge 4618962](https://www.curseforge.com/minecraft/mc-mods/bee-fix/files/4618962)、元の設定を維持、手動導入 |

### 配布元の確認

Modrinthのプロジェクト・チームAPIとJAR内の作者情報を照合した。移行7件は、MelodicCougar7（Shots Fired / Immersive Fixes）、Subthy（Plushie Buddies）、tgstyle（Refined Storage Mixin）、Mr.Toad（GPUTape）、tr7zw（Entity Culling）、Tynoxs（Builder's Delight）の公開プロジェクトに対応する。
API: `https://api.modrinth.com/v2/version_file/<元のSHA-1>?algorithm=sha1`、`/version/<version-id>`、`/project/<project-id>`、`/team/<team-id>/members`。

GPUTapeのプロジェクトの現在の表示名はGPUBoosterだが、採用したのは過去の固定版 `1.0.5.1-forge`。
CDNのファイル名には `-forge` がないものの、元のJARとSHA-1が一致する。インストール先名には元の `-forge.jar` を維持し、重複導入を避けた。
Builder's Delightは配布ファイル名が `v.1.3`、Modrinthの版名とJAR内部の版名が `1.2.1` だが、元のCurseForge指定ファイルと同一SHA-1なので版の置換ではない。

Bee Fixにも同一SHA-1の[Modrinth公開](https://modrinth.com/mod/the-bee-fix/version/zbKx0iEX)がある。
ただし公開チームは `gbird84` で、元作者MacTso / Lupicusによる公式配布であることを確認できなかったため、今回は採用していない。無許可であると断定するものではない。
[公式CurseForgeページ](https://www.curseforge.com/minecraft/mc-mods/bee-fix)が示す[作者のGitHub](https://github.com/Lupicus/BeeFix)も調べたが、リリースは空で、同一JARの配布を確認できなかった。
ライセンスはMITだが、今回の「正式配布元を使用する」方針に従い保留した。

## 同一ファイルの照合

移行7件は公式CDNから実ファイルを取得し、元メタデータのSHA-1、Modrinth APIのSHA-512とサイズにすべて一致した。
Bee Fixの候補も調査用に同一ハッシュを確認したが、移行には使用していない。

| MOD | 維持した元のSHA-1 |
| --- | --- |
| Shots Fired | `f5ba631f02cd9df539417b0be4393a81e00ed0e0` |
| Plushie Buddies | `fc36e0ab5f15fad50ce933c5095a8e8bcf057990` |
| Refined Storage Mixin | `e5fcaa67c9e00c78293fc718716f630e8d561ad7` |
| Immersive Fixes | `e9db8df6d62eedbd49ef0c03cb9d6f71f909be67` |
| GPUTape | `db4a84db628dd668e08898e42e881615d34f0629` |
| Entity Culling | `2b19c5c38f88285aed2aad6a61eb622003540ee5` |
| Builder's Delight | `ad9053d0711da8157f6dbe2cc7083f17fe7aa831` |
| Bee Fix（変更なし） | `0eba7daf8b460a78375f9d3944e744ce5060d394` |

## Forge / Minecraft互換条件

移行7件すべてがModrinthでForge / 1.20.1として公開されていることを確認し、JAR内の `META-INF/mods.toml` も確認した。いずれも `javafml`。

| MOD | FML loaderVersion | Forge依存範囲 | Minecraft依存範囲 |
| --- | --- | --- | --- |
| Shots Fired | `[47,)` | `[47,)` | `[1.20.1,1.21)` |
| Plushie Buddies | `[47,)` | `[47.1.3,)` | `[1.20.1,1.21)` |
| Refined Storage Mixin | `[47,)` | `[47,)` | `[1.20.1,1.21)` |
| Immersive Fixes | `[47,)` | `[47,)` | `[1.20.1]` |
| GPUTape | `[37,56)` | `[37,56)` | `[1.18,1.22)` |
| Entity Culling | `[28,)` | 個別指定なし | `1.20.1` |
| Builder's Delight | `[47,)` | `[47,)` | `[1.20.1,)` |
| Bee Fix（参考） | `[46,)` | `[46,)` | `[1.20,1.21)` |

Forge 47.4.29 / Minecraft 1.20.1は各条件に含まれる。Bee FixはModrinth表記が1.20のみだが、元の[公式CurseForgeファイル](https://www.curseforge.com/minecraft/mc-mods/bee-fix/files/4618962)は1.20.1を明示し、内部条件も含む。
これは配布元変更による互換性維持の確認であり、全MODの相互動作やゲームプレイを保証するテストではない。

## 実行した検証

- クローン直後に元の `pack.toml → index.toml → 各ファイル` のハッシュがすべて正しいことを確認。
- `packwiz refresh` 後の全インデックスハッシュを再計算して検証。
- 基準コミットと比較し、307件のMOD定義の追加・削除なし、対象外のMOD変更なし、全対象の元ファイル名・SHA-1・side維持を検証。
- 移行7件のAPI/CDN取得、SHA-1 / SHA-512 / サイズ、Forgeメタデータを検証。
- 使用中のbootstrap.jarからinstaller **v0.5.14**を取得し、変更済み7件のメタデータだけをそのまま複製した最小パックで実行。空のインスタンスへの7件の自動導入、2回目の起動とも終了コード0。
- 続けて元のBee Fix定義を検証用パックに加え、同一SHA-1のJARを検証用インスタンスの `mods` に配置。`Bee Fix already exists (validated)` となり、8件すべてを維持して終了コード0。
- [インストーラーログ](installer-smoke-test.log)。ゲーム本体と全307件の起動、実際のPrismLauncher画面操作は未実施。

ローカルの全体ハッシュ検証（Python 3.11以上）:

以下はコミット `71032ac` 時点の監査再現用。後続の地図共有MOD追加後は、[地図共有の検証手順](xaero-map-sharing.md#検証)を使用する。

```powershell
packwiz refresh
python scripts/verify_official_downloads.py
```

公式配布ファイルを再取得して検証（JAR保存先はリポジトリの外にする）:

```powershell
python scripts/verify_official_downloads.py --download-dir ../verified-downloads
```

`docs/` と `scripts/` は `.packwizignore` でインスタンスへの配信対象から除外した。
既存の `resourcepacks/` 内3定義と `shaderpacks/` 内1定義は元のForgeインデックスに含まれていなかった。`packwiz refresh` で意図せず有効化されないよう、その4パスも明示的に除外した。元ファイルは保持し、インデックスの配信対象集合は基準コミットと同一であることを検証した。

## Bee Fixを手動導入する方法

1. [公式の指定ファイルページ](https://www.curseforge.com/minecraft/mc-mods/bee-fix/files/4618962)から **BeeFix-1.20-1.0.7.jar** を取得する。別の1.20.6版や1.21版は選ばない。
2. PrismLauncherで対象インスタンスのフォルダーを開き、Minecraftフォルダー（`options.txt` がある場所）内の `mods` に保存する。
3. 必要ならPowerShellで確認する。SHA-1は上の表と一致する必要がある。

```powershell
Get-FileHash -Algorithm SHA1 -LiteralPath .\mods\BeeFix-1.20-1.0.7.jar
```

4. 再起動またはインストーラーの再試行を行う。指定ファイルが存在すれば認識され、その後の起動でもそのまま使用できる。JARを消した場合や将来指定版を変えた場合は再取得が必要。

他のMODで今後API除外エラーが出た場合も、画面に表示される正式な指定ファイルページから取得し、表示される保存先・ファイル名に合わせる。今回の残り299種類は配布元を変更していない。

友達への共有は[packwiz公式の起動前コマンド方式](https://packwiz.infra.link/tutorials/installing/packwiz-installer/)を使う。Bee Fixは各自が一度取得する必要があるため、完全な初回無操作導入にはまだ至っていない。
完全自動化には元作者が確認できる正式なAPI配布先を公開するか、既存Modrinth公開の作者との関係を確認する必要がある。MOD削除や別バージョン採用は行っていない。

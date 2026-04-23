# Arcade Angel Project Status (Miko Edition)

## 1. 現状のステータス (Current Status)
Arcade Angel は現在、プロダクション品質の安定状態にあります。
RGBA アセットパイプラインへの完全移行により、透明度の描画不具合が解消され、慣性ベースの物理演算（物理揺れ）が安定稼働しています。

## 2. 完了した主要マイルストーン (Key Milestones)
- **RGBA PNG パイプライン**:
  - 従来のカラーキー（グリーン抜き）方式から、ネイティブ透過 PNG (Base64) へ完全に移行。
  - `processAlpha` シェーダーを廃止し、レンダリング負荷の低減と画質の向上を実現。
- **物理演算 (Hair Physics)**:
  - 髪の揺れに `stiffness (0.08)` と `damping (0.85)` の黄金比を適用。
  - 頭の動きに連動した自然な慣性運動を実装済み。
- **黄金比の顔面配置**:
  - v0.15.118 で確立された黄金比（目の位置、眉の高さ、グローバルスケール）をデフォルトとして固定。
- **天狐 (Tenko) モード & Miko 衣装**:
  - 三つの衣装（CYBER, GOTHIC, MIKO）の切り替えと、天狐の耳の動的レンダリングを統合。

## 3. 主要ファイル (Core Files)
- [index.html](./index.html): 最新の安定版。`dev.html` から `release.py` を通じて生成されます。
- [dev.html](./dev.html): 開発・検証用ファイル。すべての新機能はこのファイルでテストされます。
- [version_history_dev.json](./version_history_dev.json): 開発版の詳細な変更履歴。

## 4. 運用ルール (The Ritual)
1. **開発は必ず `dev.html` で行う**。
2. **本番公開時は `python3 release.py` を実行する**。これにより `index.html` への同期、バックアップ作成、GitHub へのプッシュが自動で行われます。
3. **コミュニケーションと言語**: 開発プロセス、TODO管理、およびエージェントとの対話は原則として**日本語**で行われます。

---
*最終更新: 2026-04-23 16:38:00 (v0.16.2)*

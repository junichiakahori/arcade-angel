# 🎮 Arcade Angel - Portable Puppet System

![Version](https://img.shields.io/badge/version-v0.15.124-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Arcade Angel** は、ブラウザ1つで動作する、高機能・高画質なアニメスタイル・デジタルパペットシステムです。

## 🌟 特徴 (Features)

- 📦 **完全ポータブル設計**: 画像・音声アセットをすべてBase64でHTMLに埋め込み済み。インターネット環境や外部サーバーがなくとも、HTMLファイル1つでどこでも起動可能です。
- 🧬 **高度なフェイストレッキング**: MediaPipe FaceMeshを採用し、滑らかな口パク（母音追従）、ウィンク、首の回転をリアルタイムで実現。
- 🎀 **独自開発 髪の物理演算**: 静止画パペットでありながら、ツインテールが頭の動きに合わせて揺れる「物理演算風遅延システム」を搭載。
- 🦊 **天狐 (Tenko) モード**: 北九州・魚町の守り神、天狐ちゃんへの変身機能を搭載。
- 🎥 **OBS配信特化**: クロマキー（グリーンバック）および透過背景モードをワンクリックで切り替え可能。OBSブラウザソースで背景透過のままストリーミングができます。

## 🚀 クイックスタート (Quick Start)

1.  `dev.html` をブラウザ（Chrome推奨）で開きます。
2.  画面中央のオーバーレイをクリックして、カメラとマイクの使用を許可してください。
3.  カメラが正常に読み込まれると、あなたに合わせてパペットが動き出します。

> **Note**: ローカルファイルのセキュリティ制限により、カメラが起動しない場合は、以下のコマンドでローカルサーバーを立ち上げてください。
> ```bash
> python3 -m http.server
> ```
> その後、 `http://localhost:8000/dev.html` にアクセスしてください。

## ⚙️ 調整パネル (Control Panel)

右側の設定パネルから以下の調整が可能です：
- **GLOBAL SCALE**: パペットの表示サイズ
- **HAIR LAG**: ツインテールの揺れ具合（物理演算）の強度
- **SMILE SENS**: 笑顔の反応感度
- **BG MODE**: 通常背景 / クロマキー / 透過の切り替え（OBS用）

## 🛠 テクノロジー (Tech Stack)

- **Logic**: JavaScript (ES6+)
- **Tracking**: [MediaPipe FaceMesh](https://google.github.io/mediapipe/solutions/face_mesh)
- **Styling**: Vanilla CSS / Glassmorphism UI
- **Portability**: Base64 Asset Embedding System

---

## 🎨 キャラクターについて (Character)

**魚町天狐 (Uomachi Tenko)**
北九州市小倉北区「魚町」周辺を守護する天狐をモチーフにしたデジタルパペット。アーケードの守護天使として、あなたの配信活動をサポートします。

---

## ⚖️ ライセンス (License)

Copyright © 2026 junichiakahori.
This project is licensed under the MIT License.

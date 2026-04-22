# Arcade Angel - Portable Anime Puppet

![Arcade Angel](https://img.shields.io/badge/Version-v0.15.118_%28Stable%29-00F0FF?style=for-the-badge)
![Unit Status](https://img.shields.io/badge/Status-Restored_&_Aesthetic-ff69b4?style=for-the-badge)

High-fidelity, browser-based anime puppet with real-time facial tracking and physics. Built for streamers and interactive experiences.

## ✨ Features

- **Real-time Face Tracking**: Powered by MediaPipe Face Mesh for fluid expressions and movement.
- **Independent Eye Logic**: Supports asymmetrical winks and gaze tracking.
- **Dynamic Physics**: Natural hair lag and breathing animations.
- **Portable & Lightweight**: Single-file HTML execution with Base64 embedded assets.
- **Streamer Ready**: Integrated Chroma Key (Green Screen) and Transparency modes for OBS.
- **Costume Switching**: Includes Standard, Gothic, and the new **Uomachi Tenko Miko Edition**.

## 🚀 Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/junichiakahori/arcade-angel.git
    ```
2.  **Run a local server**:
    ```bash
    python3 -m http.server
    ```
3.  **Open in Browser**:
    Visit `http://localhost:8000/index.html` for the stable version, or `dev.html` for the latest features.

## 🛠 Calibration Guide

- **Golden Ratio**: The default proportions (v0.15.118) are optimized for a "Cute" aesthetic. Use the **EMERGENCY RESET** button in `dev.html` to return to these values.
- **Smile Sensitivity**: Adjust the SMILE SENS slider to calibrate the auto-happy expression based on your camera quality.
- **OBS Integration**: Use "Window Capture" in OBS with the Chroma Key filter or direct transparency support.

## 📜 Version History

See [version_history.json](version_history.json) for the stable production log and [version_history_dev.json](version_history_dev.json) for the experimental development track.

---
*Created by Antigravity AI for the Arcade Angel project.*

# 🎨 Art-In-The-Air

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)

**Art-In-The-Air** is a touchless digital canvas that lets you draw on your screen using only hand gestures. Powered by computer vision, it tracks your fingertips in real-time, allowing for a futuristic and hygienic way to create art.

---

## 📸 Demo

![air canvas](https://github.com/user-attachments/assets/fae1104f-7684-4ad7-8d8c-f9606dffabc9)

---
## ✨ Features

* **👆 AI Hand Tracking:** Uses Google's MediaPipe to detect hand landmarks with high precision.
* **🎨 Virtual Toolbar:** Select colors (Purple, Blue, Green, Yellow) by simply "touching" them in the air.
* **🧽 Eraser Mode:** Switch to the eraser tool to correct mistakes.
* **🖱️ Intuitive Gestures:**
    * **Index Finger Up:** Draw Mode.
    * **Two Fingers Up:** Selection/Hover Mode (stops drawing).
* **🖥️ Modern UI:** Features a semi-transparent interface and active selection highlights.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/mariamanbar/Art-In-The-Air.git](https://github.com/mariamanbar/Art-In-The-Air.git)
    cd Art-In-The-Air
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    python air_canvas.py
    ```

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **Index Finger** | Draw lines |
| **Index + Middle** | Hover / Select Colors |
| **'C'** | Quit the application |
| **'Q'** | Clear the canvas |

# 🐛 LarvaTrackAI

## **A Pipeline for Larvae Video-Based Classification and Analysis**

LarvaTrackAI is a cutting-edge video processing pipeline designed for entomology research. It automates larvae tracking, motion analysis, and dataset preparation, enabling efficient feature extraction for statistical and machine learning applications.

---

## 📚 Table of Contents

- [🚀 Features](#features)
- [📥 Installation](#installation)
- [🛠️ Usage](#usage)
- [🔮 Future Scope](#future-scope)
- [🤝 Contributing](#contributing)
  - [✅ What You Can Contribute](#what-you-can-contribute)
  - [🚫 What’s Not Allowed](#whats-not-allowed)
  - [📌 How to Contribute](#how-to-contribute)
- [🛡️ License](#license)
- [✨ Get Started Now!](#get-started-now)

---

## 🚀 Features

🎞️ **Comprehensive Preprocessing** – Filters, enhances, and prepares larvae movement videos for analysis.\
📍 **Automated Tracking & Feature Extraction** – Detects larvae movement, tracks trajectories, and extracts behavioral metrics.\
🔬 **Optimized for Entomology** – Specifically tailored for insect behavioral research, aiding biologists and researchers.\
🖥️ **User-Friendly Interface** – Built with **Streamlit**, offering an interactive and easy-to-use UI for data processing.

---

## 📥 Installation

To install and run **LarvaTrackAI** locally, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/Calibourne/LarvaTrackAI.git
   cd LarvaTrackAI
   ```

2. **Set up a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
   **Alternatively, if using Anaconda:**
   ```bash
   conda create --name larvatrackai python=3.8
   conda activate larvatrackai
   ```

3. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit application**

   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Usage

📤 **Upload** a video containing larvae movement.\
⚙️ **Select preprocessing parameters** – Adjust background extraction, noise filtering, and enhancement settings.\
🔄 **Process the video** – Extract motion-based features, generate tracking data, and export results.\
📥 **Download the processed output** – Obtain video overlays or feature datasets for further statistical or machine learning analysis.

---

## 🔮 Future Scope

LarvaTrackAI is actively evolving, with upcoming improvements including:

🚀 **Advanced Motion Analysis** – Fine-grained tracking enhancements and behavior pattern detection.\
📊 **Expanded Dataset Support** – Increased adaptability for various larvae species and experimental conditions.\
📡 **Real-Time Visualization** – Interactive plots and graphical insights for deeper larvae movement analysis.\
🧠 **Basic Machine Learning Integration** – Supporting feature export to common ML libraries like **scikit-learn**, allowing users to apply classification and clustering techniques without requiring GPU resources.

📝 **Note:**\
This tool is designed primarily for **data preprocessing and feature extraction** to support machine learning workflows. Users needing model training should export processed data and use external ML frameworks as needed. Deep learning frameworks requiring GPU acceleration are not natively supported within the Streamlit application.

---

## 🤝 Contributing

We welcome contributions that **enhance LarvaTrackAI**! However, please adhere to the following guidelines:

### ✅ What You Can Contribute:

🛠️ **Improved Preprocessing Pipelines** – Enhance video processing efficiency and accuracy.\
📍 **Feature Extraction Upgrades** – Develop new motion tracking algorithms and behavioral metrics.\
⚡ **Performance Optimizations** – Speed up processing and reduce computational overhead.\
🐞 **Bug Fixes & Code Refinements** – Identify and fix existing issues to improve overall stability.

### 🚫 What’s Not Allowed:

⚠️ **Rebranding or Repackaging** – Do not redistribute LarvaTrackAI under a different name.\
💰 **Commercial Use Without Permission** – Commercial deployments require explicit approval.\
🔒 **Closed-Source Modifications** – All modifications must remain **GPLv3 licensed** and open-source.

### 📌 How to Contribute:

1. **Fork** the repository.
2. **Create a feature branch:**
   ```bash
   git checkout -b feature-branch  
   ```
3. **Commit changes and push:**
   ```bash
   git push origin feature-branch
   ```
4. **Submit a pull request** for review.

---

## 🛡️ License

LarvaTrackAI is licensed under **GNU General Public License v3.0 (GPLv3)**.

📜 **You may:** Use, modify, and distribute the software under the same **GPLv3** license.\
⛔ **You may not:** Commercially redistribute or repackage the software without explicit permission.\
📢 **You must:** Ensure that any modifications remain **open-source under GPLv3**.

For full details, see the [LICENSE](LICENSE) file.

---

## ✨ Get Started Now!

👩‍🔬 Whether you're an entomologist, bioinformatics researcher, or ML enthusiast, **LarvaTrackAI** simplifies larvae motion analysis like never before! Try it out today and contribute to its continuous evolution. 🐛✨


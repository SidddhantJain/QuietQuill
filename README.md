<div align="center">
  <img src="https://img.shields.io/badge/Machine%20Learning-Music%20Genre%20Classification-blueviolet" alt="ML Music Genre Classification" />
  <h1>🎵 ML Music Genre Classification 🎶</h1>
  <p>
    <b>Predict music genres using machine learning and audio feature extraction</b><br>
    <i>Built with Python, scikit-learn, XGBoost, and GTZAN dataset</i>
  </p>
</div>

---

## 🚀 Overview

ML Music Genre Classification is a cutting-edge machine learning project that classifies music tracks into genres using advanced audio features. Leveraging the GTZAN dataset, this project extracts features from `.wav` files and trains multiple models to predict genres such as <b>blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, and rock</b>.

---

## 📂 Project Structure

```
ML_Music_genra/
├── app.py                  # Main application (inference/demo)
├── download_gztan.py       # Script to download GTZAN dataset
├── extract_features.py     # Feature extraction from audio files
├── train_models.py         # Model training scripts
├── utils/
│   └── feature_extraction.py
├── models/                 # Saved models (pkl files)
├── scaler/                 # Scaler objects
├── Data/
│   ├── genres_original/    # Raw audio files
│   ├── images_original/    # Spectrogram images
│   └── features_*.csv      # Extracted features
├── ML_music_genra.ipynb    # Jupyter notebook for EDA & experiments
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## 🧑‍💻 Features

- 🎼 **Audio Feature Extraction:** MFCCs, chroma, spectral contrast, tonnetz, and more
- 🤖 **Multi-Model Training:** Random Forest, KNN, XGBoost
- 🎧 **Genre Prediction:** Predicts 10 genres from GTZAN dataset
- 🛠️ **Scalable Pipeline:** Modular scripts for data, features, and models
- 📊 **Jupyter Notebook:** For EDA, visualization, and experimentation

---

## 📊 Notebooks

- **ML_music_genra.ipynb:** Explore data, visualize features, and experiment with models interactively.

---

## 📦 Dependencies

- Python 3.8+
- numpy, pandas, scikit-learn
- xgboost, librosa, matplotlib, seaborn

---

## 📚 References

- [GTZAN Genre Collection](http://marsyas.info/downloads/datasets.html)
- [Librosa Documentation](https://librosa.org/doc/latest/index.html)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
  <b>Made with ❤️ by Siddhant Jain</b>
</div>
---

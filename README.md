#  🍽️ Food Recommendation System

A hybrid deep learning-based restaurant recommendation system built on the **Yelp Open Dataset**, combining Sentiment Analysis (BERT), Collaborative Filtering, and Content-Based Filtering to deliver personalised restaurant suggestions.

---

## 📌 Overview

This project implements the paper:
> *"A Hybrid Restaurant Recommendation System Using Sentiment Analysis"*

The system analyses user reviews using BERT, extracts restaurant features via Word2Vec embeddings, and fuses three recommendation signals through NMF + Decision Tree Regression to predict personalised star ratings.

---

## 🏗️ Architecture

```
Raw Reviews (Yelp Dataset)
        │
        ▼
┌─────────────────────────────────────────────┐
│           Preprocessing Pipeline            │
│  Tokenization → Stopword Removal → POS      │
│  Tagging → Lemmatization (NLTK + WordNet)   │
└────────────────────┬────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌──────────┐
   │  BERT   │  │   CF    │  │   CB     │
   │Sentiment│  │Collab   │  │Content   │
   │Analysis │  │Filter   │  │Based     │
   └────┬────┘  └────┬────┘  └────┬─────┘
        │            │            │
        └────────────┼────────────┘
                     ▼
         ┌──────────────────────┐
         │  MinMaxScaler [1,5]  │
         │  NMF (2 components)  │
         │  Decision Tree Reg.  │
         └──────────┬───────────┘
                    ▼
         Top-N Restaurant Recommendations
```

---

## ⚙️ Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.x |
| Deep Learning | PyTorch, HuggingFace Transformers (BERT) |
| ML / Stats | scikit-learn, scipy, numpy, pandas |
| NLP | NLTK, Gensim (Word2Vec), AFINN, TextBlob, VADER |
| Visualisation | Matplotlib, Seaborn |
| Dataset | Yelp Open Dataset (5,000 restaurant reviews) |

---

## 🔬 Models Evaluated

**Sentiment Analysis**
- AFINN · TextBlob · VADER · BERT ✅ *(best)*

**Collaborative Filtering**
- Cosine Similarity · MSD · Pearson Correlation

**Dimensionality Reduction**
- PCA ✅ *(selected — higher Trustworthiness)* · Isomap

**Hybrid Regression**
- NMF + Decision Tree ✅ · NMF + Random Forest
- NMF + Gradient Boosting · NMF + SVR
- Standalone DTR/RFR/GBR/SVR · Weighted Hybrid

---

## 📊 Key Results

| Model | RMSE |
|-------|------|
| **NMF + Decision Tree Regressor** | **1.1955** ✅ |
| NMF + Random Forest | 1.2340 |
| NMF + Gradient Boosting | 1.2600 |
| Weighted Hybrid (baseline) | 1.4200 |

BERT Sentiment Accuracy: **94.8%** · F1: ~0.94

---

---

## 🧠 Cold Start Handling

New users with no review history are handled gracefully:
- **CF score** → falls back to dataset global mean
- **CB score** → cluster-based, works without user history
- **BERT score** → restaurant-level sentiment, always available

Result: new users receive **popularity-based recommendations** that personalise over time as reviews accumulate.


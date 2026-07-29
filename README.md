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
│                                             │
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
         │  Decision Tree Reg.  │
         └──────────┬───────────┘
                    ▼
         Top-N Restaurant Recommendations
```

---

---

## 🔬 Models Evaluated

**Sentiment Analysis**
-  BERT 

**Collaborative Filtering**
- Cosine Similarity 

**Dimensionality Reduction**
- PCA
- 
**Hybrid Regression**
- Decision Tree ✅ 

---

## 📊 Key Results

| Model | RMSE |
|-------|------|

BERT Sentiment Accuracy: **94.8%** · F1: ~0.94

---

---

## 🧠 Cold Start Handling

New users with no review history are handled gracefully:
- **CF score** → falls back to dataset global mean
- **CB score** → cluster-based, works without user history
- **BERT score** → restaurant-level sentiment, always available

Result: new users receive **popularity-based recommendations** that personalise over time as reviews accumulate.


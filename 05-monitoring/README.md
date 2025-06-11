# 📊 Data Drift: What It Is and Why It Matters

## What is Data Drift?

**Data drift** occurs when the statistical distribution of input data changes over time compared to the data a machine learning model was originally trained on.

There are two main types:

- **Covariate Shift (Feature Drift):**  
  The distribution of input features changes.  
  _Example:_ A model trained on mostly desktop users now receives more mobile user data.

- **Concept Drift (Target Drift):**  
  The relationship between input features and the target variable changes.  
  _Example:_ User click behavior patterns change due to seasonality or trends.

---

## Why Does Data Drift Matter?

- ⚠️ **Model Degradation:**  
  Predictions become less accurate as the model encounters unfamiliar data patterns.

- 🧪 **Monitoring is Critical:**  
  Without detection, drift can silently impact business decisions or user experience.

- 🔄 **Trigger for Retraining:**  
  Drift can indicate the need to update or retrain your model with new data.

## This Repository

In this repository, we demonstrate a batch processing approach for monitoring data drift in a machine learning model using the NYC taxi dataset. We leverage:

- **Evidently** for generating data drift reports  
- **Adminer** for storing and managing data in PostgreSQL  
- **Grafana** for building a dynamic drift monitoring dashboard

This setup enables effective exploration and visualization of drift patterns across time.

---
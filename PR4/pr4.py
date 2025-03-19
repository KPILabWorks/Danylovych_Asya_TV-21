import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs

# Генерація синтетичних даних з 3 кластерами
np.random.seed(42)
X, _ = make_blobs(n_samples=365, centers=3, cluster_std=25, random_state=42)
data = pd.DataFrame({
    'date': pd.date_range(start='2025-01-01', periods=365, freq='D'),
    'consumption': X[:, 0] * 50 + 500  # Масштабування до реальних значень
})
data.set_index('date', inplace=True)

# Масштабування даних для алгоритмів
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[['consumption']])

# ------------------------------------------------------------
# Hidden Markov Model (HMM) для часових рядів
# ------------------------------------------------------------
model_hmm = hmm.GaussianHMM(
    n_components=3,        # Кількість прихованих станів
    covariance_type="diag", # Діагональна коваріаційна матриця
    n_iter=200,            # Кількість ітерацій EM-алгоритму
    random_state=42
)
model_hmm.fit(data_scaled)  # Навчання моделі
hmm_states = model_hmm.predict(data_scaled)  # Прогноз станів
data['HMM_State'] = hmm_states

# ------------------------------------------------------------
# Кластеризація K-Means
# ------------------------------------------------------------
kmeans = KMeans(
    n_clusters=3,       # Кількість кластерів
    random_state=42,
    n_init=10           # Кількість ініціалізацій
)
data['KMeans_Cluster'] = kmeans.fit_predict(data_scaled)

# ------------------------------------------------------------
# Кластеризація DBSCAN
# ------------------------------------------------------------
dbscan = DBSCAN(
    eps=0.7,            # Максимальна відстань між точками
    min_samples=5       # Мінімальна кількість сусідів
)
data['DBSCAN_Cluster'] = dbscan.fit_predict(data_scaled)

# ------------------------------------------------------------
# Візуалізація результатів
# ------------------------------------------------------------
fig, ax = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# Налаштування графіків
titles = [
    "Приховані стани (HMM)",
    "Кластеризація K-Means",
    "Кластеризація DBSCAN"
]

for i, (title, col) in enumerate(zip(titles, ['HMM_State', 'KMeans_Cluster', 'DBSCAN_Cluster'])):
    scatter = ax[i].scatter(
        data.index,
        data['consumption'],
        c=data[col],
        cmap='viridis',
        s=20,
        alpha=0.8
    )
    ax[i].set_title(title, fontsize=12)
    plt.colorbar(scatter, ax=ax[i], label='Кластер/стан')

plt.xlabel("Дата", fontsize=10)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Прогноз наступного стану за HMM
# ------------------------------------------------------------

next_state = model_hmm.predict(data_scaled[-1].reshape(1, -1))
print(f"Прогнозований наступний стан системи (HMM): {next_state[0]}")

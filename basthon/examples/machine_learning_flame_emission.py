import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

rng = np.random.default_rng(7)
rows = []
for ion, centre in {"Na": [88, 13, 12], "Li": [14, 86, 11], "K": [12, 14, 90]}.items():
    for replicate in range(20):
        signals = rng.normal(centre, [3.0, 3.0, 3.0])
        rows.append([f"{ion}_{replicate + 1:02d}", *signals, ion])

data = pd.DataFrame(rows, columns=["sample_id", "emission_589_nm", "emission_671_nm", "emission_766_nm", "ion"])
features = data[["emission_589_nm", "emission_671_nm", "emission_766_nm"]]
labels = data["ion"]
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.30, random_state=42, stratify=labels
)

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"Test accuracy: {accuracy_score(y_test, predictions):.3f}")
ConfusionMatrixDisplay.from_predictions(y_test, predictions)
plt.title("Flame-emission classification")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
plot_tree(model, feature_names=features.columns, class_names=model.classes_, filled=True)
plt.tight_layout()
plt.show()

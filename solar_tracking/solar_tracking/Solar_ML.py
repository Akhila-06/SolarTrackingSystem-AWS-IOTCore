import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

print("Please select your arduino_data.csv file...")
csv_file = askopenfilename(title="Choose CSV", filetypes=[("CSV files", "*.csv")])
df = pd.read_csv(csv_file)

features = ["LDR1", "LDR2", "Temp", "Humid"]
targets = ["LDR1", "LDR2", "Temp", "Humid", "Voltage"]
predictions = {}

for target in targets:
    feature_set = [f for f in features if f != target]
    y = df[target].values
    X = df[feature_set].values
    X = np.hstack((np.ones((X.shape[0], 1)), X))
    theta = np.linalg.inv(X.T @ X) @ X.T @ y
    y_pred = X @ theta
    predictions[f"Predicted {target}"] = y_pred
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    print(f"{target} model → RMSE: {rmse:.4f}")

df_output = df.copy()
for col, pred in predictions.items():
    df_output[col] = pred

output_path = csv_file.replace(".csv", "_predictions.csv")
df_output.to_csv(output_path, index=False)
print("\n Predictions saved to:", output_path)

# ==== Visualization ====
plt.figure(figsize=(16, 12))
for i, target in enumerate(targets):
    plt.subplot(3, 2, i + 1)
    plt.plot(df[target], label=f"Actual {target}", linewidth=2)
    plt.plot(df_output[f"Predicted {target}"], label=f"Predicted {target}", linestyle='--')
    plt.title(f"{target} - Actual vs Predicted")
    plt.xlabel("Sample Index")
    plt.ylabel(target)
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()

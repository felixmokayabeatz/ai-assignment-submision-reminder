# import os
# import numpy as np
# import pickle
# from sklearn.ensemble import RandomForestClassifier

# # Get the directory of THIS script
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(SCRIPT_DIR, "reminder_model.pkl")

# # Simulated Training Data
# X_train = np.array([
#     [-10], [-7], [-5], [-3], [-2], [0], [1], [3], [5], [7], [9], [10]
# ])  # Days before deadline

# y_train = np.array([
#     "P", "P", "P", "O", "O", "O", "O", "O", "E", "E", "E", "E"
# ])  # Labels (P=Procrastinator, O=On-time, E=Early)

# # Train Model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Save Model in the SAME DIRECTORY as this script
# with open(MODEL_PATH, "wb") as file:
#     pickle.dump(model, file)

# print(f"✅ Model training complete! Model saved at: {MODEL_PATH}")

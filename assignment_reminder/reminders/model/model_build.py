import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Step 1: Generate Synthetic Data
data = {
    'student_id': [1, 2, 1, 3, 2, 3, 1, 2, 3, 1],
    'assignment_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'days_before_due': [5, 3, 0, 1, -1, 2, 4, -2, 0, 3],
    'reminders_sent': [1, 2, 3, 1, 2, 2, 0, 3, 1, 0],
    'submitted_on_time': [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
}

# Step 2: Load Data into a DataFrame
df = pd.DataFrame(data)

# Step 3: Feature Selection and Preprocessing
X = df[['days_before_due', 'reminders_sent']]
y = df['submitted_on_time']

# Step 4: Split the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Make Predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate the Model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

# Step 8: Save the Trained Model
# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
model_filename = os.path.join(script_dir, 'reminder_model.pkl')

# Save the model using joblib
joblib.dump(model, model_filename)
print(f"Model saved successfully in the script's directory as {model_filename}")

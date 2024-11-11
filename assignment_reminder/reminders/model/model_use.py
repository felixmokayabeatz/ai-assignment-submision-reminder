import joblib

# Step 1: Load the Saved Model
model_filename = 'reminder_model.pkl'
model = joblib.load(model_filename)
print(f"Model loaded successfully from {model_filename}")

# Step 2: Prepare New Data for Prediction
# Example: Predict if a student will submit on time based on `days_before_due` and `reminders_sent`
new_data = [[3, 2], [0, 1], [-1, 3], [5, 0]]  # [days_before_due, reminders_sent]

# Step 3: Make Predictions
predictions = model.predict(new_data)

# Step 4: Display Results
for i, prediction in enumerate(predictions):
    status = "On Time" if prediction == 1 else "Late"
    print(f"Student {i+1}: {status}")

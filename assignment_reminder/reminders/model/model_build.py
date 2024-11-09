from sklearn.linear_model import LinearRegression
import numpy as np

# Example data
submission_times = np.array([7, 10, 12, 5, 3])  # days before due date
reminder_responses = np.array([1, 0, 1, 1, 0])  # 1 = on-time, 0 = late

model = LinearRegression()
model.fit(submission_times.reshape(-1, 1), reminder_responses)

# Predict best reminder time for a student
best_reminder_time = model.predict([[6]])  # Predict for 6 days before due date
print(f"Optimal Reminder Time: {best_reminder_time}")

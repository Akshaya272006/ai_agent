from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_month_sales(df):

    x = np.arange(len(df)).reshape(-1, 1)

    y = df["Sales (INR)"]

    model = LinearRegression()

    model.fit(x, y)

    next_month = np.array([[len(df)]])

    prediction = model.predict(next_month)

    return int(prediction[0])
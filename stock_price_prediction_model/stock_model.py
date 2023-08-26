import os

import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

DATA_PATH = "msft_data.json"

if os.path.exists(DATA_PATH):
    with open(DATA_PATH) as f:
        msft_hist = pd.read_json(DATA_PATH)
else:
    msft = yf.Ticker("MSFT")
    msft_hist = msft.history(period="max")
    msft_hist.to_json(DATA_PATH)

print("\n----------Data---------------")
print(msft_hist.head(5))

# msft_hist.plot.line(y="Close", use_index=True)

predictors = ["Close", "Volume", "Open", "High", "Low"]


def prepare_data(msft_hist, predictors):
    data = msft_hist[["Close"]]
    data = data.rename(columns={"Close": "Actual_Close"})

    data["Target"] = msft_hist.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])[
        "Close"
    ]

    # print("----------Target---------------")
    # print(data.head())

    msft_prev = msft_hist.copy()
    msft_prev = msft_prev.shift(1)
    # print("\n----------Shifted data---------------")
    # print(msft_prev.head())

    # Create the training data
    data = data.join(msft_prev[predictors]).iloc[1:]
    print("\n----------Training data---------------")
    print(data.head())

    return data


data = prepare_data(msft_hist, predictors)

# creat the model
model = RandomForestClassifier(n_estimators=100, min_samples_split=200, random_state=1)

# train the model
train = data.iloc[:-100]
test = data.iloc[-100:]  # last 100 rows for testing

model.fit(train[predictors], train["Target"])

# calculate precision
preds = model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
# print("\n----------Predictions for test data---------------")
# print(preds)
print(f"\nPrecision: {precision_score(test['Target'], preds)}")

# combined = pd.concat({"Target": test["Target"], "Predictions": preds}, axis=1)
# combined.plot()


# Backtesting
def backtest(data, model, predictors, start=1000, step=750):
    predictions = []

    for i in range(start, data.shape[0], step):
        # split training and test datasets
        train = data.iloc[0:i].copy()
        test = data.iloc[i : (i + step)].copy()

        # fit the model
        model.fit(train[predictors], train["Target"])

        # make predictions
        preds = model.predict_proba(test[predictors])[:, 1]
        preds = pd.Series(preds, index=test.index)
        preds[preds > 0.6] = 1
        preds[preds <= 0.6] = 0

        # combine predictions and test values
        combined = pd.concat({"Target": test["Target"], "Predictions": preds}, axis=1)

        predictions.append(combined)
    return pd.concat(predictions)


# add more predictors to improve accuracy
weekly_mean = data.rolling(7).mean()["Close"]
quarterly_mean = data.rolling(90).mean()["Close"]
annual_mean = data.rolling(365).mean()["Close"]
weekly_trend = data.shift(1).rolling(7).sum()["Target"]

data["weekly_mean"] = weekly_mean / data["Close"]
data["quarterly_mean"] = quarterly_mean / data["Close"]
data["annual_mean"] = annual_mean / data["Close"]
data["annual_weekly_mean"] = data["annual_mean"] / data["weekly_mean"]
data["annual_quarterly_mean"] = data["annual_mean"] / data["quarterly_mean"]
data["weekly_trend"] = weekly_trend
data["open_close_ratio"] = data["Open"] / data["Close"]
data["high_close_ratio"] = data["High"] / data["Close"]
data["low_close_ratio"] = data["Low"] / data["Close"]

full_predictors = predictors + [
    "weekly_mean",
    "quarterly_mean",
    "annual_mean",
    "annual_weekly_mean",
    "annual_quarterly_mean",
    "open_close_ratio",
    "high_close_ratio",
    "low_close_ratio",
]

predictions = backtest(data.iloc[365:], model, full_predictors)

print(
    f"\nPrecision with more predictors: {precision_score(predictions['Target'], predictions['Predictions'])}"
)

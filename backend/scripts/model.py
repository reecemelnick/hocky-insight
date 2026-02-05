from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, root_mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
from player_data import process_data


df = pd.read_csv('oilers_final.csv')

# X is all columns no ppg_3
X = df.drop(['ppg_3'], axis=1)
Y = df['ppg_3']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15)

print('Number of training data:', len(x_train))
print('Number of testing data:', len(x_test))

standardization = {}
for col in ["height", "plus_minus_1", "plus_minus_2", "avg_toi_1", "avg_toi_2", "weight", "age"]:
    mu = x_train[col].mean()
    sig = x_train[col].std()
    standardization[col] = {"mu": mu, "sig": sig}

def normalize_data(data):
    for col in ["height", "plus_minus_1", "plus_minus_2", "avg_toi_1", "avg_toi_2", "weight", "age"]:
        data[col] = (data[col] - standardization[col]["mu"]) / standardization[col]["sig"]
    return data 

x_train = normalize_data(x_train)
x_test = normalize_data(x_test)

# last season points as benchmark
print("Mean Squared Error:", mean_squared_error(x_test["points_2"], y_test))
print("Root Mean Squared Error:", root_mean_squared_error(x_test["points_2"], y_test))

# train a linear regression model and evaluate on test data
model = LinearRegression().fit(x_train, y_train)

print('MSE:', mean_squared_error(model.predict(x_test), y_test))
print('RMSE:', root_mean_squared_error(model.predict(x_test), y_test))

fig, ax = plt.subplots()
ax.scatter(y_test, model.predict(x_test), edgecolors=(0, 0, 0))
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k-', lw=2)
ax.set_xlabel('Target Pts/gm', size='x-large')
ax.set_ylabel('Predicted Pts/gm', size='x-large')
plt.savefig('plot.png')

df_pred = process_data()
df_pred_final = df_pred[["name","games_played_1", "games_played_2", "goals_1", "goals_2",
            "height", "plus_minus_1", "plus_minus_2", "ppg_3",
            "shots_1", "shots_2", "avg_toi_1", "avg_toi_2",
            "weight", "points_1", "points_2", "age"]]
# df_pred_final = pd.get_dummies(df_pred_final)

df_pred_final = normalize_data(df_pred_final)

predictions = df_pred_final[["name"]]
predictions["first name"] = predictions["name"].apply(lambda s: s.split(' ')[0])
predictions["name"] = predictions["name"].apply(lambda s: s.split(' ')[1])
# predictions["ppg"] = model.predict(df_pred_final.drop('name', axis=1))

print(predictions)
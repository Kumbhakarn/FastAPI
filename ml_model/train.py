import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

file_path = r"D:\16_FastAPI\housing.csv"

# Import the dataset and drop null values
df = pd.read_csv(file_path).iloc[:,:-1].dropna()
print('Read the data set: ')
# df.head()

# Split the dataset 
X = df.drop(columns='median_house_value')
y = df.median_house_value.copy()
print('split the dataset')

model = LinearRegression().fit(X,y)
print('Trained the model')

# Seralize the ml mode
joblib.dump(model, 'model.joblib')
print('Saved the Model')


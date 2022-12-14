# -*- coding: utf-8 -*-
"""Medical_Cost.ipynb adlı not defterinin kopyası

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17RDduYkb9LKwu-yeuY9UY88VJg-6hrsg
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
# %matplotlib inline

import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("insurance.csv")

df.head()

df.info()

df.describe().T

#normal bir dağılım gösteriyor
plt.figure(figsize=(9,6))
sns.distplot(df.bmi,color='orange')
plt.title('bmi dağılım')
plt.show()

plt.figure(figsize=(12,6))
sns.boxplot(df['bmi'])
plt.title('data with outliers')
plt.show()

def out_bound(df, col):
    Q1=df[col].quantile(0.25)
    Q3=df[col].quantile(0.75)
    IQR=Q3-Q1
    lower_bound=Q1-1.5*IQR
    upper_bound=Q3+1.5*IQR
    
    return lower_bound, upper_bound

out_bound(df, 'bmi')

def remove_outliers(data, col):
    l_b, u_b=out_bound(data, col)
    
    return data[ (data[col]>l_b) & (data[col]<u_b) ]

data1=remove_outliers(df, 'bmi')

plt.figure(figsize=(12,9))
sns.boxplot(data1['bmi'])
plt.title('data with removed outliers')
plt.show()

fig, ax1 = plt.subplots(figsize=(16, 9))
sns.set_palette('dark')
sns.histplot(data = df, x='charges', ax=ax1, bins=25, hue='smoker', kde=True)
plt.title('charges by smoker')
plt.show()

sns.set_palette('pastel')
plt.figure(figsize=(12,9))
plt.title('smokers by region')
sns.countplot(x='smoker', hue='region', data=df)
plt.show()

plt.figure(figsize=(12,7))
sns.set_palette('bright')
sns.violinplot(x=df['sex'],y=df['bmi'])
plt.title('bmi by gender')
plt.show()

region_children=df.groupby("region")["children"].sum()

#aralarında çok fark olmamakla birlikte southest de çocuk sayısı en fazladır
labels=region_children.index
sizes=region_children.values
plt.figure(figsize=(12,9))
colors=sns.color_palette('pastel')
plt.pie(sizes,labels=labels,autopct='%1.1f%%',
        shadow=True,colors=colors,startangle=90)
plt.show()

import plotly.express as px
px.scatter(y = df['age'], x = df['bmi'], color = df['sex'])

sns.set_palette('dark')
plt.figure(figsize=(12,9))
sns.scatterplot(x='children',y='bmi',data=df)
plt.title('charges by children')
plt.show()

plt.figure(figsize=(12,9))
sns.scatterplot(x='bmi',y='charges',data=df,color='#8A388A')
plt.show()

plt.figure(figsize=(10,6))
sns.barplot(x='region',y='bmi',data=df,hue='smoker')
plt.title('bmi across ages')
plt.show()





"""# Veri ön işleme"""

df.smoker=df.smoker.map({'yes':1,'no':0})

df.region=df.region.map({'southwest':0,'southeast':1,'northwest':2,'northeast':3})

df.sex=pd.get_dummies(df.sex,drop_first=True)

#train test split
X = df.drop('charges', axis = 1)
y = df['charges']
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.3, random_state=101)

#scalling data
scaler= StandardScaler()
scaler.fit(X_train)
X_train_scaled= scaler.transform(X_train)
X_test_scaled= scaler.transform(X_test)



"""# Model Seçme

### Linear regression
"""

linear_reg_model= LinearRegression()
linear_reg_model.fit(X_train_scaled, y_train)

y_pred = linear_reg_model.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_li_reg= metrics.mean_absolute_error(y_test, y_pred)
MSE_li_reg = metrics.mean_squared_error(y_test, y_pred)
RMSE_li_reg =np.sqrt(MSE_li_reg)
pd.DataFrame([MAE_li_reg, MSE_li_reg, RMSE_li_reg], index=['MAE_li_reg', 'MSE_li_reg', 'RMSE_li_reg'], columns=['Metrics'])

scores = cross_val_score(linear_reg_model, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

r2_score(y_test, linear_reg_model.predict(X_test_scaled))



"""### gradient boosting regressor"""

Gradient_model = GradientBoostingRegressor()
Gradient_model.fit(X_train_scaled, y_train)

y_pred = Gradient_model.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_gradient= metrics.mean_absolute_error(y_test, y_pred)
MSE_gradient = metrics.mean_squared_error(y_test, y_pred)
RMSE_gradient =np.sqrt(MSE_gradient)
pd.DataFrame([MAE_gradient, MSE_gradient, RMSE_gradient], index=['MAE_gradient', 'MSE_gradient', 'RMSE_gradient'], columns=['Metrics'])

scores = cross_val_score(Gradient_model, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

r2_score(y_test, Gradient_model.predict(X_test_scaled))



"""### XGB regressor"""

XGB_model =XGBRegressor()
XGB_model.fit(X_train_scaled, y_train);

y_pred = XGB_model.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_XGB= metrics.mean_absolute_error(y_test, y_pred)
MSE_XGB = metrics.mean_squared_error(y_test, y_pred)
RMSE_XGB =np.sqrt(MSE_XGB)
pd.DataFrame([MAE_XGB, MSE_XGB, RMSE_XGB], index=['MAE_XGB', 'MSE_XGB', 'RMSE_XGB'], columns=['Metrics'])

scores = cross_val_score(XGB_model, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

r2_score(y_test, XGB_model.predict(X_test_scaled))



"""### decision tree """

tree_reg_model =DecisionTreeRegressor()
tree_reg_model.fit(X_train_scaled, y_train);

y_pred = tree_reg_model.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_tree_reg= metrics.mean_absolute_error(y_test, y_pred)
MSE_tree_reg = metrics.mean_squared_error(y_test, y_pred)
RMSE_tree_reg =np.sqrt(MSE_tree_reg)
pd.DataFrame([MAE_tree_reg, MSE_tree_reg, RMSE_tree_reg], index=['MAE_tree_reg', 'MSE_tree_reg', 'RMSE_tree_reg'], columns=['Metrics'])

scores = cross_val_score(tree_reg_model, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

r2_score(y_test, tree_reg_model.predict(X_test_scaled))



"""### random forest regressor"""

forest_reg_model =RandomForestRegressor()
forest_reg_model.fit(X_train_scaled, y_train);

y_pred = forest_reg_model.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_forest_reg= metrics.mean_absolute_error(y_test, y_pred)
MSE_forest_reg = metrics.mean_squared_error(y_test, y_pred)
RMSE_forest_reg =np.sqrt(MSE_forest_reg)
pd.DataFrame([MAE_forest_reg, MSE_forest_reg, RMSE_forest_reg], index=['MAE_forest_reg', 'MSE_forest_reg', 'RMSE_forest_reg'], columns=['Metrics'])

scores = cross_val_score(forest_reg_model, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

r2_score(y_test, forest_reg_model.predict(X_test_scaled))



"""# Hyperparameters"""

from sklearn.model_selection import GridSearchCV

parameters = {'learning_rate': [0.005,0.01,0.02,0.03,0.04],
                  'subsample'    : [0.9, 0.5, 0.2, 0.1],
                  'n_estimators' : [50,100,500,1000,1500],
                  'max_depth'    : [1,2,4,6,8,10]
                 }

Gradient_model = GradientBoostingRegressor()

grid_GBR = GridSearchCV(estimator=Gradient_model, param_grid = parameters, cv = 2, n_jobs=-1)

grid_GBR.fit(X_train_scaled, y_train)

grid_GBR.best_estimator_

grid_GBR.best_score_

grid_GBR.best_params_

random_grid={'bootstrap': [True, False],
 'max_depth': [1,2,5,10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000,2500]}

rf = RandomForestRegressor(random_state = 42)

from sklearn.model_selection import RandomizedSearchCV
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)

rf_random.fit(X_train_scaled, y_train)

rf_random.best_params_

rf_random.best_score_

param_grid = {
    'bootstrap': [True],
    'max_depth': [80, 90, 100, 110],
    'max_features': [2, 3],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [100, 200, 300, 1000]
}

grid_GBR=GridSearchCV(estimator=rf, param_grid = param_grid, cv = 2, n_jobs=-1)

grid_GBR.fit(X_train_scaled,y_train)

grid_GBR.best_score_

grid_GBR.best_params_



random_forest= RandomForestRegressor(random_state = 42,n_estimators= 800,min_samples_split= 2, min_samples_leaf= 4,max_features= 'auto',max_depth= 5,bootstrap= True)

random_forest.fit(X_train_scaled,y_train)

y_pred = random_forest.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_gradient= metrics.mean_absolute_error(y_test, y_pred)
MSE_gradient = metrics.mean_squared_error(y_test, y_pred)
RMSE_gradient =np.sqrt(MSE_gradient)
pd.DataFrame([MAE_gradient, MSE_gradient, RMSE_gradient], index=['MAE_rf', 'MSE_rf', 'RMSE_rf'], columns=['Metrics'])

scores = cross_val_score(random_forest, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

rf_r2_score=r2_score(y_test, random_forest.predict(X_test_scaled))

r2_score(y_train, random_forest.predict(X_train_scaled))



gb=GradientBoostingRegressor(learning_rate=0.005, max_depth=2, n_estimators=1500,
                          subsample=0.9)

gb.fit(X_train_scaled,y_train)

y_pred = gb.predict(X_test_scaled)
y_pred = pd.DataFrame(y_pred)
MAE_gradient= metrics.mean_absolute_error(y_test, y_pred)
MSE_gradient = metrics.mean_squared_error(y_test, y_pred)
RMSE_gradient =np.sqrt(MSE_gradient)
pd.DataFrame([MAE_gradient, MSE_gradient, RMSE_gradient], index=['MAE_gb', 'MSE_gb', 'RMSE_gb'], columns=['Metrics'])

scores = cross_val_score(gb, X_train_scaled, y_train, cv=5)
print(np.sqrt(scores))

gb_r2_score=r2_score(y_test, gb.predict(X_test_scaled))

r2_score(y_train, gb.predict(X_train_scaled))



import numpy as np
import matplotlib.pyplot as plt


r2_scores = [rf_r2_score*100, gb_r2_score*100]
model_names = ['RF', 'GBM']

total_bar = np.arange(len(model_names))
color = ['#9edd1d', '#3edd1d', '#f7c851']

fig, ax = plt.subplots(figsize=(10, 3))
bar = plt.bar(model_names, r2_scores, align='center', alpha=.75, color=color)
plt.xticks(total_bar, model_names)
plt.ylabel('Accuracy',fontsize=14, color='black')
plt.xlabel('Model Name',fontsize=14, color='black')
plt.title('Model (LR, RF, GB) Performance Comparison', fontsize=16, color='black', fontweight='bold')

# # this functions will set data lebel 
def autolabel(bar):
    for bar in bar:
        height = int(bar.get_height())
        ax.text(bar.get_x() + .4, .5*height,
                height, va='bottom',
                fontsize=14, color='black')
        
autolabel(bar)

plt.show()


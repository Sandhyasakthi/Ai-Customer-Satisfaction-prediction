from catboost import CatBoostClassifier
import numpy as np

X = np.array([
    [5,5,5],
    [4,4,4],
    [3,3,3],
    [2,2,2],
    [1,1,1]
])

y = ["Happy","Happy","Neutral","Sad","Sad"]

model = CatBoostClassifier(verbose=0)
model.fit(X,y)

model.save_model("catboost_model.cbm")
print("Model saved")

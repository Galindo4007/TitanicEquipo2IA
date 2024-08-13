import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

df_gender = pd.read_csv('gender_submission.csv')
df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')

print(df_gender.head())

import numpy as np
import pandas as pd
import sys
# creates a random assignemnt of peg positions where the first is a movement to
# the initial position
fname = sys.argv[1]

# Hardcoding the extent of movement (in steps) that we want
neg_extent_x = -6
neg_extent_y = 0
pos_extent_x = 10
pos_extent_y = 10
spacing = 2 # must be an int
mode = 'D'
delay = 2

x = np.arange(neg_extent_x,pos_extent_x,spacing)
y = np.arange(neg_extent_y,pos_extent_y,spacing)
X,Y = np.meshgrid(x,y)
mask = X**2>Y
X = X[mask]
Y = Y[mask]

df = pd.DataFrame()
df['X'] = X.ravel()
df['Y'] = Y.ravel()
df['mode'] = mode
df['delay'] = delay
df = df.loc[1:]

df = df.sample(frac=1)

temp = pd.DataFrame([{'X':0,'Y':0,'mode':'D','delay':0}])
df = pd.concat([temp, df])
df = df.reset_index(drop=True)


df.to_csv(fname)






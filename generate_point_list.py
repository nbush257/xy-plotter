import numpy as np
import pandas as pd
import sys
# creates a random assignemnt of peg positions where the first is a movement to
# the initial position

# Hardcoding the extent of movement (in steps) that we want
extent_x = 50
extent_y = 50
spacing = 10 # must be an int

delay = 5

# Position furthest from the nose:
start_x = int(sys.argv[1])
# Position most medial
start_y = int(sys.argv[2])
fname = sys.argv[3]


x = np.arange(start_x, start_x + extent_x,spacing)
y = np.arange(start_y, start_y + extent_y,spacing)
X,Y = np.meshgrid(x,y)


df = pd.DataFrame()
df['X'] = X.ravel()
df['Y'] = Y.ravel()
df['mode'] = 'M'
df['delay'] = delay
df = df.loc[1:]

df = df.sample(frac=1)

temp = pd.DataFrame([{'X':start_x,'Y':start_y,'mode':'D','delay':0}])
df = pd.concat([temp, df])
df = df.reset_index(drop=True)


df.to_csv(fname)






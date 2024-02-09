import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(-122,-120, 5)
y = np.linspace(34, 36, 5)
x_1, y_1 = np.meshgrid(x, y)
 

random_data = np.random.random((5, 5))

plt.contourf(x_1, y_1, random_data, cmap = 'jet') 
 
 
plt.colorbar()
plt.show()  

#at each point in the matrix take a weighted average of 3 or 4 (maybe all) of the swell height 

''' 
 Quiver plot 
https://www.geeksforgeeks.org/quiver-plot-in-matplotlib/
https://www.geeksforgeeks.org/numpy-meshgrid-function/
https://stackoverflow.com/questions/56046811/how-make-a-correct-gradient-map-using-numpy-gradient
'''
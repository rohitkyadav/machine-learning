from math import sqrt

plot1 = [1, 3]
plot2 = [2, 5]

euclidean_distance = sqrt( (plot1[0]-plot2[0])**2 + (plot1[1]-plot2[1])**2 )
print(euclidean_distance)

# alternate way
# x = [ 1,3 ]
# y = [ 2,5 ]
# euclidean_distance = sqrt( sum(  [(x-y)**2 for x, y in zip(x,y) ] ) )
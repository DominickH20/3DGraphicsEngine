from ThreeSpace import *

a = vector(1,0,0)
b = vector(0,1,0)
print("a = " + a)
print("b = " + b)

mag = a.mag()
print("mag = " + mag)

dot = dot(a,b)
print("dot = " + dot)

c = cross(a,b)
d = cross(b,a)

print(c)
print(d)

print(add(a,b))
print(subtract(a,b))

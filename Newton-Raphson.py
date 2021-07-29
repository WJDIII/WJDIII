def newraph(fn, x, tolerance=.0001, max_iteration=1000):
    for i in range(max_iteration):
        xnew = x - fn[0](x)/fn[1](x)
        if abs(xnew-x) < tolerance: break
        x = xnew
    return xnew, i

y = [lambda x: 2*x**3 - 9.5*x + 7.5, lambda x: 6*x**2 - 9.5]

x, n = newraph(y, 5)
print(x)
print(n)
print("the root is %f at %d interations." % (x, n))
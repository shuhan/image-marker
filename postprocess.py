from DroneData import Loader

loader = Loader('static/marked/')

(x, y), (a, b) = loader.load_data()

print(x.shape)
print(y.shape)
print(a.shape)
print(b.shape)
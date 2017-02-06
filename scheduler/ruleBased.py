
class Pass():
	def __init__(self, start, end, duration):
		self.start = start
		self.end = end
		self.duration = duration

	
passes = [
	Pass(10, 12, 2), Pass(22, 24, 2), Pass(34, 36, 2), 
	Pass(0, 1, 1), Pass(4, 1, 1), Pass(7, 1, 1), 
	Pass(4, 6, 2), Pass(16, 18, 2), Pass(28, 30, 2), 
	Pass(2, 5, 3), Pass(14, 17, 3), Pass(26, 29, 3), 
]

print("Initial list")
for aPass in passes: 
	print(str(aPass.start) + ",")

passes.sort(key=lambda x: x.start, reverse=False)

print("Sorted list")
for aPass in passes: 
	print(str(aPass.start) + ",")

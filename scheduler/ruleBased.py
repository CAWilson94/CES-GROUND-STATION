
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

i = 0
print("passes: " + str(len(passes)))
for i in range(len(passes)):
	j = i + 1
	print("i: " + str(i) + ", j: " + str(j))
	conflicting = []
	while(conflicts(passes[i], passes[j])):
		print("i: " + str(i) + ", j: " + str(j))
		conflicting.append(passes[j])
		if(j < i - 2):
			j += 1
		else:
			break
	if(conflicting):
		conflicting.append(passes[i])

def conflicts(passA, passB):
	if(passB.start>passA.start and passB.start < passA.end):
		return False
	else:
		return True
	
def sortConflics(conflicting):
	print("There were : " + str(len(conflicting)) + " conflics found:")
	for aPass in conflicting: 
		print(str(aPass.start) + " - " + str(aPass.end))
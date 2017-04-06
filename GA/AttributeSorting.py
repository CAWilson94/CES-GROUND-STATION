import operator

class Score:
	 def __init__(self, score):
	 	self.score = score


scoreOne = Score(30)
scoreTwo = Score(20)
scoreThree = Score(10)

listScore = [scoreOne,scoreTwo,scoreThree]

cmpfun= operator.attrgetter("score")

listScore.sort(key=cmpfun, reverse=True)

newScore = sorted(listScore, key=cmpfun)

for item in newScore:
	print(item.score)

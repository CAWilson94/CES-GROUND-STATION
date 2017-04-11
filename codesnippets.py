Simple

currentSolution = startingSolution
oldScore = -INF
loop do 
	neighbours = getNeighbours(currentSoution)
	for n in neighbours
		newScore = getFitness(n)
		if(newScore > oldScore)
			nextSolution = n
			oldScore = newScore
			exit for loop
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


Steepest

currentSolution = startingSolution
oldScore = -INF
loop do 
	neighbours = getNeighbours(currentSoution)
	for n in neighbours
		newScore = getFitness(n)
		if(newScore > oldScore)
			nextSolution = n
			oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


stochastic

currentSolution = startingSolution
oldScore = -INF
loop do 
		j = getRandomInt()
		k = getRandomInt()

		swap1=currentSolution[k]
		swap2=currentSolution[j]

		currentSolution[j]=swap1
		currentSolution[k]=swap2

		newScore = getFitness(currentSolution)

		if(newScore > oldScore)
			bestSolution = currentSolution
			oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution


RR

currentSoution = startingSolution
oldScore = - INF
loop do 
	shuffle(currentSolution)
	newSolution = simpleHC(currentSolution)
	newScore = getFitness(bestSolution)
	if(newScore > oldScore)
		bestSolution =  newSolution
		oldScore = newScore
	if newScore <= getFitness(currentSolution)
		return currentSolution
	currentSolution =  nextSolution




class PriceStrategy():
	def cost(baseCost):
		pass

class NormalPrice(PriceStrategy):
	def cost(baseCost):
		return baseCost

class SalePrice(PriceStrategy):
	def cost(baseCost):
		return baseCost*.8

priceStrategy = NormalPrice()

price = priceStrategy.cost(10)
price = 10

priceStrategy = SalePrice()

price = priceStrategy.cost(10)
price = 8


class MissionView(APIView):

	def get(self, request):
			...
		serializer = MissionSerializer(missionList, many=True)         
		return Response(serializer.data)

	def post(self, request):
			...
		return Response({'Creation Successful': request.data.get("name")} ,status=status.HTTP_201_CREATED)

	def delete(self, request):
			...
		return Response({'Deleted Successful':deleted},status=status.HTTP_200_OK)


scheduler = MOTSimpleHC()
scheduler = MOTSteepestHC()
scheduler = MOTStochasticHC()
scheduler = MOTRandomRestartHC()
scheduler = MOTRuleBased()
scheduler = MOTGA()
 #Tour Object
class Tour:
   
   def __init__(self, attributes, price):
      self.attributes = attributes
      self.price = price
   
   def getPrice(self):
      return self.price
   
   def getAttributes(self):
      return self.attributes
      
#Tour Combinations and Prices
tours = [] 
tours.append(Tour(["Van", "Corp", "Gold"], 800))
tours.append(Tour(["Van", "Corp", "Silver"], 720))
tours.append(Tour(["Van", "Corp", "Bronze"], 680))

tours.append(Tour(["Van", "Edu", "Gold"], 640))
tours.append(Tour(["Van", "Edu", "Silver"], 608))
tours.append(Tour(["Van", "Edu", "Bronze"], 576))

tours.append(Tour(["Van", "Comm", "Gold"], 360))
tours.append(Tour(["Van", "Comm", "Silver"], 400))
tours.append(Tour(["Van", "Comm", "Bronze"], 380))

tours.append(Tour(["Walk", "Corp", "Gold"], 800))
tours.append(Tour(["Walk", "Corp", "Silver"], 720))
tours.append(Tour(["Walk", "Corp", "Bronze"], 680))

tours.append(Tour(["Walk", "Edu", "Gold"], 600))
tours.append(Tour(["Walk", "Edu", "Silver"], 540))
tours.append(Tour(["Walk", "Edu", "Bronze"], 510))

tours.append(Tour(["Walk", "Comm", "Gold"], 360))
tours.append(Tour(["Walk", "Comm", "Silver"], 400))
tours.append(Tour(["Walk", "Comm", "Bronze"], 380))

tours.append(Tour(["Talk", "Corp", "Gold"], 960))
tours.append(Tour(["Talk", "Corp", "Silver"], 720))
tours.append(Tour(["Talk", "Corp", "Bronze"], 1040))

tours.append(Tour(["Talk", "Edu", "Gold"], 585))
tours.append(Tour(["Talk", "Edu", "Silver"], 450))
tours.append(Tour(["Talk", "Edu", "Bronze"], 450))

tours.append(Tour(["Talk", "Comm", "Gold"], 400))
tours.append(Tour(["Talk", "Comm", "Silver"], 400))
tours.append(Tour(["Talk", "Comm", "Bronze"], 480))

#Randomly Generated Example !(Can delete when implemented)!
import random
tourTypes = ["Van", "Walk", "Talk"]
orgTypes = ["Corp", "Edu", "Comm"]
tierTypes = ["Gold", "Silver", "Bronze"]

exTour = random.choice(tourTypes)
exOrg = random.choice(orgTypes)
exTier = random.choice(tierTypes)

clientTour = [exTour, exOrg, exTier]

#Algorithm
for item in tours:
   if(clientTour == item.getAttributes()):
      print(item.getPrice())
      break

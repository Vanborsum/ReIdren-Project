# Create Tour class
class Tour:   
   def __init__(self, attributes, price):
      self.attributes = attributes
      self.price = price
   
   def getPrice(self):
      return self.price
   
   def getAttributes(self):
      return self.attributes

# Import values from form
orgType = input_data.get('orgType')
tierType = input_data.get('tierType')
tourDescription = input_data.get('tourDescription')
firstRequestedDate = input_data.get('firstRequestedDate')
secondRequestedDate = input_data.get('secondRequestedDate')
fullName = input_data.get('fullName')
price = 0

# Determine Tour Description
tourDescription = tourDescription[3:]   

#Tour Combinations and Prices
tours = [] 
tours.append(Tour(["Corporate Group", "4 to 8 passengers (Min. 4)"], 800))
tours.append(Tour(["Corporate Group", "9 to 11 passengers"], 720))
tours.append(Tour(["Corporate Group", "12 to 14 passengers (Max. 14)"], 680))

tours.append(Tour(["Educational/Non-Profit Group", "4 to 8 passengers (Min. 4)"], 640))
tours.append(Tour(["Educational/Non-Profit Group", "9 to 11 passengers"], 608))
tours.append(Tour(["Educational/Non-Profit Group", "12 to 14 passengers (Max. 14)"], 576))

tours.append(Tour(["Local Community Group", "4 to 8 passengers (Min. 4)"], 360))
tours.append(Tour(["Local Community Group", "9 to 11 passengers"], 400))
tours.append(Tour(["Local Community Group", "12 to 14 passengers (Max. 14)"], 380))

# Create Requested Tour
requestedTour = [orgType, tierType]

# Loop through tour combinations looking for correct tour
for item in tours:
   if(requestedTour == item.getAttributes()):
      price = item.getPrice()
      break

# Add Wave fee to price
feePrice = price + (price * (0.029) + 0.60)
feePrice = round(feePrice, 2)

# Get today's date and due date for invoice
from datetime import date, timedelta
today = str(date.today())
dueDate = str(date.today() + timedelta(days=10))

# Change format of requested dates to fit Zapier format requirements
from datetime import datetime
parsed_date = datetime.strptime(firstRequestedDate, '%m/%d/%Y')
parsed_date2 = datetime.strptime(secondRequestedDate, '%m/%d/%Y')

# Convert to desired format yyyy-mm-dd
firstRequestedDate = parsed_date.strftime('%Y-%m-%d')
new_date = parsed_date + timedelta(days=1)
firstRequestedDatePlusOne = new_date.strftime('%Y-%m-%d')

secondRequestedDate = parsed_date2.strftime('%Y-%m-%d')
new_date2 = parsed_date2 + timedelta(days=1)
secondRequestedDatePlusOne = new_date2.strftime('%Y-%m-%d')

# Parse firstName out of fullName
firstName = fullName.split()[0] 

# Return Outputs
output = {'tourType': 'Van', 'tierType': tierType, 'orgType': orgType, 'price': price, 'feePrice': feePrice, 'today': today, 'dueDate': dueDate, 'tourDescription': tourDescription, 'firstRequestedDate': firstRequestedDate, 'firstRequestedDatePlusOne': firstRequestedDatePlusOne, 'secondRequestedDate': secondRequestedDate, 'secondRequestedDatePlusOne': secondRequestedDatePlusOne, 'firstName': firstName}
ver. 2024-11-05T16:42-9b38ba24
Van Tour | Zapier
y': today, 'dueDate': dueDate, 'tourDescription': tourDescription}

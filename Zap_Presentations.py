# Create Presentation class
class Presentation:   
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
presentationDescription = input_data.get('presentationDescription')
firstRequestedDate = input_data.get('firstRequestedDate')
secondRequestedDate = input_data.get('secondRequestedDate')
fullName = input_data.get('fullName')
price = 0

# Determine Tour Description
presentationDescription = presentationDescription[3:]

#Tour Combinations and Prices
presentations = [] 
presentations.append(Presentation(["Local Community Group/Libraries/Edus/Non-profits", "8 to 25 people"], 450))
presentations.append(Presentation(["Local Community Group/Libraries/Edus/Non-profits", "26 to 45 people"], 675))

presentations.append(Presentation(["Corporate Group", "8 to 25 people"], 600))
presentations .append(Presentation(["Corporate Group", "26 to 45 people"], 900))

# Create Requested Tour
requestedPresentation = [orgType, tierType]

# Loop through tour combinations looking for correct tour
for item in presentations:
   if(requestedPresentation == item.getAttributes()):
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

output = {'bookingType': 'Presentation', 'tierType': tierType, 'orgType': orgType, 'price': price, 'feePrice': feePrice, 'today': today, 'dueDate': dueDate, 'presentationDescription': presentationDescription, 'firstRequestedDate': firstRequestedDate, 'firstRequestedDatePlusOne': firstRequestedDatePlusOne, 'secondRequestedDate': secondRequestedDate, 'secondRequestedDatePlusOne': secondRequestedDatePlusOne, 'firstName': firstName} 'today': today, 'dueDate': dueDate, 'presentationDescription': presentationDescription}

import sensortag
import time

# Global constants for menu choices
TEMP = 1
ADD = 2
CHANGE = 3
DELETE = 4
NOTHING = 5
YET = 6
QUIT = 7

def main():
 
	# Initialize a variable for the user's choice.
	choice = 0
	
	# Process menu selections until the user
	# wants to quit the program.
	while choice != QUIT:
		# Get the user's menu choice.
		choice = get_menu_choice()
		
		# Process the choice.
		if choice == TEMP:
			temp()
		elif choice == ADD:
			add()
		elif choice == CHANGE:
			change()
		elif choice == DELETE:
			delete()
		elif choice == NOTHING:
			nothing()
		elif choice == YET:
			yet()
		
def get_menu_choice():
	print()
	print('Menu')
	print('---------------------------')
	print('1. Test Temperature Reader')
	print('2. Test NO Reader')
	print('3. Test NO Reader')
	print('4. Test NO Reader')
	print('5. Test NO Reader')
	print('6. Test NO Reader')
	print('7. Quit the program')
	print()
	# Get the user's choice.
	choice = int(input('Enter your choice: '))
	
	# Validate the choice.
	while choice < TEMP or choice > QUIT:
		choice = int(input('Enter a valid choice: '))
	
	# return the user's choice.
	return choice

def temp():
	print('CTRL+C to return to Menu')
	try:
		ST = sensortag.Sensortag()
		
		while True:
			print(ST.getTemp())
			time.sleep(5)
	except(KeyboardInterrupt):
		pass

def add():
	pass
def change():
	pass
def delete():
	pass
def nothing():
	pass
def yet():
	pass

main()

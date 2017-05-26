def user_input():
    """"Ask for and create variables to store user input."""
    print("This script will help you to create personalized email notifications for homes for sale." + "\n")
    area = input("What area are you interested in? E.g. enter 'Falun', 'Uppsala', 'Nacka': ")
    type_of_object = input("What type of object? E.g. enter 'villa', 'lägenhet', 'gård', 'tomt-mark', 'fritidshus', 'parhus','radhus','kedjehus': ")
    MinRooms = input("Minimum number of rooms? ")
    MaxPrice = input("Maximum starting price? ")


    print("\n" + "Your preferences are: ")
    print("Area of interest = " + str(area))
    print("Type of object = " + str(type_of_object))
    print("Minimum number of rooms = " + str(MinRooms))
    print("Maximum price = " + str(MaxPrice) + "\n")

    correct_inputs = input("Is this correct? y/n")

    if correct_inputs == "n":
        print("\n")
        user_input()
    else:
        print("\n" + "Great! Let's setup the email notifications.")

user_input()
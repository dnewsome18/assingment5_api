import data
from sandwich_maker import SandwichMaker
from cashier import Cashier


# Make an instance of other classes here
resources = data.resources
recipes = data.recipes
sandwich_maker_instance = SandwichMaker(resources)
cashier_instance = Cashier()

def main():
    is_on = True
    while is_on:
        choice = input("What size sandwich would you like? (small/medium/large or 'exit' to quit): ").lower()

        if choice == "exit":
            print("Exiting the program. Goodbye!")
            is_on = False  # Exit the loop

        elif choice in recipes:
            sandwich = recipes[choice]
            cost = sandwich["cost"]

            print(f"That will be ${cost}.")
            payment = cashier_instance.process_coins()

            if cashier_instance.transaction_result(payment, cost):
                sandwich_maker_instance.make_sandwich(choice, sandwich["ingredients"])

        else:
            print("Sorry, that's not a valid size.")

if __name__ == "__main__":
    main()
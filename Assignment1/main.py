recipes = {
    "small": {
        "ingredients": {
            "bread": 2,  ## slice
            "ham": 4,  ## slice
            "cheese": 4,  ## ounces
        },
        "cost": 1.75,
    },
    "medium": {
        "ingredients": {
            "bread": 4,  ## slice
            "ham": 6,  ## slice
            "cheese": 8,  ## ounces
        },
        "cost": 3.25,
    },
    "large": {
        "ingredients": {
            "bread": 6,  ## slice
            "ham": 8,  ## slice
            "cheese": 12,  ## ounces
        },
        "cost": 5.5,
    }
}

resources = {
    "bread": 12,  ## slice
    "ham": 18,  ## slice
    "cheese": 24,  ## ounces
}

def run_sandwich_machine():
    """Main function to run the sandwich machine."""
    machine = SandwichMachine(resources)

    is_running = True
    while is_running:
        choice = input("What would you like? (small/medium/large/off/report): ").lower()

        if choice == "off":
            is_running = False
        elif choice == "report":
            machine.show_report()
        elif choice in recipes:
            sandwich = recipes[choice]
            if machine.check_resources(sandwich['ingredients']):
                payment = machine.process_coins()
                if machine.transaction_result(payment, sandwich['cost']):
                    machine.make_sandwich(choice, sandwich['ingredients'])
        else:
            print("Invalid selection. Please choose small, medium, large, off, or report.")


class SandwichMachine:

    def __init__(self, machine_resources):
        """Receives resources as input"""
        self.machine_resources = machine_resources

    def check_resources(self, ingredients):
        """Returns True when order can be made, False if ingredients are insufficient."""
        for item, amount in ingredients.items():
            if self.machine_resources[item] < amount:
                print(f"Sorry, there is not enough {item}.")
                return False
        return True

    def process_coins(self):
        """Returns the total calculated from coins inserted."""
        print("Please insert coins.")
        large_dollars = int(input("How many large dollars?: "))
        half_dollars = int(input("How many half dollars?: "))
        quarters = int(input("How many quarters?: "))
        nickels = int(input("How many nickels?: "))

        total = (large_dollars * 1) + (half_dollars * 0.5) + (quarters * 0.25) + (nickels * 0.05)
        return total

    def transaction_result(self, coins, cost):
        """Return True when the payment is accepted, or False if money is insufficient."""
        if coins < cost:
            print("Sorry, that's not enough money. Money refunded.")
            return False
        elif coins > cost:
            change = round(coins - cost, 2)
            print(f"Here is ${change} in change.")
        return True

    def make_sandwich(self, sandwich_size, order_ingredients):
        """Deduct the required ingredients from the resources."""
        for item, amount in order_ingredients.items():
            self.machine_resources[item] -= amount
        print(f"{sandwich_size.capitalize()} sandwich is ready. Bon appetit!")

    def show_report(self):
        """Display current resource levels."""
        print("Current resources:")
        for item, amount in self.machine_resources.items():
            if item == "cheese":
                print(f"{item.capitalize()}: {amount} ounce(s)")
            else:
                print(f"{item.capitalize()}: {amount} slice(s)")

if __name__ == "__main__":
    run_sandwich_machine()
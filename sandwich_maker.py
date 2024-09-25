
class SandwichMaker:
    def __init__(self, resources):
        self.machine_resources = resources

    def check_resources(self, ingredients):
        """Returns True when order can be made, False if ingredients are insufficient."""
        for item in ingredients:
            if ingredients[item] > self.machine_resources.get(item, 0):
                print(f"Sorry, there is not enough {item}.")
                return False
        return True

    def make_sandwich(self, sandwich_size, order_ingredients):
        if self.check_resources(order_ingredients):
            for item in order_ingredients:
                self.machine_resources[item] -= order_ingredients[item]
            print(f"Here is your {sandwich_size} sandwich!")
        else:
            print("Cannot make the sandwich due to insufficient resources.")
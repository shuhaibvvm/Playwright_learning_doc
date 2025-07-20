# Demonstrating Instance Method, Class Method, and Static Method

# -------------------------------------------------------------------
# 🧠 Concept Summary:
# - Instance Method (`self`): Used by one specific object; can access instance variables.
#   👉 Why? Because every cake (object) has a different flavor or size, so we use `self` to access its unique data.
#
# - Class Method (`cls`): Used by the class itself; can access or modify class-level data.
#   👉 Why? Sometimes we want to work with shared factory rules or change something for all cakes, not just one.
#
# - Static Method: A helper method; does not access instance or class data.
#   👉 Why? It's just a utility — like a tip or formula — that doesn’t depend on any object or class data.
# -------------------------------------------------------------------

class CakeFactory:
    factory_name = "Yummy Cakes"  # Class variable shared by all

    def __init__(self, flavor):
        self.flavor = flavor  # Instance variable

    # Instance Method
    def describe(self):
        print(f"This cake is {self.flavor}")

    # Class Method
    @classmethod
    def describe_factory(cls):
        print(f"This is the {cls.factory_name} factory")

    # Static Method
    @staticmethod
    def baking_tip():
        print("Always preheat the oven to 180°C")


# Using the methods
cake1 = CakeFactory("Chocolate")
cake2 = CakeFactory("Vanilla")

# Instance Method
cake1.describe()          # Output: This cake is Chocolate
cake2.describe()          # Output: This cake is Vanilla

# Class Method
CakeFactory.describe_factory()  # Output: This is the Yummy Cakes factory

# Static Method
CakeFactory.baking_tip()        # Output: Always preheat the oven to 180°C

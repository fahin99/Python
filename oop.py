class Car:
    def __init__(self, model, year, for_sale):
        self.model = model
        self.year = year
        self.for_sale = for_sale

    def display_info(self):
        return f"{self.year} {self.model} - {'For Sale' if self.for_sale else 'Not For Sale'}"
    
car1 = Car("Toyota Camry", 2020, True)
print(car1)
print(car1.model)
print(car1.display_info())
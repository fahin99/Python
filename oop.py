from abc import ABC, abstractmethod
        
# Demonstrating class and instance attributes
class Car:
    color = "Red"  # Class attribute
    price = 25000  # Class attribute
    def __init__(self, model, year, for_sale):
        self.model = model
        self.year = year
        self.for_sale = for_sale
        self.price+=500  # Instance attribute modification

    def display_info(self):
        return f"{self.year} {self.model} - {'For Sale' if self.for_sale else 'Not For Sale'}"
    def speak(self):
        print(f"{self.model} says Vroom Vroom!")
print("-----Demonstrating class and instance attributes-----\n")
car1 = Car("Toyota Camry", 2020, True)
car2 = Car("Honda Accord", 2019, False)
print(car1)
print(car1.model)
print(car1.display_info())
print(f"{Car.color} and {car1.color}")  # Accessing class attribute
print(f"Price: {car1.price}")  # Accessing modified instance attribute

# Demonstrating multiple inheritance
print("\n-----Demonstrating multiple inheritance-----\n")
class animal:
    def __init__(self, name):
        self.name = name

class prey(animal):
    def flee(self):
        print(f"{self.name} is fleeing!")
        
class predator(animal):
    def hunt(self):
        print(f"{self.name} is hunting!")
class dog(animal):
    def speak(self):
        print(f"{self.name} says Woof!")
        
class fish(prey, predator):
    def swim(self):
        print(f"{self.name} is swimming!")
    def speak(self):
        print(f"{self.name} says Blub!")
        
class rabbit(prey):
    def hide(self):
        print(f"{self.name} is hiding!")
dog1 = dog("Scooby")
dog1.speak()

fish1 = fish("Nemo")
fish1.flee()
fish1.hunt()
fish1.swim()

rabbit1 = rabbit("Raboot")
rabbit1.flee()
rabbit1.hide()

# Demonstrating inheritance and method overriding, using super()
print("\n-----Demonstrating inheritance and method overriding, using super()-----\n")
class shape:
    def __init__(self, color, is_filled):
        self.color = color
        self.is_filled = is_filled
    def identity(self):
        return f"Shape: {self.color}, Filled: {self.is_filled}"

class circle(shape):
    def __init__(self, radius, color, is_filled):
        super().__init__(color, is_filled)
        self.radius = radius
        
class square(shape):
    def __init__(self, side_length, color, is_filled):
        super().__init__(color, is_filled)
        self.side_length = side_length
        
class triangle(shape):
    def __init__(self, base, height, color, is_filled):
        super().__init__(color, is_filled)
        self.base = base
        self.height = height
shape1 = shape("Blue", True)
print(shape1.identity())
circle1 = circle(5, "Red", False)
print(circle1.identity())
print(f"Circle Radius: {circle1.radius}")

# Demonstrating polymorphism
print("\n-----Demonstrating polymorphism-----\n")
class shape_area:
    @abstractmethod
    def area(self):
        pass
class circle(shape_area):
    name="Circle"
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius * self.radius
    
class square(shape_area):
    name="Square"
    def __init__(self, side_length):
        self.side_length = side_length
    def area(self):
        return self.side_length * self.side_length
    
class triangle(shape_area):
    name="Triangle"
    def __init__(self, base, height):
        self.base = base
        self.height = height
    def area(self):
        return 0.5 * self.base * self.height

shapes=[circle(3), square(4), triangle(3, 4)]
for shape in shapes:
    print(f"Area of {shape.name}: {shape.area():.2f}")

# Demonstrating duck typing
print("\n-----Demonstrating duck typing-----\n")
sounders=[dog("Buddy"), fish("Dory"), Car("Ford Mustang", 2021, True)]
for sounder in sounders:
    sounder.speak()
    
# Demonstrating Static and Class methods
print("\n-----Demonstrating Static and Class methods-----\n")
class employee:
    count = 0  # Class attribute to count employees
    total_salary = 0  # Class attribute to track total salary

    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary
        employee.count += 1
        employee.total_salary += salary
    #instance method
    def get_info(self):
        return f"Employee: {self.name}, Position: {self.position}"
    
    #static method
    @staticmethod
    def is_valid_position(position):
        valid_positions = ["Manager", "CEO", "Cook"]
        return position in valid_positions
    
    #class method
    @classmethod
    def get_employee_count(cls):
        return f"Total # employees: {cls.count}"

    @classmethod
    def get_avg_salary(cls):
        if cls.count == 0:
            return "No employees to calculate average salary."
        else:
            return f"Average salary: {cls.total_salary / cls.count :.2f}"
        
emp1 = employee("Alice", "Manager", 80000)
emp2 = employee("Bob", "Cook", 40000)
print(f"Instance method: {emp1.get_info()}")
print(f"Static method: Is valid position (CEO): {employee.is_valid_position("CEO")}")
print("Class method outputs:")
print(employee.get_employee_count())
print(employee.get_avg_salary())

# Demonstrating Magic Methods
print("\n-----Demonstrating Magic Methods-----\n")
class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
print(f"Before __str__: {book('1984', 'George Orwell', 328)}")

class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    def __str__(self):
        return f"'{self.title}' by {self.author}, {self.pages} pages"
    
print(f"After __str__: {book('1984', 'George Orwell', 328)}")
    
class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    def __len__(self):
        return self.pages

print(f"\nNumber of pages in book, using len(book('1984', 'George Orwell', 328)): {len(book('1984', 'George Orwell', 328))}")

print(f"\nComparing two books using == operator, before __eq__: {book('1984', 'George Orwell', 328) == book('1984', 'George Orwell', 328)}")
class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    def __eq__(self, other):
        return self.title == other.title and self.author == other.author and self.pages == other.pages
    
print(f"Comparing two books using == operator, after __eq__: {book('1984', 'George Orwell', 328) == book('1984', 'George Orwell', 328)}")

class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    def __lt__(self, other):
        return self.pages < other.pages
    def __gt__(self, other):
        return self.pages > other.pages
print(f"\nComparing two books using < operator: {book('Animal Farm', 'George Orwell', 112) < book('1984', 'George Orwell', 328)}")
print(f"Comparing two books using > operator: {book('Animal Farm', 'George Orwell', 112) > book('1984', 'George Orwell', 328)}")

class book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    def __contains__(self, item):
        return item in self.title or item in self.author
    
print(f"\nChecking if '1984' is in book title using 'in' operator: {'1984' in book('1984', 'George Orwell', 328)}")
print(f"Checking if 'Orwell' is in book author using 'in' operator: {'Orwell' in book('1984', 'George Orwell', 328)}")
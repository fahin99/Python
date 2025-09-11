def add_wrapper(func):
    def wrapper(*args, **kwargs):
        print("**You added a wrapper 🍨**")
        func(*args, **kwargs)
    return wrapper

def add_sprinkles(func):
    def sprinkles(*args, **kwargs):
        print("**You added some sprinkles 🎊**")
        func(*args, **kwargs)
    return sprinkles

@add_wrapper
@add_sprinkles
def ice_cream(flavor):
    print(f"You ordered a {flavor} ice cream! 🍦")

ice_cream("chocolate")
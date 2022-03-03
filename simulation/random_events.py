from random import randint, choice, sample


def rainy_day(model):
    print("Rainy day, we will be closing earlier today.")
    model.time -= (model.time//3)

def broken_cashier(model):
    print("Broken Cashier")
    if len(model.cashiers)>1:
        model.remove_cashier()

def angry_customers(model):
    print("Some customers are angry and less tolerant.")
    ac = sample(model.customers, randint(1, len(model.customers) - 1))
    for c in ac:
        c.tolerance = c.tolerance//2

def black_friday(model):
    print("Today is Black Friday, double amount of customers and time.")
    model.time *= 2
    for i in range(model.no_customers) :
        model.add_customer(model.behavior[randint(0,2)])

def cyber_monday(model):
    print("Today is Cyber Monday, customers will yield more profits.")
    model.customer_value *= 2


def event_selector(model, proc_chance = 10):
    events = [rainy_day, broken_cashier, angry_customers, cyber_monday, black_friday]
    if randint(0, 99) < proc_chance:
        choice(events)(model)
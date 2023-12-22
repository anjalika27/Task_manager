# create fake dataset to learn about queries in django

# django admin credentials
# Username = Anjalika
# password = 123

from faker import Faker 
fake=Faker()

def seed_db(n=10)->None:
    for i in range(0,n):
        name=fake.name()
        description=fake.text()
        
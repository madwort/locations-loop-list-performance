import datetime
from faker import Faker
from faker.providers import address
from tqdm import tqdm

fake = Faker()

print(datetime.datetime.now())

fake.add_provider(address)

trial_list = []

for n in range(20000):
    mylocations = []
    for n in range(5):
        mylocations.append({"address":fake.street_address()})
    trial_list.append(
        {
            "name": fake.name(),
            "protocolSection": {
                "contactsLocationsModule": {"locations": mylocations},
                "identificationModule": {"nctId": "1234abc"}
            },
        }
    )

before_time = datetime.datetime.now()
print(before_time)


locations_list = []
for x in trial_list:
    try:
        locations = x['protocolSection']['contactsLocationsModule']['locations']
        for l in locations:
            l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
        locations_list = locations_list + locations
    except KeyError:
        pass

locations_list_1 = locations_list

after_time = datetime.datetime.now()
print(after_time)

time_difference = after_time - before_time
print(time_difference)

print("-------")

before_time = datetime.datetime.now()
print(before_time)


locations_list = [
    {**data_item, 'nctid': item['protocolSection']['identificationModule']['nctId']}
    for item in trial_list
    if 'contactsLocationsModule' in item['protocolSection'] and 'locations' in item['protocolSection']['contactsLocationsModule']
    for data_item in item['protocolSection']['contactsLocationsModule']['locations']
]

locations_list_2 = locations_list

after_time = datetime.datetime.now()
print(after_time)

time_difference = after_time - before_time
print(time_difference)

assert(locations_list_1 == locations_list_2)
print(locations_list_1[0])
print(locations_list_1[0])

print("-------")

before_time = datetime.datetime.now()
print(before_time)


locations_list = []
for x in trial_list:
    try:
        locations = x['protocolSection']['contactsLocationsModule']['locations']
        for l in locations:
            l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
            locations_list.append(l)
    except KeyError:
        pass

locations_list_3 = locations_list

after_time = datetime.datetime.now()
print(after_time)

time_difference = after_time - before_time
print(time_difference)

assert(locations_list_1 == locations_list_3)

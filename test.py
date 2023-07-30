import datetime
from faker import Faker
from faker.providers import address
import random
import timeit
from tqdm import tqdm

fake = Faker()
fake.add_provider(address)

trial_list = []
for n in range(40000):
    mylocations = []
    for n in range(5):
        mylocations.append({"address":fake.street_address()})
    if (random.random() > 0.5):
        trial_list.append(
            {
                "name": fake.name(),
                "protocolSection": {
                    "contactsLocationsModule": {"locations": mylocations},
                    "identificationModule": {"nctId": "1234abc"}
                },
            }
        )
    else:
        trial_list.append(
            {
                "name": fake.name(),
                "protocolSection": {},
            }
        )
        
def original_version(trial_list):
    locations_list = []
    for x in trial_list:
        try:
            locations = x['protocolSection']['contactsLocationsModule']['locations']
            for l in locations:
                l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
            locations_list = locations_list + locations
        except KeyError:
            pass
    return locations_list

def original_version_if(trial_list):
    locations_list = []
    for x in trial_list:
        if 'contactsLocationsModule' in x['protocolSection'] and 'locations' in x['protocolSection']['contactsLocationsModule']:
            locations = x['protocolSection']['contactsLocationsModule']['locations']
            for l in locations:
                l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
            locations_list = locations_list + locations
    return locations_list

def chatgpt_version(trial_list):
    locations_list = [
        {**data_item, 'nctid': item['protocolSection']['identificationModule']['nctId']}
        for item in trial_list
        if 'contactsLocationsModule' in item['protocolSection'] and 'locations' in item['protocolSection']['contactsLocationsModule']
        for data_item in item['protocolSection']['contactsLocationsModule']['locations']
    ]
    return locations_list

def tom_version(trial_list):
    locations_list = []
    for x in trial_list:
        try:
            locations = x['protocolSection']['contactsLocationsModule']['locations']
            for l in locations:
                l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
                locations_list.append(l)
        except KeyError:
            pass
    return locations_list

def tom_version2(trial_list):
    locations_list = []
    for x in trial_list:
        if 'contactsLocationsModule' in x['protocolSection'] and 'locations' in x['protocolSection']['contactsLocationsModule']:
            locations = x['protocolSection']['contactsLocationsModule']['locations']
            for l in locations:
                l.update({'nctid':x['protocolSection']['identificationModule']['nctId']})
                locations_list.append(l)
    return locations_list

setup = "from __main__ import original_version, trial_list"
print(f"Original: {timeit.timeit('original_version(trial_list)', setup=setup, number=1)}")

setup = "from __main__ import original_version_if, trial_list"
print(f"Original (if): {timeit.timeit('original_version_if(trial_list)', setup=setup, number=1)}")

setup = "from __main__ import chatgpt_version, trial_list"
print(f"ChatGPT: {timeit.timeit('chatgpt_version(trial_list)', setup=setup, number=1)}")

setup = "from __main__ import tom_version, trial_list"
print(f"TomW (try/except): {timeit.timeit('tom_version(trial_list)', setup=setup, number=1)}")

setup = "from __main__ import tom_version2, trial_list"
print(f"TomW (if): {timeit.timeit('tom_version2(trial_list)', setup=setup, number=1)}")

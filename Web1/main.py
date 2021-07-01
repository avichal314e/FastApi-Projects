# Part 1 - Create a Python Rest API endpoint
# Create a CRUD Rest API endpoint for Healthcare Provider directory. Use Python - FastAPI for building the Rest APIs.
# Store the data as an in-memory Dictionary.

# Invokation: hypercorn main:app --reload


from enum import Enum
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import pickle


app = FastAPI()
db = {}


class status(int, Enum):
    active = 1
    inactive = 0


class Provider(BaseModel):
    active: Optional[status] = 1
    name: str
    qualification: str
    speciality: str
    phone: str
    department: Optional[str] = None
    organization: str
    location: Optional[str] = None
    address: str


@app.get('/')
def index():
    return 'HEALTH PROVIDER API ACTIVE!!'


def get_uuid(param: str, value: str):
    if(param == 'active'):
        try:
            value = int(value)
        except:
            return []
    results = []
    for uuid in db:
        try:
            if(db[uuid][param] == value):
                results.append(uuid)
        except:
            return []
    return results


@app.get('/providers')
def get_providers():
    return [db[uuid] for uuid in db.keys()]


@app.get('/get_provider/{field}={value}')
def get_provider(field: str, value: str):
    entries = get_uuid(field, value)
    results = [db[entry] for entry in entries]
    return (results if results else "No Data Found")


@app.put('/create_provider')
def create_provider(provider: Provider):
    pro_uuid = str(uuid.uuid4())
    db[pro_uuid] = provider.dict()
    db[pro_uuid]['providerID'] = pro_uuid
    return db[pro_uuid]


@app.delete('/delete_provider/{field}={value}')
def delete_provider(field: str, value: str):
    entries = get_uuid(field, value)
    results = []
    for entry in entries:
        results.append(db[entry])
        del db[entry]
    return (results if results else "No Data Found")


@app.post('/update_provider/{id}')
def update_provider(id: str, active=None, name=None, qualification=None, speciality=None, phone=None, department=None, organization=None, location=None, address=None):
    if(id in db.keys()):
        try:
            if(active and int(active) not in [0, 1]):
                return "Invalid Active Status!"
            db[id]['active'] = (
                int(active) if active is not None else db[id]['active'])
        except:
            return "Invalid Active Status!"

        db[id]['name'] = (
            name if name is not None else db[id]['name'])

        db[id]['qualification'] = (
            qualification if qualification is not None else db[id]['qualification'])

        db[id]['speciality'] = (
            speciality if speciality is not None else db[id]['speciality'])

        db[id]['phone'] = (
            phone if phone is not None else db[id]['phone'])

        db[id]['department'] = (
            department if department is not None else db[id]['department'])

        db[id]['organization'] = (
            organization if organization is not None else db[id]['organization'])

        db[id]['location'] = (
            location if location is not None else db[id]['location'])

        db[id]['address'] = (
            address if address is not None else db[id]['address'])
        return "SUCCESS!! Provider Details Updated."
    else:
        return "Provider not found!!"

# Invokation: hypercorn main:app --reload


from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uuid


app = FastAPI()

db = {}


class Provider(BaseModel):
    active: Optional[bool] = True
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
        if(value == "false"):
            value = False
        elif(value == 'true'):
            value = True
        else:
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
    if(field == "providerID"):
        try:
            return db[uuid.UUID(value)]
        except:
            return "No Data Found"
    else:
        entries = get_uuid(field, value)
        results = [db[entry] for entry in entries]
        return (results if results else "No Data Found")


@app.put('/provider')
def create_provider(provider: Provider):
    pro_uuid = uuid.uuid4()
    db[pro_uuid] = provider.dict()
    db[pro_uuid]['providerID'] = pro_uuid
    return db[pro_uuid]


@app.delete('/delete_provider/{field}={value}')
def delete_provider(field: str, value: str):
    if(field == "providerID"):
        try:
            val = db[uuid.UUID(value)]
            del db[uuid.UUID(value)]
            return [val]
        except:
            return "No Data Found"
    else:
        entries = get_uuid(field, value)
        results = []
        for entry in entries:
            results.append(db[entry])
            del db[entry]
        return (results if results else "No Data Found")


@app.post('/update_provider/{id}')
def update_provider(id: str, active=None, name=None, qualification=None, speciality=None, phone=None, department=None, organization=None, location=None, address=None):
    try:
        pro_uuid = uuid.UUID(id)
    except:
        return "Invalid UUID!"
    if(pro_uuid in db.keys()):
        if(active):
            if(active == 'false'):
                db[pro_uuid]['active'] = False
            else:
                db[pro_uuid]['active'] = True

        db[pro_uuid]['name'] = (
            name if name is not None else db[pro_uuid]['name'])

        db[pro_uuid]['qualification'] = (
            qualification if qualification is not None else db[pro_uuid]['qualification'])

        db[pro_uuid]['speciality'] = (
            speciality if speciality is not None else db[pro_uuid]['speciality'])

        db[pro_uuid]['phone'] = (
            phone if phone is not None else db[pro_uuid]['phone'])

        db[pro_uuid]['department'] = (
            department if department is not None else db[pro_uuid]['department'])

        db[pro_uuid]['organization'] = (
            organization if organization is not None else db[pro_uuid]['organization'])

        db[pro_uuid]['location'] = (
            location if location is not None else db[pro_uuid]['location'])

        db[pro_uuid]['address'] = (
            address if address is not None else db[pro_uuid]['address'])
        return "SUCCESS!! Provider Details Updated."
    else:
        return "Provider not found!!"

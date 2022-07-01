from models.raw import Raw
from models.organizations import Client
from db import Session

def etl_clients(domain, raw_type, updated_after):
    with Session().no_autoflush as session:
        raw_clients = Raw.find_all_distinct(
            domain=domain,
            raw_type='client',
            session=session
        )

        for raw_client in raw_clients:
            body = raw_client.body

            client = Client(
                id = raw_client.id,
                pbz_id = body.get('id'),
                name = body.get('name'),
                street = body.get('street'),
                city = body.get('city'),
                postal_code = body.get('postal_code'),
                phone = body.get('phone'),
                fax = body.get('fax'),
                email = body.get('email'),
                web = body.get('web'),
                person = body.get('person'),
                timezone = body.get('timezone'),
                country_code = body.get('country_code')
            )

            session.add(client)
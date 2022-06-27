from db import Session
from models.raw import Raw
from network import RequestMaker


def scrap_categories(domain, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_categories()


def scrap_clients(domain, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_clients()


def scrap_participant_detail(domain, client_id, participant_id, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_participant_detail(client_id, participant_id)


def scrap_participants_per_client(domain, client_id, updated_after, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_participants(client_id, updated_after)


def scrap_all_participants(domain, updated_after, use_proxy):
    with Session() as session:
        clients = Raw.find_all_distinct(domain, 'client', session)

    for client in clients:
        print('Scraping participants of client: {}'.format(client))
        client_id = client.raw_obj_id
        participants = scrap_participants_per_client(domain, client_id, updated_after, use_proxy)

        for p in participants:
            participant_id = p.get('id')
            p_detail = scrap_participant_detail(
                domain, client_id, participant_id, use_proxy)

            with Session() as ins_session:
                p_raw = Raw(
                    raw_type='participant',
                    raw_obj_id=participant_id,
                    domain=domain,
                    body=p_detail
                )

                ins_session.add(p_raw)
                ins_session.commit()


def scrap_auction_detail(domain, client_id, auction_id, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_auction_detail(client_id, auction_id)


def scrap_auctions_per_client(domain, client_id, updated_after, use_proxy):
    rm = RequestMaker(domain, use_proxy)
    return rm.get_auctions(client_id, updated_after)


def scrap_all_auctions(domain, updated_after, use_proxy):
    with Session() as session:
        clients = Raw.find_all_distinct(domain, 'client', session)

    for client in clients:
        print('Scraping auctions of client: {}'.format(client))
        client_id = client.raw_obj_id
        auctions = scrap_auctions_per_client(domain, client_id, updated_after, use_proxy)

        for a in auctions:
            auction_id = a.get('id')
            a_detail = scrap_auction_detail(domain, client_id, auction_id, use_proxy)

            with Session() as ins_session:
                a_raw = Raw(
                    raw_type='auction',
                    raw_obj_id=auction_id,
                    domain=domain,
                    body=a_detail
                )

                ins_session.add(a_raw)
                ins_session.commit()

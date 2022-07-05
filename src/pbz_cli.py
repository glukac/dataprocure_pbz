from datetime import datetime
from typing import List, Optional

import typer

from db import Session
from etl import etl_clients
from models.raw import Raw
from scraper import (scrap_all_auctions, scrap_all_participants,
                     scrap_categories, scrap_clients)

app = typer.Typer()


@app.command()
def scrap(domain: str, 
        use_proxy: bool = typer.Option(False), 
        raw_type: Optional[List[str]] = typer.Option(None), 
        updated_after: datetime = typer.Option(datetime(2000, 1, 1))):

    if 'category' in raw_type:
        categories = scrap_categories(domain, use_proxy)

        if categories:
            with Session() as session:
                for cat in categories:
                    cat_id = cat.get('id')

                    old_cat = Raw.find_one(
                        domain, 'category', cat_id, session)

                    new_cat = Raw(
                        raw_type='category',
                        pbz_id=cat_id,
                        domain=domain,
                        body=cat
                    )

                    if not old_cat or old_cat.body != cat:  # ; compare new and old JSON containing scrapped info
                        session.add(new_cat)

                    session.commit()

    if 'client' in raw_type:
        clients = scrap_clients(domain, use_proxy)

        if clients:
            with Session() as session:
                for cl in clients:
                    cl_id = cl.get('id')

                    old_cl = Raw.find_one(domain, 'client', cl_id, session)

                    new_cl = Raw(
                        raw_type='client',
                        pbz_id=cl_id,
                        domain=domain,
                        body=cl
                    )

                    if not old_cl or old_cl.body != cl:  # compare new and old JSON containing scrapped info
                        session.add(new_cl)

                    session.commit()

    if 'participant' in raw_type:
        scrap_all_participants(domain, updated_after, use_proxy)

    if 'auction' in raw_type:
        scrap_all_auctions(domain, updated_after, use_proxy)


@app.command()
def etl(domain: str,
        use_proxy: bool = typer.Option(False),
        raw_type: Optional[List[str]] = typer.Option(None),
        updated_after: datetime = typer.Option(datetime(2000, 1, 1))):
    etl_clients(domain, use_proxy, raw_type, updated_after)


if __name__ == "__main__":
    app()

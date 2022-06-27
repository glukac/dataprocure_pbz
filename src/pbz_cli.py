from datetime import datetime
from typing import List, Optional

import typer

from db import Session
from models.raw import Raw
from scraper import scrap_all_auctions, scrap_all_participants, scrap_categories, scrap_clients

app = typer.Typer()


@app.command()
def scrap(domain: str, use_proxy: bool = typer.Option(False), raw_type: Optional[List[str]] = typer.Option(None), updated_after: datetime = typer.Option(datetime(2000, 1, 1))):

    if 'category' in raw_type:
        categories = scrap_categories(domain, use_proxy)

        with Session() as session:
            for cat in categories:
                cat_id = cat.get('id')

                old_cat = Raw.find_one(
                    domain, 'category', cat_id, session)

                new_cat = Raw(
                    raw_type='category',
                    raw_obj_id=cat_id,
                    domain=domain,
                    body=cat
                )

                if not old_cat or old_cat.body != cat:  #; compare new and old JSON containing scrapped info
                    session.add(new_cat)

                session.commit()

    if 'client' in raw_type:
        clients = scrap_clients(domain, use_proxy)

        with Session() as session:
            for cl in clients:
                cl_id = cl.get('id')

                old_cl = Raw.find_one(domain, 'client', cl_id, session)

                new_cl = Raw(
                    raw_type='client',
                    raw_obj_id=cl_id,
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
def etl(sample: bool = False, form_type: Optional[List[str]] = typer.Option(None)):
    typer.echo(f"Hello from etl. Please be patient...")


if __name__ == "__main__":
    app()

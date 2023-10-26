from sqlalchemy.orm import sessionmaker
import functions_framework

from utils.connection import connect_with_connector
from utils.exceptions import StoreAlreadyExists, StoreNotFound
from utils.models import Local2


@functions_framework.http
def update_store(request) -> None:
    engine = connect_with_connector()
    session_marker = sessionmaker(bind=engine)
    session = session_marker()

    request_json = request.get_json(silent=True)
    holding = request_json.get('holding')
    store_code = request_json.get('store_code')
    store_b2b = request_json.get('store_b2b')
    new_store_code = request_json.get('new_store_code')
    new_store_b2b = request_json.get('new_store_b2b')

    try:
        store = session.query(Local2).filter(
            Local2.holding == holding,
            Local2.codigo_local == store_code,
            Local2.codigo_b2b == store_b2b,
        ).first()

        if not store:
            raise StoreNotFound

        exists_store = session.query(Local2).filter(
            Local2.holding == holding,
            Local2.codigo_local == new_store_code,
            Local2.codigo_b2b == new_store_b2b,
        ).exists()

        if exists_store:
            raise StoreAlreadyExists

        if new_store_code:
            store.codigo_local = new_store_code

        if new_store_b2b:
            store.codigo_b2b = new_store_b2b

        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

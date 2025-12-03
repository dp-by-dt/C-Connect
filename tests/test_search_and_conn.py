# tests/test_search_and_conn.py
import pytest
from app import create_app, db
from models import User, Profile, Connection

@pytest.fixture
def client():
    app = create_app('testing')  # ensure testing config
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            # create users
            u1 = User(full_name='Alice Tester', email='alice@test.com')
            p1 = Profile(user=u1, department='ECE', interests='ai,ml')
            db.session.add(u1); db.session.commit()
        yield c
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_api_search_empty(client):
    resp = client.get('/api/search?q=')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['total'] == 0

def test_connection_send(client):
    # create second user and login as first (requires test login helper)
    pass

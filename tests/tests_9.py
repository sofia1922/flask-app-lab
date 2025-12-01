import pytest
from app import create_app, db
from app.users.models import User

@pytest.fixture
def app():
    app = create_app("testing")
    app.config["WTF_CSRF_ENABLED"] = False  

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# завантаження сторінки
def test_register_page_loads(client):
    """Сторінка реєстрації доступна"""
    response = client.get("/users/register")
    assert response.status_code == 200
    assert "Реєстрація" in response.get_data(as_text=True)


def test_login_page_loads(client):
    """Сторінка входу доступна"""
    response = client.get("/users/login")
    assert response.status_code == 200
    assert "Вхід" in response.get_data(as_text=True)

def test_user_registration(client, app):
    """Користувач успішно реєструється та зберігається в БД"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "12345"
    }

    response = client.post("/users/register", data=data, follow_redirects=True)

    assert "Реєстрація успішна" in response.get_data(as_text=True)

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(email="test@example.com")
        ).scalar_one_or_none()

        assert user is not None
        assert user.username == "testuser"


def test_login_logout(client, app):
    """Перевірка логіну і логауту"""

    # cтворюємо користувача 
    with app.app_context():
        user = User(username="loginuser", email="login@test.com")
        user.set_password("mypassword")
        db.session.add(user)
        db.session.commit()

    # Вхід
    response = client.post(
        "/users/login",
        data={"username": "login@test.com", "password": "mypassword"},
        follow_redirects=True
    )

    assert "Вхід успішний" in response.get_data(as_text=True)

    # Вихід
    response = client.get("/users/logout", follow_redirects=True)

    assert "Ви вийшли із системи" in response.get_data(as_text=True)

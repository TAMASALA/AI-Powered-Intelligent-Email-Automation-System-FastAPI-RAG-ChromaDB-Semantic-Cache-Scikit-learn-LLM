from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["status"] == "Running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_process_ham():

    payload = {

        "email": """
        Hi HR,

        I am suffering from fever.

        Kindly approve one day sick leave.

        Regards,
        Vinay
        """

    }

    response = client.post(

        "/api/v1/process-email",

        json=payload

    )

    assert response.status_code == 200

    assert "classification" in response.json()

    assert "response" in response.json()


def test_process_spam():

    payload = {

        "email": """
        Congratulations!!

        You won ₹10,00,000.

        Click Here.

        """

    }

    response = client.post(

        "/api/v1/process-email",

        json=payload

    )

    assert response.status_code == 200

    assert "classification" in response.json()
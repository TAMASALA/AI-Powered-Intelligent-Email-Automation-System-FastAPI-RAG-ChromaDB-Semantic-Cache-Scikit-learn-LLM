from app.ml.predictor import (

    predict_email,

    predict_probability

)


def test_prediction():

    email = """

    Hi HR,

    I need sick leave tomorrow.

    """

    result = predict_email(

        email

    )

    assert result in [

        "HAM",

        "SPAM"

    ]


def test_probability():

    email = """

    Free Lottery Winner.

    Click Here.

    """

    result = predict_probability(

        email

    )

    assert "prediction" in result

    assert "confidence" in result
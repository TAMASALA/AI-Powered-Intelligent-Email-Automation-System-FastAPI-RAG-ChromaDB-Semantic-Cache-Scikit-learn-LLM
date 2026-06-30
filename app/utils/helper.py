import uuid

from datetime import datetime


# =============================================
# Generate UUID
# =============================================

def generate_uuid():

    return str(uuid.uuid4())


# =============================================
# Current Timestamp
# =============================================

def current_timestamp():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )


# =============================================
# Current File Name
# =============================================

def generate_filename():

    return (

        datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        + "_"

        + str(uuid.uuid4())[:8]

        + ".json"

    )


# =============================================
# Success Response
# =============================================

def success_response(

    message,

    data=None

):

    return {

        "status": "success",

        "message": message,

        "data": data

    }


# =============================================
# Error Response
# =============================================

def error_response(

    message

):

    return {

        "status": "error",

        "message": message

    }


# =============================================
# Separator
# =============================================

def line(length=60):

    print("=" * length)


# =============================================
# Print Heading
# =============================================

def heading(title):

    line()

    print(title)

    line()


if __name__ == "__main__":

    heading("Helper Test")

    print(generate_uuid())

    print(current_timestamp())

    print(generate_filename())
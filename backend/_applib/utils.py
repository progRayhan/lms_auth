import jwt

def get_token(payload:dict, secret:str, algorithm:str):
    generated_token = jwt.encode(
        payload=payload,
        key=secret,
        algorithm=algorithm
    )

    return generated_token

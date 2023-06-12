import os
import jwt
from datetime import datetime, timedelta

class JWT:

    def __init__(self):
        """Initialize jwt by os environments
        """

        self.secret = os.getenv("JWT_SECRET", "DEFAULT_SECRET_IS_32_BIT_LENGTH!")
        self.expire_time = int(os.getenv("JWT_EXPIRE_TIME", 10800))
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")

        # Check if using default secret
        if self.secret == "DEFAULT_SECRET_IS_32_BIT_LENGTH!":
            print("WARNING:\tDetected JWT is using default secret.")

        # Variable mappings
        self.INVALID = -1

    def generate(self, uid: int) -> str:
        """Generates jwt from uid

        Args:
            uid (int): the uid of the user

        Returns:
            str: the encoded jwt
        """

        print(datetime.utcnow())

        return jwt.encode({"uid": uid, "exp": int((datetime.utcnow() + timedelta(seconds=self.expire_time)).timestamp())}, self.secret, self.algorithm)
    
    def validate(self, jwt_token: str) -> int:
        """Validate the jwt token and returns the data

        Args:
            jwt_token (str): the jwt token

        Returns:
            int: the uid, or -1 if invalid
        """

        try:

            data = jwt.decode(jwt_token, self.secret, [self.algorithm])
            print(f"INFO:\tUser <{data.get('uid')}> authenticated")
            return data.get('uid')
        
        # The token expires
        except jwt.exceptions.ExpiredSignatureError:

            return -1

        
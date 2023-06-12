import os
 
basedir = os.path.abspath(os.path.dirname(__file__))
 
def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)
 
class BaseConfig:
    TITLE="Auth-System-API"
    SQLALCHEMY_DATABASE_URI = ""
    STAGE=""
 
class DevelopmentConfig(BaseConfig):
    STAGE="DEV"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:5432/auth-system'
 
class TestingConfig(BaseConfig):
    STAGE="TEST"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("test.db")
 
config: BaseConfig = {
    'DEV': DevelopmentConfig,
    'TEST': TestingConfig,
}
class Config:
    SECRET_KEY = "B!1w8NAt1T^%kvhUI*S^"

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = "sql3.freesqldatabase.com"
    MYSQL_USER = "sql3490743"
    MYSQL_PASSWORD = "8RytB29KfK"
    MYSQL_DB = "sql3490743"

config={
    'development':DevelopmentConfig
}
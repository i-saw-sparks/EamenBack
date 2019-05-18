import sqlalchemy

db = sqlalchemy.create_engine("postgresql+psycopg2://postgres:1234@192.168.84.147/aerolinea")

db.connect()
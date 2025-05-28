from sqlalchemy import create_engine
from backend_ticketing.models.meta import Base
from backend_ticketing.models.mymodel import Bus, Route, Schedule, Seat, Ticket

def init_database():
    # Ganti dengan URL database Anda
    engine = create_engine('sqlite:///ticketing.db')
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
    
    # Tambah data sample
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Tambah bus sample jika belum ada
    if session.query(Bus).count() == 0:
        sample_bus = Bus(name='Bus Jakarta', license_plate='B1234CD')
        session.add(sample_bus)
        session.commit()
        print("Sample bus added!")
    
    session.close()

if __name__ == '__main__':
    init_database()
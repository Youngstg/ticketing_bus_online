import argparse
import sys
import transaction
import datetime # Untuk data awal

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

# Sesuaikan path import ini dengan struktur proyek Anda
# Asumsi package utama Anda bernama 'backend'
from .. import models # Ini akan mengimpor dari backend/backend/models/__init__.py
from ..models.meta import Base # Untuk operasi create_all jika diperlukan, tapi Alembic lebih baik
from ..models.user import User, UserRole
from ..models.bus import Bus, BusClass
from ..models.schedule import Schedule
# from ..models.booking import Booking, BookingStatus # Uncomment jika ingin membuat contoh booking

def setup_models(dbsession):
    """
    Tambahkan atau perbarui model/fixtures di database.
    Fungsi ini akan menambahkan data contoh jika tabel kosong.
    """
    print("Setting up initial data...")

    # 1. Buat Pengguna Admin (jika belum ada)
    admin_email = 'admin@example.com'
    admin_user = dbsession.query(models.User).filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = models.User(email=admin_email, role=UserRole.ADMIN)
        admin_user.set_password('admin123') # Ganti dengan password yang lebih aman
        dbsession.add(admin_user)
        print(f"Admin user '{admin_email}' created.")
    else:
        print(f"Admin user '{admin_email}' already exists.")

    # 2. Tambah Contoh Data Bus (jika belum ada)
    if dbsession.query(models.Bus).count() == 0:
        bus1 = models.Bus(name='RouteMaster Express', capacity=40, bus_class=BusClass.ECONOMY)
        bus2 = models.Bus(name='TravelGo Luxury', capacity=30, bus_class=BusClass.BUSINESS)
        bus3 = models.Bus(name='CityHopper Mini', capacity=20, bus_class=BusClass.ECONOMY)
        
        dbsession.add_all([bus1, bus2, bus3])
        dbsession.flush() # Penting untuk mendapatkan ID bus sebelum membuat schedule
        print("Sample buses created.")

        # 3. Tambah Contoh Data Schedule (jika bus sudah ada)
        # Pastikan bus1, bus2, bus3 memiliki ID setelah flush
        if bus1.id and bus2.id and bus3.id and dbsession.query(models.Schedule).count() == 0 :
            schedule1 = models.Schedule(
                bus_id=bus1.id,
                origin_location='Jakarta',
                destination_location='Bandung',
                departure_time=datetime.datetime(2025, 7, 15, 8, 0, 0), # Tahun, Bulan, Hari, Jam, Menit, Detik
                arrival_time=datetime.datetime(2025, 7, 15, 11, 30, 0),
                price=150000.00
            )
            schedule2 = models.Schedule(
                bus_id=bus2.id,
                origin_location='Bandung',
                destination_location='Jakarta',
                departure_time=datetime.datetime(2025, 7, 15, 14, 0, 0),
                arrival_time=datetime.datetime(2025, 7, 15, 17, 30, 0),
                price=250000.00
            )
            schedule3 = models.Schedule(
                bus_id=bus1.id,
                origin_location='Jakarta',
                destination_location='Yogyakarta',
                departure_time=datetime.datetime(2025, 7, 16, 19, 0, 0),
                arrival_time=datetime.datetime(2025, 7, 17, 5, 0, 0),
                price=350000.00
            )
            schedule4 = models.Schedule(
                bus_id=bus3.id,
                origin_location='Solo',
                destination_location='Yogyakarta',
                departure_time=datetime.datetime(2025, 7, 16, 10, 0, 0),
                arrival_time=datetime.datetime(2025, 7, 16, 12, 0, 0),
                price=75000.00
            )
            dbsession.add_all([schedule1, schedule2, schedule3, schedule4])
            print("Sample schedules created.")
    else:
        print("Buses already exist or no new buses added, skipping schedule creation.")
    
    # Tambahkan contoh data lain jika perlu, misalnya Booking ( uncomment import di atas)
    # if admin_user and dbsession.query(models.Schedule).first() and dbsession.query(models.Booking).count() == 0:
    #     first_schedule = dbsession.query(models.Schedule).first()
    #     example_booking = models.Booking(
    #         user_id=admin_user.id,
    #         schedule_id=first_schedule.id,
    #         seat_number='A1',
    #         total_price=first_schedule.price,
    #         status=BookingStatus.PAID
    #     )
    #     dbsession.add(example_booking)
    #     print("Sample booking created.")

    print("Initial data setup finished.")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        # Jika Anda menggunakan Alembic untuk membuat tabel, baris Base.metadata.create_all(engine)
        # biasanya tidak diperlukan di sini, atau bisa dijadikan opsional.
        # Namun, cookiecutter scaffold mungkin menyertakannya.
        # Jika tabel sudah dibuat Alembic, ini tidak akan melakukan apa-apa.
        engine = env['request'].dbsession.bind 
        # Base.metadata.create_all(engine) # Opsional jika Alembic sudah menangani pembuatan tabel

        with env['request'].tm: # Menggunakan transaction manager dari request
            dbsession = env['request'].dbsession
            setup_models(dbsession)
        print("Database initialization script completed successfully.")
    except OperationalError as e:
        print(f'''
Pyramid is having a problem using your SQL database.
Error: {e}
The problem might be caused by one of the following things:

1.  You may need to create your database and tables with `alembic upgrade head`.
    Check your README.txt (atau README.md) for description and try to run it.

2.  Your database server may not be running. Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "{args.config_uri}" file is running.
        ''')
        sys.exit(1) # Keluar dengan error code jika ada masalah DB
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
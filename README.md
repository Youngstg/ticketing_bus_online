Whiish - Sistem Pemesanan Tiket Bus Daring
Whiish adalah aplikasi web yang dikembangkan menggunakan React dan Pyramid, dirancang untuk memfasilitasi pengguna dalam melakukan pencarian perjalanan bus, pemilihan kursi, dan pemesanan tiket secara daring melalui antarmuka yang modern dan interaktif.

Deskripsi Aplikasi Web
Aplikasi ini menyediakan sebuah sistem pemesanan tiket bus daring yang komprehensif. Fitur utama mencakup pencarian jadwal perjalanan berdasarkan kota asal, kota tujuan, dan tanggal keberangkatan. Pengguna dapat meninjau daftar jadwal yang tersedia, memilih kursi secara interaktif sesuai dengan denah bus, dan melakukan konfirmasi pemesanan. Lebih lanjut, sistem ini juga mendukung fungsionalitas administratif untuk pengelolaan data bus, rute perjalanan, jadwal keberangkatan, dan konfigurasi kursi untuk setiap jadwal.

Dependensi dan Teknologi
Backend (Python Pyramid)
pyramid==2.0.2
pyramid_jinja2
pyramid_tm
SQLAlchemy==2.0.x
alembic
psycopg2-binary
zope.sqlalchemy
Frontend (React + Tailwind CSS)
react
react-dom
react-router-dom
tailwindcss
create-react-app (opsional)
@heroicons/react (opsional)

Fitur Aplikasi
Untuk Pengguna:
Pencarian perjalanan berdasarkan kota asal, tujuan, dan tanggal keberangkatan.
Peninjauan daftar jadwal bus yang tersedia.
Pemilihan kursi secara interaktif berdasarkan tata letak kursi bus.
Konfirmasi pemesanan kursi.
Untuk Admin:
Manajemen data bus (penambahan, perubahan, penghapusan).
Manajemen rute perjalanan.
Manajemen jadwal perjalanan bus.
Manajemen konfigurasi kursi per jadwal.

Referensi
Dokumentasi Pyramid: https://docs.pylonsproject.org/projects/pyramid/en/latest/
Dokumentasi React: https://reactjs.org/
Dokumentasi Tailwind CSS: https://tailwindcss.com/
Dokumentasi PostgreSQL: https://www.postgresql.org/docs/
MDN Web Docs - Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

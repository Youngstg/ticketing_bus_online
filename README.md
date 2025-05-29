# 🚌 Whiish - Sistem Pemesanan Tiket Bus Online

**Whiish** adalah aplikasi web berbasis React dan Pyramid yang memungkinkan pengguna untuk mencari perjalanan bus, memilih kursi, dan memesan tiket secara daring dengan antarmuka yang modern dan interaktif.

---

## 📄 Deskripsi Aplikasi Web

Aplikasi ini menyediakan sistem pemesanan tiket bus online dengan fitur pencarian jadwal berdasarkan kota asal, tujuan, dan tanggal keberangkatan. Pengguna dapat melihat daftar jadwal yang tersedia, memilih kursi secara interaktif, dan melakukan konfirmasi pemesanan. Sistem juga mendukung manajemen data bus, rute, jadwal, dan kursi melalui halaman admin.

---

## 📦 Dependensi & Teknologi

### 🔧 Backend (Python Pyramid)
- `pyramid==2.0.2`
- `pyramid_jinja2`
- `pyramid_tm`
- `SQLAlchemy==2.0.x`
- `alembic`
- `psycopg2-binary`
- `zope.sqlalchemy`

### 🎨 Frontend (React + Tailwind CSS)
- `react`
- `react-dom`
- `react-router-dom`
- `tailwindcss`
- `create-react-app` (opsional)
- `@heroicons/react` (opsional)

---

## 🚀 Fitur Aplikasi

### Untuk Pengguna:
- 🔍 Cari perjalanan berdasarkan asal, tujuan, dan tanggal keberangkatan
- 📆 Lihat daftar jadwal bus yang tersedia
- 🎟️ Pilih kursi secara interaktif sesuai layout bus
- ✅ Konfirmasi pemesanan kursi

### Untuk Admin:
- 🚌 Manajemen data bus (tambah, ubah, hapus)
- 📍 Manajemen rute perjalanan
- 🕒 Manajemen jadwal perjalanan bus
- 💺 Manajemen kursi per jadwal

---

## 📚 Referensi

- [Pyramid Documentation](https://docs.pylonsproject.org/projects/pyramid/en/latest/)
- [React Documentation](https://reactjs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MDN Web Docs - Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

> Proyek ini dibuat untuk memenuhi tugas besar mata kuliah *Pemrograman Web 2024/2025*.

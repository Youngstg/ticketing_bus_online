import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api'; // Pastikan path ini benar
import Navbar from '../components/Navbar';

const ReviewBooking = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { schedule, seat } = location.state || {};

  if (!schedule || !seat) {
    // Redirect jika tidak ada state (misal, akses langsung URL)
    navigate('/'); 
    return <div className="container p-4 mx-auto text-center">Data pemesanan tidak ditemukan. Mengalihkan...</div>;
  }

  const handlePayment = async () => {
    // Ambil userId. Implementasi ini mungkin perlu disesuaikan dengan sistem auth Anda.
    // Contoh: mengambil dari localStorage setelah login.
    const userIdString = localStorage.getItem('userId');
    if (!userIdString) {
      alert('Anda harus login untuk melanjutkan pembayaran.');
      navigate('/login'); // Arahkan ke halaman login jika belum login
      return;
    }

    const userId = parseInt(userIdString);
    if (isNaN(userId)) {
        alert('User ID tidak valid.');
        return;
    }

    const ticketData = {
      user_id: userId,
      schedule_id: schedule.id,
      seat_id: seat.id,
      status: 'booked', // Atau 'pending_payment' tergantung alur Anda
    };

    try {
      const createdTicket = await api.createTicket(ticketData);
      console.log('Ticket created:', createdTicket);
      // Navigasi ke halaman payment dengan membawa data yang diperlukan
      navigate('/payment', { 
        state: { 
          schedule, 
          seat, 
          ticket: createdTicket // Mengirim data tiket yang baru dibuat
        } 
      });
    } catch (error) {
      console.error('Failed to create ticket:', error);
      alert(error.response?.data?.message || 'Gagal membuat tiket. Silakan coba lagi.');
    }
  };

  return (
    <>
      <Navbar />
      <div className="container max-w-2xl p-4 mx-auto">
        <h1 className="mb-8 text-3xl font-bold text-center text-gray-800">Review Pemesanan Anda</h1>

        <div className="p-8 bg-white rounded-lg shadow-xl">
          <div className="pb-6 mb-6 border-b border-gray-200">
            <h2 className="mb-3 text-2xl font-semibold text-indigo-600">Detail Perjalanan</h2>
            <p className="text-lg text-gray-700"><span className="font-semibold">Rute:</span> {schedule.route.origin} - {schedule.route.destination}</p>
            <p className="text-lg text-gray-700"><span className="font-semibold">Bus:</span> {schedule.bus.name} ({schedule.bus.license_plate})</p>
            <p className="text-lg text-gray-700"><span className="font-semibold">Tanggal:</span> {new Date(schedule.departure_time).toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
            <p className="text-lg text-gray-700"><span className="font-semibold">Waktu Keberangkatan:</span> {new Date(schedule.departure_time).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })} WIB</p>
          </div>

          <div className="pb-6 mb-6 border-b border-gray-200">
            <h2 className="mb-3 text-2xl font-semibold text-indigo-600">Kursi Dipilih</h2>
            <p className="text-lg text-gray-700"><span className="font-semibold">Nomor Kursi:</span> {seat.seat_number}</p>
          </div>
          
          <div className="mb-8">
             <h2 className="mb-3 text-2xl font-semibold text-indigo-600">Rincian Harga</h2>
            <div className="flex items-center justify-between text-lg text-gray-700">
              <span>Harga Tiket:</span>
              <span className="font-semibold">Rp {schedule.price.toLocaleString('id-ID')}</span>
            </div>
             {/* Bisa ditambahkan biaya layanan atau PPN jika ada */}
            <div className="flex items-center justify-between pt-4 mt-4 text-xl text-gray-800 border-t border-gray-300">
              <span className="font-bold">Total Pembayaran:</span>
              <span className="font-bold text-indigo-600">Rp {schedule.price.toLocaleString('id-ID')}</span>
            </div>
          </div>

          <button
            onClick={handlePayment}
            className="w-full px-4 py-3 text-lg font-bold text-white transition-colors bg-green-500 rounded-lg shadow-md hover:bg-green-600"
          >
            Lanjutkan ke Pembayaran
          </button>
        </div>
      </div>
    </>
  );
};

export default ReviewBooking;
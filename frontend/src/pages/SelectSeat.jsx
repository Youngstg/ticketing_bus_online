import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { fetchSeats } from '../api';

const rows = 6;
const cols = 4;
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

const SelectSeat = () => {
  const { state: trip } = useLocation();
  const navigate = useNavigate();
  const [selectedSeat, setSelectedSeat] = useState(null);
  const [bookedSeats, setBookedSeats] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip?.id) {
      console.error('No trip ID found');
      return;
    }
    
    console.log('Fetching seats for schedule ID:', trip.id);
    fetchSeats(trip.id)
      .then((data) => {
        console.log('Seats data received:', data);
        const booked = data
          .filter(seat => seat.is_booked || seat.status === 'booked')
          .map(seat => seat.seat_number);
        setBookedSeats(booked);
      })
      .catch((err) => {
        console.error('Error fetching seats:', err);
        alert("Gagal mengambil data kursi: " + err.message);
      });
  }, [trip]);

  const handleSelect = (seatId) => {
    if (bookedSeats.includes(seatId)) return;
    setSelectedSeat(seatId === selectedSeat ? null : seatId);
  };

  const handleConfirm = async () => {
    if (!selectedSeat) {
      alert("Pilih kursi terlebih dahulu");
      return;
    }

    setLoading(true);
    
    // Simulasi loading untuk user experience
    setTimeout(() => {
      // Update local state untuk menandai kursi sebagai booked
      setBookedSeats(prev => [...prev, selectedSeat]);
      
      // Tampilkan notifikasi booking berhasil
      alert("Booking berhasil! Kursi " + selectedSeat + " telah dipesan.");
      
      // Navigasi ke halaman berikutnya
      navigate('/review-booking', {
        state: { 
          trip, 
          selectedSeat,
          bookingStatus: 'success'
        },
      });
      
      setLoading(false);
    }, 1000); // 1 detik delay untuk simulasi proses booking
  };

  const renderSeats = () => {
    const seatRows = [];

    for (let row = 0; row < rows; row++) {
      const seats = [];
      for (let col = 0; col < cols; col++) {
        const seatId = `${alphabet[row]}${col + 1}`;
        const isBooked = bookedSeats.includes(seatId);
        const isSelected = seatId === selectedSeat;

        seats.push(
          <button
            key={seatId}
            onClick={() => handleSelect(seatId)}
            className={`w-12 h-12 m-1 rounded-md font-medium text-sm ${
              isBooked
                ? 'bg-gray-600 text-gray-300 cursor-not-allowed'
                : isSelected
                ? 'bg-blue-500 text-white'
                : 'bg-[#2c2c2e] text-white hover:bg-blue-600'
            }`}
            disabled={isBooked}
          >
            {seatId}
          </button>
        );

        if (col === 1) {
          seats.push(<div key={`spacer-${row}`} className="w-6" />);
        }
      }

      seatRows.push(
        <div key={`row-${row}`} className="flex justify-center mb-2">
          {seats}
        </div>
      );
    }

    return seatRows;
  };

  if (!trip) {
    return (
      <div className="bg-[#0e0e10] text-white min-h-screen flex items-center justify-center">
        <p>No trip data found</p>
      </div>
    );
  }

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-12 px-6">
      <div className="max-w-xl mx-auto text-center">
        <h2 className="mb-2 text-2xl font-bold text-blue-400">
          {trip?.bus} — {trip?.time} to {trip?.arrival}
        </h2>
        <p className="mb-6 text-sm text-gray-400">
          {trip?.duration} • {trip?.price}
        </p>

        {renderSeats()}

        <div className="mt-6 text-lg">
          Selected Seat:{' '}
          <span className="font-semibold text-blue-400">
            {selectedSeat || 'None'}
          </span>
        </div>

        <button
          onClick={handleConfirm}
          className="px-6 py-3 mt-6 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl disabled:opacity-40"
          disabled={!selectedSeat || loading}
        >
          {loading ? 'Processing...' : 'Confirm Seat'}
        </button>
      </div>
    </section>
  );
};

export default SelectSeat;
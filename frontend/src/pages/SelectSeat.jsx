import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';


const rows = 6;
const cols = 4;
const bookedSeats = ['A2', 'B3'];

const SelectSeat = () => {
  const { state: trip } = useLocation();
  const [selectedSeat, setSelectedSeat] = useState(null);
  const navigate = useNavigate();


  const handleSelect = (seatId) => {
    if (bookedSeats.includes(seatId)) return;
    setSelectedSeat(seatId === selectedSeat ? null : seatId);
  };

  const renderSeats = () => {
    const seatRows = [];
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

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

        // Tambah lorong setelah kolom 2 (antara A2 dan A3)
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

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-12 px-6">
      <div className="max-w-xl mx-auto text-center">
        <h2 className="text-2xl font-bold mb-2 text-blue-400">
          {trip?.bus} — {trip?.time} to {trip?.arrival}
        </h2>
        <p className="text-sm text-gray-400 mb-6">
          {trip?.duration} • {trip?.price}
        </p>

        {/* Seat Layout */}
        {renderSeats()}

        <div className="text-lg mt-6">
          Selected Seat:{' '}
          <span className="text-blue-400 font-semibold">
            {selectedSeat || 'None'}
          </span>
        </div>

        <button
        onClick={() => navigate('/review-booking', {
            state: { trip, selectedSeat }
        })}
        className="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl disabled:opacity-40"
        disabled={!selectedSeat}
        >
        Confirm Seat
        </button>

      </div>
    </section>
  );
};

export default SelectSeat;

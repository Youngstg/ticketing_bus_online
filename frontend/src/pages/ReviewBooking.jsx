import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ReviewBooking = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { trip, selectedSeat } = state || {};

  const handleProceed = () => {
    alert('Proceeding to payment...');
    // navigate('/payment'); // Uncomment if payment route exists
  };

  if (!trip || !selectedSeat) {
    return (
      <div className="text-white text-center py-20">
        <h2 className="text-2xl font-bold">Invalid booking data.</h2>
      </div>
    );
  }

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-16 px-6">
      <div className="max-w-xl mx-auto bg-[#1a1a1d] p-10 rounded-3xl shadow-lg text-center">
        <h2 className="text-3xl font-bold mb-6 text-blue-400">Review Your Booking</h2>

        <div className="text-left space-y-4 text-gray-200">
          <p><strong>Bus:</strong> {trip.bus}</p>
          <p><strong>Departure:</strong> {trip.time}</p>
          <p><strong>Arrival:</strong> {trip.arrival}</p>
          <p><strong>Duration:</strong> {trip.duration}</p>
          <p><strong>Seat:</strong> <span className="text-blue-400 font-semibold">{selectedSeat}</span></p>
          <p><strong>Price:</strong> {trip.price}</p>
        </div>

        <button
          onClick={handleProceed}
          className="mt-8 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl"
        >
          Proceed to Payment
        </button>
      </div>
    </section>
  );
};

export default ReviewBooking;

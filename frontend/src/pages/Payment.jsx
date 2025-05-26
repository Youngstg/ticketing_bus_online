import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Payment = ({ orders, setOrders }) => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { trip, selectedSeat, orderId } = state || {};

  const handlePayment = () => {
    if (orderId != null) {
      // Update status existing order from history
      const updated = orders.map((order) =>
        order.id === orderId ? { ...order, status: 'Paid' } : order
      );
      setOrders(updated);
    } else {
      // Simpan order baru dari ReviewBooking
      const newOrder = {
        id: Date.now(),
        bus: trip.bus,
        seat: selectedSeat,
        departure: trip.time,
        arrival: trip.arrival,
        duration: trip.duration,
        status: 'Paid',
      };
      setOrders([...orders, newOrder]);
    }

    alert('Payment successful!');
    navigate('/history');
  };

  if (!trip && orderId == null) {
    return (
      <div className="py-20 text-center text-white">
        <h2 className="text-2xl font-bold">No booking data found.</h2>
      </div>
    );
  }

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-12 px-6">
      <div className="max-w-lg mx-auto bg-[#1a1a1d] p-10 rounded-3xl shadow-lg">
        <h2 className="mb-6 text-3xl font-bold text-center">Payment</h2>
        <p className="mb-4 text-sm text-center text-gray-300">You are about to pay for:</p>
        <div className="mb-8 space-y-3 text-left text-gray-200">
          <p><strong>Bus:</strong> {trip?.bus || '—'}</p>
          <p><strong>Seat:</strong> {selectedSeat || '—'}</p>
          <p><strong>Departure:</strong> {trip?.time || '—'}</p>
          <p><strong>Arrival:</strong> {trip?.arrival || '—'}</p>
          <p><strong>Price:</strong> {trip?.price || '$0'}</p>
        </div>

        <button
          onClick={handlePayment}
          className="w-full py-3 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl"
        >
          Pay Now
        </button>
      </div>
    </section>
  );
};

export default Payment;

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchTicketDetail } from '../api';

const TicketDetail = () => {
  const { id } = useParams();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTicketDetail(id)
      .then(setTicket)
      .catch(err => alert("Gagal memuat detail tiket: " + err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="p-6 text-white">Loading...</p>;
  if (!ticket) return <p className="p-6 text-white">Ticket not found</p>;

  return (
    <div className="bg-[#0e0e10] text-white min-h-screen p-6">
      <h2 className="mb-6 text-3xl font-bold">Ticket Detail</h2>
      <div className="bg-[#1a1a1d] p-6 rounded-lg shadow-md border border-[#2c2c2e] space-y-2">
        <p><strong>Customer:</strong> {ticket.customer_name}</p>
        <p><strong>Booking Code:</strong> {ticket.booking_code}</p>
        <p><strong>Status:</strong> {ticket.status}</p>
        <p><strong>Seat:</strong> {ticket.seat_number}</p>
        <p><strong>From:</strong> {ticket.origin}</p>
        <p><strong>To:</strong> {ticket.destination}</p>
        <p><strong>Departure Time:</strong> {ticket.departure_time}</p>
        <p><strong>Bus:</strong> {ticket.bus_name}</p>
        <p><strong>Total Price:</strong> Rp{ticket.price}</p>
      </div>
    </div>
  );
};

export default TicketDetail;

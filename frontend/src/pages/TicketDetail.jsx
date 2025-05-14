import React from 'react';
import { useParams } from 'react-router-dom';

const TicketDetail = () => {
  const { id } = useParams();
  const ticket = {
    id,
    from: 'Jakarta',
    to: 'Bandung',
    time: '16:20',
    date: '2025-06-01',
    seat: '13',
    route: 'E58',
    station: 'Central Station',
    price: 'Rp150.000',
  };

  return (
    <div className="bg-[#0e0e10] text-white min-h-screen p-6">
      <h2 className="text-3xl font-bold mb-6">Ticket Detail</h2>
      <div className="bg-[#1a1a1d] p-6 rounded-lg shadow-md border border-[#2c2c2e] space-y-2">
        <p><strong>From:</strong> {ticket.from}</p>
        <p><strong>To:</strong> {ticket.to}</p>
        <p><strong>Date:</strong> {ticket.date}</p>
        <p><strong>Time:</strong> {ticket.time}</p>
        <p><strong>Seat:</strong> {ticket.seat}</p>
        <p><strong>Route:</strong> {ticket.route}</p>
        <p><strong>Station:</strong> {ticket.station}</p>
        <p><strong>Total Price:</strong> {ticket.price}</p>
      </div>
    </div>
  );
};

export default TicketDetail;

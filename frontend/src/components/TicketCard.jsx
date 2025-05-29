import React from 'react';
import { Link } from 'react-router-dom';

const TicketCard = ({ ticket }) => {
  return (
    <div className="bg-[#1a1a1d] text-white p-4 rounded-lg flex justify-between items-center border border-gray-700">
      <div>
        <p className="text-lg font-semibold">{ticket.origin} → {ticket.destination}</p>
        <p className="text-sm text-gray-300">Bus: {ticket.bus_name}</p>
        <p className="text-sm text-gray-300">Seat: {ticket.seat_number} | Code: {ticket.booking_code}</p>
        <p className="text-sm text-gray-300">Time: {ticket.departure_time} | Status: {ticket.status}</p>
      </div>
      <Link to={`/ticket/${ticket.id}`}>
        <button className="px-4 py-2 text-white bg-blue-600 rounded">View</button>
      </Link>
    </div>
  );
};

export default TicketCard;

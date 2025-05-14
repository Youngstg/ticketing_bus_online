import React from 'react';
import { Link } from 'react-router-dom';

const TicketCard = ({ ticket }) => {
  return (
    <div className="bg-[#1a1a1d] text-white p-6 rounded-lg shadow-md border border-[#2c2c2e]">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-xl font-semibold">{ticket.from} → {ticket.to}</h3>
          <p className="text-gray-400 text-sm">{ticket.date} • {ticket.time}</p>
        </div>
        <Link
          to={`/ticket/${ticket.id}`}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
        >
          View
        </Link>
      </div>
    </div>
  );
};

export default TicketCard;

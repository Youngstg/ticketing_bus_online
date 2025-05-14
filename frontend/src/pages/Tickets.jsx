import React from 'react';
import TicketCard from '../components/TicketCard';

const Tickets = () => {
  const tickets = [
    { id: '1', from: 'Jakarta', to: 'Bandung', time: '16:20', date: '2025-06-01', seat: '13' },
    { id: '2', from: 'Solo', to: 'Yogyakarta', time: '14:00', date: '2025-06-03', seat: '22' },
  ];

  return (
    <div className="bg-[#0e0e10] text-white p-6 min-h-screen">
      <h2 className="text-3xl font-bold mb-6">Your Tickets</h2>
      <div className="space-y-4">
        {tickets.map(ticket => (
          <TicketCard key={ticket.id} ticket={ticket} />
        ))}
      </div>
    </div>
  );
};

export default Tickets;

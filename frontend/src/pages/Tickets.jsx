import React, { useEffect, useState } from 'react';
import TicketCard from '../components/TicketCard';
import { fetchTickets } from '../api';

const Tickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  fetchTickets()
    .then(data => {
      const filtered = data.filter(t => t.customer_name === 'Lucky');
      setTickets(filtered);
    })
    .catch(err => alert("Gagal memuat tiket: " + err.message))
    .finally(() => setLoading(false));
}, []);


  return (
    <div className="bg-[#0e0e10] text-white p-6 min-h-screen">
      <h2 className="mb-6 text-3xl font-bold">Your Tickets</h2>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="space-y-4">
          {tickets.length === 0 ? (
            <p>No tickets found.</p>
          ) : (
            tickets.map(ticket => (
              <TicketCard key={ticket.id} ticket={ticket} />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Tickets;

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchTickets } from '../api';

const formatDateTime = (datetime) => {
  const date = new Date(datetime);
  return `${date.toLocaleDateString()} • ${date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })}`;
};

const getDuration = (start, end) => {
  const ms = new Date(end) - new Date(start);
  const hours = Math.floor(ms / (1000 * 60 * 60));
  const minutes = Math.floor((ms / (1000 * 60)) % 60);
  return `${hours}h ${minutes}m`;
};

const History = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
  fetchTickets()
    .then(data => {
      const luckyOnly = data.filter(ticket => ticket.customer_name === 'Lucky');
      setTickets(luckyOnly);
    })
    .catch(err => alert("Gagal memuat tiket Lucky"))
    .finally(() => setLoading(false));
}, []);


  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-12 px-6">
      <div className="max-w-5xl mx-auto">
        <h2 className="mb-8 text-3xl font-bold text-center">Booking History</h2>

        {loading ? (
          <p className="text-center">Loading...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-[#1a1a1d] rounded-xl overflow-hidden">
              <thead className="bg-[#2c2c2e] text-left text-gray-400 text-sm uppercase">
                <tr>
                  <th className="px-6 py-4">Bus</th>
                  <th className="px-6 py-4">Seat</th>
                  <th className="px-6 py-4">Departure</th>
                  <th className="px-6 py-4">Arrival</th>
                  <th className="px-6 py-4">Duration</th>
                  <th className="px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((ticket) => (
                  <tr key={ticket.id} className="border-t border-[#2c2c2e] text-sm">
                    <td className="px-6 py-4">{ticket.bus_name}</td>
                    <td className="px-6 py-4">{ticket.seat_number}</td>
                    <td className="px-6 py-4">{formatDateTime(ticket.departure_time)}</td>
                    <td className="px-6 py-4">Unknown</td> {/* ❗Tambahkan jika Anda punya arrival_time */}
                    <td className="px-6 py-4">-</td> {/* Bisa dihitung jika ada arrival_time */}
                    <td className="px-6 py-4">
                      {ticket.status === 'Pending' ? (
                        <button
                          onClick={() =>
                            navigate('/payment', {
                              state: {
                                orderId: ticket.id,
                                trip: ticket,
                              },
                            })
                          }
                          className="px-3 py-1 text-xs font-semibold text-black bg-yellow-400 rounded-full hover:bg-yellow-500"
                        >
                          Pay Now
                        </button>
                      ) : (
                        <span className="px-3 py-1 text-xs font-semibold text-white bg-green-600 rounded-full">
                          Paid
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
};

export default History;

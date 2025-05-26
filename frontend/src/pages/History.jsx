import React from 'react';
import { useNavigate } from 'react-router-dom';

const orders = [
  {
    id: 1,
    bus: 'RouteMaster',
    seat: 'A1',
    departure: '2025-05-21T08:00',
    arrival: '2025-05-21T14:20',
    status: 'Paid',
    price: '$135',
  },
  {
    id: 2,
    bus: 'TravelGo',
    seat: 'B3',
    departure: '2025-05-28T09:15',
    arrival: '2025-05-28T16:25',
    status: 'Pending',
    price: '$150',
  },
];

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
  const navigate = useNavigate();

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-12 px-6">
      <div className="max-w-5xl mx-auto">
        <h2 className="mb-8 text-3xl font-bold text-center">Booking History</h2>

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
              {orders.map((order) => (
                <tr key={order.id} className="border-t border-[#2c2c2e] text-sm">
                  <td className="px-6 py-4">{order.bus}</td>
                  <td className="px-6 py-4">{order.seat}</td>
                  <td className="px-6 py-4">{formatDateTime(order.departure)}</td>
                  <td className="px-6 py-4">{formatDateTime(order.arrival)}</td>
                  <td className="px-6 py-4">{getDuration(order.departure, order.arrival)}</td>
                  <td className="px-6 py-4">
                    {order.status === 'Pending' ? (
                      <button
                        onClick={() =>
                          navigate('/payment', {
                            state: {
                              orderId: order.id,
                              trip: order,
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
      </div>
    </section>
  );
};

export default History;

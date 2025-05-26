import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer
} from 'recharts';
import { format } from 'date-fns';

// Dummy orders with createdAt
const dummyOrders = [
  {
    id: 1,
    user: 'alice@gmail.com',
    bus: 'RouteMaster',
    seat: 'A1',
    status: 'Paid',
    price: '$150',
    createdAt: '2025-05-01T12:30'
  },
  {
    id: 2,
    user: 'bob@gmail.com',
    bus: 'TravelGo',
    seat: 'B2',
    status: 'Pending',
    price: '$120',
    createdAt: '2025-05-08T09:00'
  },
  {
    id: 3,
    user: 'claire@gmail.com',
    bus: 'SkyBus',
    seat: 'C5',
    status: 'Paid',
    price: '$180',
    createdAt: '2025-05-15T11:45'
  }
];

const Dashboard = ({ user, orders = dummyOrders }) => {
  const navigate = useNavigate();

  if (!user || user.role !== 'admin') {
    return (
      <div className="py-20 text-center text-white">
        <h2 className="text-2xl font-bold">Access Denied</h2>
        <p>You do not have permission to view this page.</p>
      </div>
    );
  }

  const totalOrders = orders.length;
  const totalPaid = orders.filter((o) => o.status === 'Paid').length;
  const totalPending = orders.filter((o) => o.status === 'Pending').length;
  const totalRevenue = orders
    .filter((o) => o.status === 'Paid')
    .reduce((sum, o) => sum + parseFloat(o.price.replace('$', '')), 0);

  const handleLogout = () => {
    window.location.href = '/login';
  };

  // === Weekly Chart Data Generation ===
  const getWeekLabel = (date) => {
    const d = new Date(date);
    const start = new Date(d.setDate(d.getDate() - d.getDay()));
    return format(start, "'Week of' MMM d");
  };

  const grouped = {};
  orders.forEach((order) => {
    const week = getWeekLabel(order.createdAt);
    if (!grouped[week]) {
      grouped[week] = { week, bookings: 0, revenue: 0 };
    }
    grouped[week].bookings += 1;
    if (order.status === 'Paid') {
      const price = parseFloat(order.price?.replace('$', '') || 0);
      grouped[week].revenue += price;
    }
  });

  const weeklyChartData = Object.values(grouped).sort(
    (a, b) => new Date(a.week) - new Date(b.week)
  );

  return (
    <section className="bg-[#0e0e10] text-white min-h-screen py-6 px-6">
      {/* Header Top */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-3xl font-bold">Dashboard</h2>
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-sm bg-red-600 rounded-md hover:bg-red-700"
        >
          Logout
        </button>
      </div>

      {/* Statistik */}
      <div className="grid grid-cols-1 gap-6 mb-10 sm:grid-cols-2 md:grid-cols-4">
        <div className="bg-[#1a1a1d] p-6 rounded-xl text-center shadow-md">
          <h3 className="text-2xl font-bold">{totalOrders}</h3>
          <p className="text-sm text-gray-400">Total Bookings</p>
        </div>
        <div className="bg-[#1a1a1d] p-6 rounded-xl text-center shadow-md">
          <h3 className="text-2xl font-bold">{totalPaid}</h3>
          <p className="text-sm text-gray-400">Paid</p>
        </div>
        <div className="bg-[#1a1a1d] p-6 rounded-xl text-center shadow-md">
          <h3 className="text-2xl font-bold">{totalPending}</h3>
          <p className="text-sm text-gray-400">Pending</p>
        </div>
        <div className="bg-[#1a1a1d] p-6 rounded-xl text-center shadow-md">
          <h3 className="text-2xl font-bold">${totalRevenue}</h3>
          <p className="text-sm text-gray-400">Revenue</p>
        </div>
      </div>

      {/* Tabel semua pemesanan */}
      <div className="mb-16 overflow-x-auto">
        <table className="min-w-full bg-[#1a1a1d] rounded-xl overflow-hidden">
          <thead className="bg-[#2c2c2e] text-left text-gray-400 text-sm uppercase">
            <tr>
              <th className="px-6 py-4">User</th>
              <th className="px-6 py-4">Bus</th>
              <th className="px-6 py-4">Seat</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Price</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id} className="border-t border-[#2c2c2e] text-sm">
                <td className="px-6 py-4">{order.user}</td>
                <td className="px-6 py-4">{order.bus}</td>
                <td className="px-6 py-4">{order.seat}</td>
                <td className="px-6 py-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      order.status === 'Paid'
                        ? 'bg-green-600 text-white'
                        : 'bg-yellow-500 text-black'
                    }`}
                  >
                    {order.status}
                  </span>
                </td>
                <td className="px-6 py-4">{order.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Grafik Mingguan */}
      <div className="space-y-12">
        <div>
          <h3 className="mb-4 text-xl font-semibold">Weekly Bookings</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="bookings" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div>
          <h3 className="mb-4 text-xl font-semibold">Weekly Revenue</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weeklyChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#82ca9d" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
};

export default Dashboard;

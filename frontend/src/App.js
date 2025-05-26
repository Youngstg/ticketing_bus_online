import React, { useState } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation
} from 'react-router-dom';

import Navbar from './components/Navbar';
import Home from './pages/Home';
import Tickets from './pages/Tickets';
import TicketDetail from './pages/TicketDetail';
import SearchTrip from './pages/SearchTrip';
import SelectSeat from './pages/SelectSeat';
import ReviewBooking from './pages/ReviewBooking';
import Login from './pages/Login';
import Register from './pages/Register';
import History from './pages/History';
import Payment from './pages/Payment';
import Dashboard from './pages/admin/Dashboard';

function AppWrapper() {
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([
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
      createdAt: '2025-06-01T12:30'
    }
  ]);

  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith('/admin');

  return (
    <div className="min-h-screen text-gray-900 bg-white">
      {!isAdminRoute && <Navbar user={user} setUser={setUser} />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tickets" element={<Tickets />} />
        <Route path="/ticket/:id" element={<TicketDetail />} />
        <Route path="/search" element={<SearchTrip />} />
        <Route path="/select-seat" element={<SelectSeat />} />
        <Route path="/review-booking" element={<ReviewBooking />} />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/history" element={<History orders={orders} setOrders={setOrders} />} />
        <Route path="/payment" element={<Payment orders={orders} setOrders={setOrders} />} />
        <Route
          path="/admin/dashboard"
          element={<Dashboard user={user} orders={orders} />}
        />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}

export default App;

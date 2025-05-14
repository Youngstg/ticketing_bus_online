import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Tickets from './pages/Tickets';
import TicketDetail from './pages/TicketDetail';
import SearchTrip from './pages/SearchTrip';
import SelectSeat from './pages/SelectSeat';
import ReviewBooking from './pages/ReviewBooking';

function App() {
  return (
    <Router>
      <div className="bg-white min-h-screen text-gray-900">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tickets" element={<Tickets />} />
          <Route path="/ticket/:id" element={<TicketDetail />} />
          <Route path="/search" element={<SearchTrip />} />
          <Route path="/select-seat" element={<SelectSeat />} />
          <Route path="/review-booking" element={<ReviewBooking />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
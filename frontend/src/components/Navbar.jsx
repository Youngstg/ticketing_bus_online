import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = () => {
  return (
    <nav className="bg-[#0e0e10] text-white py-6 px-6 flex items-center justify-between relative">
      {/* Logo + Nama */}
      <div className="flex items-center space-x-4 z-10">
        <img src={logo} alt="Whiish Logo" className="w-17 h-14" />
        <h1 className="text-3xl font-extrabold font-poppins">Whiish</h1>
      </div>

      {/* Menu Tengah */}
      <div className="absolute left-1/2 transform -translate-x-1/2 flex space-x-12 text-1xl font-semibold tracking-wide">
        <Link to="/" className="hover:text-blue-400 transition">Home</Link>
        <Link to="/search" className="hover:text-blue-400 transition">Search</Link>
        <Link to="/tickets" className="hover:text-blue-400 transition">My Tickets</Link>
      </div>
    </nav>
  );
};

export default Navbar;

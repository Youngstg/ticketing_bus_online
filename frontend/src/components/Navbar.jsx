import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; // Ganti sesuai path logo Anda

const Navbar = ({ user, setUser }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    setUser(null);         // Hapus data user (logout)
    navigate('/login');    // Arahkan ke halaman login
  };

  return (
    <nav className="bg-[#0e0e10] text-white px-6 py-4 flex justify-between items-center">
      {/* Kiri: Logo */}
      <div className="flex items-center gap-2">
        <img src={logo} alt="logo" className="object-contain w-8 h-8" />
        <Link to="/" className="text-xl font-bold hover:text-blue-400">Whiish</Link>
      </div>

      {/* Tengah: Navigasi */}
      <div className="absolute hidden gap-8 text-sm font-medium -translate-x-1/2 md:flex left-1/2">
        <Link to="/" className="hover:text-blue-400">Home</Link>
        <Link to="/search" className="hover:text-blue-400">Search</Link>
        <Link to="/tickets" className="hover:text-blue-400">My Tickets</Link>
        <Link to="/history" className="hover:text-blue-400">History</Link>
      </div>

      {/* Kanan: Login/Register atau Logout */}
      <div className="flex items-center gap-4 ml-auto text-sm">
        {!user ? (
          <>
            <Link to="/login" className="hover:text-blue-400">Login</Link>
            <Link to="/register" className="hover:text-blue-400">Register</Link>
          </>
        ) : (
          <button
            onClick={handleLogout}
            className="px-3 py-1 text-sm bg-red-600 rounded-md hover:bg-red-700"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;

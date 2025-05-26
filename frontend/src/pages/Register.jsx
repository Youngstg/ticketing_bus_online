import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from '../assets/bg-logo.jpg'; // sesuaikan nama file gambarmu

const Register = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');

  const handleRegister = (e) => {
    e.preventDefault();

    if (password !== confirm) {
      alert('Passwords do not match!');
      return;
    }

    // Simulasi registrasi sukses
    alert('Account created!');
    navigate('/login');
  };

  return (
    <div
      className="flex items-center justify-center min-h-screen bg-center bg-cover"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      <div className="p-8 text-black bg-white shadow-lg bg-opacity-30 backdrop-blur-md rounded-xl w-96">
        <h2 className="mb-6 text-2xl font-bold text-center">Create Account</h2>

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm">Email</label>
            <input
              type="email"
              className="w-full px-4 py-2 bg-white rounded-md bg-opacity-80 focus:outline-none"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 bg-white rounded-md bg-opacity-80 focus:outline-none"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">Confirm Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 bg-white rounded-md bg-opacity-80 focus:outline-none"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-sm text-center">
          Already have an account?{' '}
          <a href="/login" className="text-blue-700 hover:underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
};

export default Register;

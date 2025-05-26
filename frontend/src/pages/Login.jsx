import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from '../assets/bg-logo.jpg'; // ganti dengan background sesuai kebutuhan

const Login = ({ setUser }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    const role = email.includes('@admin') ? 'admin' : 'user';
    const userData = { email, role };
    setUser(userData);

    // Redirect berdasarkan role
    if (role === 'admin') {
      navigate('/admin/dashboard');
    } else {
      navigate('/');
    }
  };

  return (
    <div
      className="flex items-center justify-center min-h-screen bg-center bg-cover"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      <div className="p-8 text-black bg-white shadow-lg bg-opacity-30 backdrop-blur-md rounded-xl w-96">
        <h2 className="mb-6 text-2xl font-bold text-center">Login</h2>

        <form onSubmit={handleLogin} className="space-y-4">
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

          <div className="flex items-center justify-between text-sm">
            <label>
              <input type="checkbox" className="mr-1" />
              Remember me
            </label>
            <button type="button" className="text-blue-700 hover:underline">
              Forgot Password?
            </button>
          </div>

          <button
            type="submit"
            className="w-full py-2 text-white bg-black rounded-md hover:bg-gray-900"
          >
            Login
          </button>
        </form>

        <p className="mt-4 text-sm text-center">
          Don’t have an account?{' '}
          <a href="/register" className="text-blue-700 hover:underline">
            Register
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;

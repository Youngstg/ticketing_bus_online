import React from 'react';
import { Link } from 'react-router-dom';
import bgImage from '../assets/bg-logo.jpg'; // sesuaikan nama file

const HeroSection = () => {
  return (
    <section
      className="text-white py-32 px-6 bg-cover bg-center relative"
      style={{
        backgroundImage: `url(${bgImage})`,
      }}
    >
      <div className="bg-black bg-opacity-60 absolute inset-0 z-0" />
      <div className="relative z-10 text-center max-w-3xl mx-auto">
        <h2 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
          Seamless Bus Booking with <span className="text-blue-400">Whiish</span>
        </h2>
        <p className="text-xl md:text-2xl text-gray-200 mb-10">
          Search schedules, pick your seat, and travel with ease — all in one modern platform.
        </p>
        <Link
          to="/search"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg md:text-xl px-8 py-4 rounded-md transition"
        >
          Start Booking
        </Link>
      </div>
    </section>
  );
};

export default HeroSection;

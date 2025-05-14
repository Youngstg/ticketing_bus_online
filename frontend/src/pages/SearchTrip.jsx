import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SearchTrip = () => {
  const [tripType, setTripType] = useState('oneway');
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = () => {
    setResults([
      {
        id: 1,
        bus: 'RouteMaster',
        time: '08:00 AM',
        duration: '6h 20m',
        arrival: '02:20 PM',
        price: '$135',
      },
      {
        id: 2,
        bus: 'TravelGo',
        time: '09:15 AM',
        duration: '7h 10m',
        arrival: '04:25 PM',
        price: '$150',
      },
    ]);
  };

  const handleSelectTrip = (trip) => {
    navigate('/select-seat', { state: trip });
  };

  return (
    <section className="bg-[#0e0e10] min-h-screen py-12 px-6 text-white">
      <div className="max-w-7xl mx-auto">
        {/* Switch Tabs */}
        <div className="flex justify-center mb-10">
          <button
            onClick={() => setTripType('oneway')}
            className={`px-6 py-2 font-semibold rounded-l-xl ${
              tripType === 'oneway' ? 'bg-blue-600 text-white' : 'bg-[#1a1a1d] text-gray-400'
            }`}
          >
            One Way
          </button>
          <button
            onClick={() => setTripType('roundtrip')}
            className={`px-6 py-2 font-semibold rounded-r-xl ${
              tripType === 'roundtrip' ? 'bg-blue-600 text-white' : 'bg-[#1a1a1d] text-gray-400'
            }`}
          >
            Round Trip
          </button>
        </div>

        {/* Form & Result Area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Form Panel */}
          <div className="bg-[#1a1a1d] p-8 rounded-3xl shadow-lg w-full">
            <h2 className="text-3xl font-bold mb-8">Book your Trip</h2>

            <div className="space-y-5">
              <div>
                <label className="block text-sm text-gray-400 mb-1">From</label>
                <input
                  type="text"
                  placeholder="Jakarta"
                  className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white border border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-1">To</label>
                <input
                  type="text"
                  placeholder="Bandung"
                  className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white border border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Departure</label>
                  <input
                    type="date"
                    className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                  />
                </div>

                {tripType === 'roundtrip' && (
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Return</label>
                    <input
                      type="date"
                      className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                    />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Passengers</label>
                  <input
                    type="number"
                    min="1"
                    defaultValue="1"
                    className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-1">Class</label>
                  <select className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white">
                    <option>Economy</option>
                    <option>Business</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleSearch}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition"
              >
                Search Trip
              </button>
            </div>
          </div>

          {/* Results Panel */}
          <div>
            <h3 className="text-2xl font-semibold mb-6">Available Trips</h3>
            {results.length === 0 ? (
              <p className="text-gray-500">No results yet. Please search above.</p>
            ) : (
              <div className="space-y-6">
                {results.map((trip) => (
                  <div
                    key={trip.id}
                    className="bg-[#1a1a1d] border border-[#2c2c2e] p-6 rounded-2xl flex flex-col md:flex-row md:items-center md:justify-between"
                  >
                    <div>
                      <h4 className="text-xl font-semibold mb-1">{trip.bus}</h4>
                      <p className="text-sm text-gray-400">
                        Depart {trip.time} • {trip.duration} • Arrive {trip.arrival}
                      </p>
                    </div>
                    <div className="mt-4 md:mt-0 flex flex-col items-end gap-2">
                      <p className="text-blue-400 text-2xl font-bold">{trip.price}</p>
                      <button
                        onClick={() => handleSelectTrip(trip)}
                        className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-xl"
                      >
                        Select Seat
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default SearchTrip;

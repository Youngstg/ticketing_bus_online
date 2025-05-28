import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchSchedulesBySearch } from '../api';

const SearchTrip = () => {
  const [tripType, setTripType] = useState('oneway');
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [departure, setDeparture] = useState('');
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = async () => {
    try {
      const trips = await fetchSchedulesBySearch({ origin, destination, date: departure });
      setResults(trips);
    } catch (err) {
      alert('❌ Failed to fetch trips: ' + err.message);
    }
  };

  const handleSelectTrip = (trip) => {
    const departureTime = new Date(trip.departure_time);
    const arrivalTime = new Date(departureTime.getTime() + trip.duration * 60000);

    navigate('/select-seat', {
      state: {
        id: trip.id,
        bus: trip.bus_name || trip.bus || 'Unknown Bus',
        time: departureTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        arrival: arrivalTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        duration: `${Math.floor(trip.duration / 60)}h ${trip.duration % 60}m`,
        price: trip.price ? `Rp ${trip.price.toLocaleString()}` : 'Rp -'
      }
    });
  };


  return (
    <section className="bg-[#0e0e10] min-h-screen py-12 px-6 text-white">
      <div className="mx-auto max-w-7xl">
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

        <div className="grid items-start grid-cols-1 gap-12 lg:grid-cols-2">
          <div className="bg-[#1a1a1d] p-8 rounded-3xl shadow-lg w-full">
            <h2 className="mb-8 text-3xl font-bold">Book your Trip</h2>

            <div className="space-y-5">
              <div>
                <label className="block mb-1 text-sm text-gray-400">From</label>
                <input
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  type="text"
                  placeholder="Jakarta"
                  className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white border border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block mb-1 text-sm text-gray-400">To</label>
                <input
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  type="text"
                  placeholder="Bandung"
                  className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white border border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                  <label className="block mb-1 text-sm text-gray-400">Departure</label>
                  <input
                    value={departure}
                    onChange={(e) => setDeparture(e.target.value)}
                    type="date"
                    className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                  />
                </div>

                {tripType === 'roundtrip' && (
                  <div>
                    <label className="block mb-1 text-sm text-gray-400">Return</label>
                    <input
                      type="date"
                      className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                    />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block mb-1 text-sm text-gray-400">Passengers</label>
                  <input
                    type="number"
                    min="1"
                    defaultValue="1"
                    className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white"
                  />
                </div>

                <div>
                  <label className="block mb-1 text-sm text-gray-400">Class</label>
                  <select className="w-full px-5 py-3 rounded-xl bg-[#2c2c2e] text-white">
                    <option>Economy</option>
                    <option>Business</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleSearch}
                className="w-full py-3 mt-6 font-bold text-white transition bg-blue-600 hover:bg-blue-700 rounded-xl"
              >
                Search Trip
              </button>
            </div>
          </div>

          <div>
            <h3 className="mb-6 text-2xl font-semibold">Available Trips</h3>
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
                      <h4 className="mb-1 text-xl font-semibold">{trip.bus}</h4>
                      <p className="text-sm text-gray-400">
                        Depart {trip.time} • {trip.duration} • Arrive {trip.arrival}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-2 mt-4 md:mt-0">
                      <p className="text-2xl font-bold text-blue-400">{trip.price}</p>
                      <button
                        onClick={() => handleSelectTrip(trip)}
                        className="px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-xl"
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

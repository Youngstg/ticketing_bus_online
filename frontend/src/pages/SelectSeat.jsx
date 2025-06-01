import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api'; // Pastikan path ini benar
import Navbar from '../components/Navbar';

const SelectSeat = () => {
  const { scheduleId } = useParams();
  const navigate = useNavigate();
  const [scheduleDetails, setScheduleDetails] = useState(null);
  const [seats, setSeats] = useState([]);
  const [selectedSeat, setSelectedSeat] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchScheduleDetails = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get(`/api/schedule/${scheduleId}`);
      setScheduleDetails(response.data);
    } catch (err) {
      console.error("Error fetching schedule details:", err);
      setError(err.response?.data?.message || "Failed to fetch schedule details.");
    }
  }, [scheduleId]);

  const fetchSeats = useCallback(async (busId) => {
    if (!busId) return;
    try {
      const response = await api.get(`/api/bus/${busId}/seats`);
      setSeats(response.data.sort((a, b) => a.seat_number.localeCompare(b.seat_number, undefined, { numeric: true })));
    } catch (err) {
      console.error("Error fetching seats:", err);
      setError(err.response?.data?.message || "Failed to fetch seats.");
    }
  }, []);

  useEffect(() => {
    fetchScheduleDetails();
  }, [fetchScheduleDetails]);

  useEffect(() => {
    if (scheduleDetails) {
      fetchSeats(scheduleDetails.bus.id);
    }
  }, [scheduleDetails, fetchSeats]);
  
  useEffect(() => {
    if (scheduleDetails && seats.length > 0) {
        setLoading(false);
    }
  }, [scheduleDetails, seats])

  const handleSeatSelect = (seat) => {
    if (!seat.is_booked) {
      setSelectedSeat(seat);
    }
  };

  const handleBooking = async () => {
    if (!selectedSeat) {
      alert('Please select a seat first.');
      return;
    }
    if (!scheduleDetails) {
        alert('Schedule details not loaded yet.');
        return;
    }

    try {
      // Tandai kursi sebagai sudah dibooking
      await api.bookSeat(selectedSeat.id); 
      // Navigasi ke halaman review booking dengan membawa data yang diperlukan
      navigate('/review-booking', { 
        state: { 
          schedule: scheduleDetails, 
          seat: selectedSeat 
        } 
      });
    } catch (bookingError) {
      console.error('Failed to book seat:', bookingError);
      alert(bookingError.response?.data?.message || 'Failed to book seat. It might already be taken or an error occurred.');
      // Refresh kursi untuk mendapatkan status terbaru
      if(scheduleDetails && scheduleDetails.bus) {
        fetchSeats(scheduleDetails.bus.id);
      }
    }
  };
  
  if (loading) return <div className="container p-4 mx-auto text-center">Loading...</div>;
  if (error) return <div className="container p-4 mx-auto text-center text-red-500">Error: {error}</div>;
  if (!scheduleDetails) return <div className="container p-4 mx-auto text-center">Schedule not found.</div>;

  const busLayout = {
    rows: scheduleDetails.bus.layout?.rows || 5, // Default jika tidak ada layout
    cols: scheduleDetails.bus.layout?.cols || 4, // Default jika tidak ada layout
    gap: scheduleDetails.bus.layout?.gap || 2,
    aisleAfter: scheduleDetails.bus.layout?.aisleAfter || 2,
  };

  const seatMap = seats.reduce((map, seat) => {
    map[seat.seat_number] = seat;
    return map;
  }, {});


  return (
    <>
      <Navbar />
      <div className="container p-4 mx-auto">
        <h1 className="mb-6 text-3xl font-bold text-center text-gray-800">Pilih Kursi</h1>
        <div className="p-6 mb-6 bg-white rounded-lg shadow-xl">
          <h2 className="mb-4 text-2xl font-semibold text-indigo-600">{scheduleDetails.route.origin} ke {scheduleDetails.route.destination}</h2>
          <p className="text-gray-700"><span className="font-semibold">Bus:</span> {scheduleDetails.bus.name} ({scheduleDetails.bus.license_plate})</p>
          <p className="text-gray-700"><span className="font-semibold">Tanggal:</span> {new Date(scheduleDetails.departure_time).toLocaleDateString()}</p>
          <p className="text-gray-700"><span className="font-semibold">Waktu Keberangkatan:</span> {new Date(scheduleDetails.departure_time).toLocaleTimeString()}</p>
          <p className="text-gray-700"><span className="font-semibold">Harga:</span> Rp {scheduleDetails.price.toLocaleString()}</p>
        </div>

        <div className="p-6 bg-white rounded-lg shadow-xl">
          <h3 className="mb-4 text-xl font-semibold text-center text-gray-700">Layout Kursi</h3>
          <div className="flex justify-center">
            <div 
              className="grid gap-2 p-4 bg-gray-100 border rounded-md"
              style={{
                gridTemplateColumns: `repeat(${busLayout.cols + (busLayout.gap > 0 ? 1 : 0)}, minmax(0, 1fr))`,
                width: `${(busLayout.cols + (busLayout.gap > 0 ? 1 : 0)) * 3.5}rem` // Estimasi lebar berdasarkan jumlah kolom
              }}
            >
              {Array.from({ length: busLayout.rows * busLayout.cols }).map((_, index) => {
                const row = Math.floor(index / busLayout.cols) + 1;
                const col = (index % busLayout.cols) + 1;
                const seatNumber = `${String.fromCharCode(64 + row)}${col}`; // A1, A2, B1, B2, ...
                const seat = seatMap[seatNumber];
                
                const isSelected = selectedSeat && seat && selectedSeat.id === seat.id;
                const isBooked = seat && seat.is_booked;

                let colSpanClass = '';
                if (busLayout.gap > 0 && col === busLayout.aisleAfter + 1) {
                   colSpanClass = `col-start-${col + 1}`; // Pindah ke kolom setelah lorong
                }


                if (busLayout.gap > 0 && col === busLayout.aisleAfter) {
                    return (
                    <React.Fragment key={`seat-${seatNumber}-aisle`}>
                         <button
                            key={`seat-${seatNumber}`}
                            onClick={() => seat && handleSeatSelect(seat)}
                            disabled={isBooked}
                            className={`
                              p-2 border rounded text-center text-sm font-medium transition-colors
                              ${isBooked ? 'bg-red-400 text-white cursor-not-allowed' : ''}
                              ${!isBooked && isSelected ? 'bg-green-500 text-white' : ''}
                              ${!isBooked && !isSelected ? 'bg-blue-200 hover:bg-blue-400 text-blue-800' : ''}
                              ${colSpanClass}
                            `}
                          >
                            {seatNumber}
                          </button>
                        <div key={`aisle-${row}-${col}`} className="w-8" /> {/* Lorong */}
                    </React.Fragment>
                    );
                }


                return (
                  <button
                    key={`seat-${seatNumber}`}
                    onClick={() => seat && handleSeatSelect(seat)}
                    disabled={isBooked}
                    className={`
                      p-2 border rounded text-center text-sm font-medium transition-colors
                      ${isBooked ? 'bg-red-400 text-white cursor-not-allowed' : ''}
                      ${!isBooked && isSelected ? 'bg-green-500 text-white' : ''}
                      ${!isBooked && !isSelected ? 'bg-blue-200 hover:bg-blue-400 text-blue-800' : ''}
                       ${colSpanClass}
                    `}
                  >
                    {seat ? seatNumber : '-'}
                  </button>
                );
              })}
            </div>
          </div>
          <div className="flex justify-center mt-6">
            <button
              onClick={handleBooking}
              disabled={!selectedSeat || loading}
              className="px-6 py-3 font-bold text-white transition-colors bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 disabled:opacity-50"
            >
              Pesan Sekarang
            </button>
          </div>
           {selectedSeat && (
            <div className="mt-4 text-lg font-semibold text-center text-gray-700">
              Kursi Dipilih: {selectedSeat.seat_number}
            </div>
          )}
        </div>

        <div className="flex justify-around mt-6 text-sm">
            <div className="flex items-center"><span className="w-4 h-4 mr-2 bg-blue-200 border rounded"></span> Tersedia</div>
            <div className="flex items-center"><span className="w-4 h-4 mr-2 bg-green-500 border rounded"></span> Dipilih</div>
            <div className="flex items-center"><span className="w-4 h-4 mr-2 bg-red-400 border rounded"></span> Dipesan</div>
        </div>

      </div>
    </>
  );
};

export default SelectSeat;
import React, { useEffect, useState } from "react";
import { fetchSeats } from "../../api";

export default function SeatList({ scheduleId }) {
  const [seats, setSeats] = useState([]);

  useEffect(() => {
    fetchSeats(scheduleId).then(setSeats).catch(console.error);
  }, [scheduleId]);

  return (
    <div>
      <h3 className="font-semibold">Daftar Kursi</h3>
      <ul className="mt-2 space-y-1">
        {seats.map(seat => (
          <li key={seat.id}>
            Kursi {seat.seat_number} — {seat.is_booked ? "Dipesan" : "Kosong"}
          </li>
        ))}
      </ul>
    </div>
  );
}

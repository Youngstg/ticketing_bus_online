import React, { useEffect, useState } from "react";
import { fetchSchedules } from "../../api";

export default function ScheduleList() {
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    fetchSchedules().then(setSchedules).catch(console.error);
  }, []);

  return (
    <div>
      <h2 className="text-lg font-semibold">Daftar Jadwal</h2>
      <ul className="mt-2 space-y-1">
        {schedules.map(s => (
          <li key={s.id}>
            {s.departure_time} — Bus ID: {s.bus_id}, Rute ID: {s.route_id}, Harga: {s.price} IDR
          </li>
        ))}
      </ul>
    </div>
  );
}

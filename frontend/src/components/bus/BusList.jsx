import React, { useEffect, useState } from "react";
import { fetchBuses } from "../../api";

export default function BusList() {
  const [buses, setBuses] = useState([]);

  useEffect(() => {
    fetchBuses().then(setBuses).catch(console.error);
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold">Daftar Bus</h2>
      <ul className="mt-2">
        {buses.map(bus => (
          <li key={bus.id}>
            {bus.name} - {bus.license_plate}
          </li>
        ))}
      </ul>
    </div>
  );
}

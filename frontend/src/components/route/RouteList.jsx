import React, { useEffect, useState } from "react";
import { fetchRoutes } from "../../api";

export default function RouteList() {
  const [routes, setRoutes] = useState([]);

  useEffect(() => {
    fetchRoutes().then(setRoutes).catch(console.error);
  }, []);

  return (
    <div>
      <h2 className="text-lg font-semibold">Daftar Rute</h2>
      <ul className="mt-2">
        {routes.map((r) => (
          <li key={r.id}>
            {r.origin} → {r.destination} ({r.duration} menit)
          </li>
        ))}
      </ul>
    </div>
  );
}

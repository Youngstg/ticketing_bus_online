import React, { useState, useEffect } from "react";
import { createSchedule, fetchBuses, fetchRoutes } from "../../api";

export default function AddScheduleForm() {
  const [busId, setBusId] = useState("");
  const [routeId, setRouteId] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [price, setPrice] = useState("");
  const [adminUser, setAdminUser] = useState("admin");
  const [adminPass, setAdminPass] = useState("admin123");
  const [buses, setBuses] = useState([]);
  const [routes, setRoutes] = useState([]);

  useEffect(() => {
    fetchBuses().then(setBuses).catch(console.error);
    fetchRoutes().then(setRoutes).catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const departure_time = `${date} ${time}`; // format "YYYY-MM-DD HH:MM"
    try {
      await createSchedule(
        { bus_id: parseInt(busId), route_id: parseInt(routeId), departure_time, price: parseInt(price) },
        adminUser,
        adminPass
      );
      alert("✅ Jadwal berhasil ditambahkan");
    } catch (err) {
      alert("❌ Gagal: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <select value={busId} onChange={e => setBusId(e.target.value)} className="w-full p-2 border">
        <option value="">Pilih Bus</option>
        {buses.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
      </select>

      <select value={routeId} onChange={e => setRouteId(e.target.value)} className="w-full p-2 border">
        <option value="">Pilih Rute</option>
        {routes.map(r => <option key={r.id} value={r.id}>{r.origin} → {r.destination}</option>)}
      </select>

      <input type="date" value={date} onChange={e => setDate(e.target.value)} className="w-full p-2 border" />
      <input type="time" value={time} onChange={e => setTime(e.target.value)} className="w-full p-2 border" />
      <input type="number" value={price} onChange={e => setPrice(e.target.value)} placeholder="Harga (Rp)" className="w-full p-2 border" />
      <input value={adminUser} onChange={e => setAdminUser(e.target.value)} className="w-full p-2 border" />
      <input type="password" value={adminPass} onChange={e => setAdminPass(e.target.value)} className="w-full p-2 border" />
      <button type="submit" className="px-4 py-2 text-white bg-purple-500">Tambah Jadwal</button>
    </form>
  );
}

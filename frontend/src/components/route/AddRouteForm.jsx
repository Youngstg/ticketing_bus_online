import React, { useState } from "react";
import { createRoute } from "../../api";

export default function AddRouteForm() {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [duration, setDuration] = useState("");
  const [adminUser, setAdminUser] = useState("admin");
  const [adminPass, setAdminPass] = useState("admin123");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createRoute(
        {
          origin,
          destination,
          duration: parseInt(duration)
        },
        adminUser,
        adminPass
      );
      alert("✅ Rute berhasil ditambahkan");
    } catch (err) {
      alert("❌ Gagal: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input value={origin} onChange={e => setOrigin(e.target.value)} placeholder="Kota Asal" className="w-full p-2 border" />
      <input value={destination} onChange={e => setDestination(e.target.value)} placeholder="Kota Tujuan" className="w-full p-2 border" />
      <input type="number" value={duration} onChange={e => setDuration(e.target.value)} placeholder="Durasi (menit)" className="w-full p-2 border" />
      <input value={adminUser} onChange={e => setAdminUser(e.target.value)} placeholder="Admin Username" className="w-full p-2 border" />
      <input type="password" value={adminPass} onChange={e => setAdminPass(e.target.value)} placeholder="Admin Password" className="w-full p-2 border" />
      <button type="submit" className="px-4 py-2 text-white bg-green-500">Tambah Rute</button>
    </form>
  );
}

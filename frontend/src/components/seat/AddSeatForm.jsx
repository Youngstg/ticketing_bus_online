import React, { useState } from "react";
import { createSeat } from "../../api";

export default function AddSeatForm({ scheduleId }) {
  const [seatNumber, setSeatNumber] = useState("");
  const [isBooked, setIsBooked] = useState(false);
  const [adminUser, setAdminUser] = useState("admin");
  const [adminPass, setAdminPass] = useState("admin123");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createSeat({
        schedule_id: scheduleId,
        seat_number: seatNumber,
        is_booked: isBooked
      }, adminUser, adminPass);
      alert("✅ Kursi berhasil ditambahkan");
    } catch (err) {
      alert("❌ Gagal: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input value={seatNumber} onChange={e => setSeatNumber(e.target.value)} placeholder="Nomor Kursi (misal A1)" className="w-full p-2 border" />
      <label className="flex items-center gap-2">
        <input type="checkbox" checked={isBooked} onChange={e => setIsBooked(e.target.checked)} />
        Sudah Dipesan
      </label>
      <input value={adminUser} onChange={e => setAdminUser(e.target.value)} placeholder="Admin Username" className="w-full p-2 border" />
      <input type="password" value={adminPass} onChange={e => setAdminPass(e.target.value)} placeholder="Admin Password" className="w-full p-2 border" />
      <button type="submit" className="px-4 py-2 text-white bg-emerald-600">Tambah Kursi</button>
    </form>
  );
}

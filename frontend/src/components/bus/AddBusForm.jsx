import React, { useState } from "react";
import { createBus } from "../../api";

export default function AddBusForm() {
  const [name, setName] = useState("");
  const [license, setLicense] = useState("");
  const [adminUser, setAdminUser] = useState("admin");
  const [adminPass, setAdminPass] = useState("admin123");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await createBus(
        { name, license_plate: license },
        adminUser,
        adminPass
      );
      alert("✅ Berhasil: " + result.message);
    } catch (err) {
      alert("❌ Gagal: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Nama Bus" className="w-full p-2 border" />
      <input value={license} onChange={e => setLicense(e.target.value)} placeholder="Plat Nomor" className="w-full p-2 border" />
      <input value={adminUser} onChange={e => setAdminUser(e.target.value)} placeholder="Admin Username" className="w-full p-2 border" />
      <input type="password" value={adminPass} onChange={e => setAdminPass(e.target.value)} placeholder="Admin Password" className="w-full p-2 border" />
      <button type="submit" className="px-4 py-2 text-white bg-blue-500">Tambah Bus</button>
    </form>
  );
}

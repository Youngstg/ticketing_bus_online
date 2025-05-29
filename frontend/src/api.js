const BASE_URL = "http://localhost:6543"; // ✅ pastikan ini BUKAN 3000

function handleError(res) {
  if (!res.ok) {
    return res.json().then(err => {
      throw new Error(err.error || "Request failed");
    });
  }
  return res.json();
}

export async function fetchBuses() {
  return fetch(`${BASE_URL}/api/buses`).then(handleError);
}

export async function createBus(data, username, password) {
  const auth = btoa(`${username}:${password}`);
  return fetch(`${BASE_URL}/api/buses/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${auth}`
    },
    body: JSON.stringify(data)
  }).then(handleError);
}

export async function fetchRoutes() {
  return fetch(`${BASE_URL}/api/routes`).then(handleError);
}

export async function createRoute(data, username, password) {
  const auth = btoa(`${username}:${password}`);
  return fetch(`${BASE_URL}/api/routes/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${auth}`
    },
    body: JSON.stringify(data)
  }).then(handleError);
}

export async function fetchSchedules() {
  return fetch(`${BASE_URL}/api/schedules`).then(handleError);
}

export async function createSchedule(data, username, password) {
  const auth = btoa(`${username}:${password}`);
  return fetch(`${BASE_URL}/api/schedules/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${auth}`
    },
    body: JSON.stringify(data)
  }).then(handleError);
}

export async function fetchSeats(scheduleId) {
  const res = await fetch(`${BASE_URL}/api/seats/${scheduleId}`);
  if (!res.ok) throw new Error("Failed to fetch seats");
  return res.json();
}

// Seat booking untuk customer (tidak perlu auth)
export async function createSeat(data) {
  const res = await fetch(`${BASE_URL}/api/seats/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Failed to create seat" }));
    throw new Error(err.error || "Failed to create seat");
  }

  return res.json();
}

// Seat management untuk admin (perlu auth)
export async function createSeatAdmin(data, username, password) {
  const auth = btoa(`${username}:${password}`);
  const res = await fetch(`${BASE_URL}/api/seats/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${auth}`
    },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Failed to create seat" }));
    throw new Error(err.error || "Failed to create seat");
  }

  return res.json();
}

export async function fetchSchedulesBySearch({ origin, destination, date }) {
  const params = new URLSearchParams({ origin, destination, date });
  return fetch(`${BASE_URL}/api/schedules/search?${params.toString()}`).then(handleError);
}

export async function fetchTickets() {
  return fetch(`${BASE_URL}/api/tickets`).then(handleError);
}

export async function fetchTicketDetail(id) {
  return fetch(`${BASE_URL}/api/tickets/detail/${id}`).then(handleError);
}

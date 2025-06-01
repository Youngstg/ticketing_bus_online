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


export const bookSeat = async (seatId) => {
  try {
    const response = await axiosInstance.put(`/api/seat/${seatId}/book`, { is_booked: true });
    return response.data;
  } catch (error) {
    console.error('Error booking seat:', error.response ? error.response.data : error.message);
    throw error;
  }
};

export const createTicket = async (ticketData) => {
  try {
    const response = await axiosInstance.post('/api/ticket', ticketData);
    return response.data;
  } catch (error) {
    console.error('Error creating ticket:', error.response ? error.response.data : error.message);
    throw error;
  }
};

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

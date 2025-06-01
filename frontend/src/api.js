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

// Fixed bookSeat function using fetch instead of axios
export const bookSeat = async (seatId) => {
  try {
    const response = await fetch(`${BASE_URL}/api/seat/${seatId}/book`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_booked: true })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Failed to book seat' }));
      throw new Error(errorData.error || 'Failed to book seat');
    }

    return response.json();
  } catch (error) {
    console.error('Error booking seat:', error.message);
    throw error;
  }
};

// Fixed createTicket function using fetch instead of axios
export const createTicket = async (ticketData) => {
  try {
    const response = await fetch(`${BASE_URL}/api/ticket`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ticketData)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Failed to create ticket' }));
      throw new Error(errorData.error || 'Failed to create ticket');
    }

    return response.json();
  } catch (error) {
    console.error('Error creating ticket:', error.message);
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

// Add missing functions that your components need
export async function fetchScheduleDetail(scheduleId) {
  return fetch(`${BASE_URL}/api/schedule/${scheduleId}`).then(handleError);
}

export async function fetchBusSeats(busId) {
  return fetch(`${BASE_URL}/api/bus/${busId}/seats`).then(handleError);
}

// Create an api object with all functions for easier usage
const api = {
  get: async (url) => {
    return fetch(`${BASE_URL}${url}`).then(handleError);
  },
  post: async (url, data) => {
    return fetch(`${BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(handleError);
  },
  put: async (url, data) => {
    return fetch(`${BASE_URL}${url}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(handleError);
  },
  // All the specific functions
  fetchBuses,
  createBus,
  fetchRoutes,
  createRoute,
  fetchSchedules,
  createSchedule,
  fetchSeats,
  createSeat,
  bookSeat,
  createTicket,
  fetchSchedulesBySearch,
  fetchTickets,
  fetchTicketDetail,
  fetchScheduleDetail,
  fetchBusSeats
};

// Export as default
export default api;
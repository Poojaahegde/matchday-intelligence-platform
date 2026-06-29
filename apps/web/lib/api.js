const BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function getMatches() {
  const r = await fetch(BASE + "/matches");
  return r.json();
}

export async function getAnalytics(id) {
  const r = await fetch(BASE + "/matches/" + id + "/analytics");
  return r.json();
}

export async function getEvents(id) {
  const r = await fetch(BASE + "/matches/" + id + "/events");
  return r.json();
}

export async function getReport(id) {
  const r = await fetch(BASE + "/matches/" + id + "/report");
  return r.json();
}

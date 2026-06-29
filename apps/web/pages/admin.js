import { useState } from "react";

const TYPES = [
  "goal", "assist", "yellow_card", "red_card",
  "substitution", "shot", "shot_on_target", "possession",
];

export default function Admin() {
  const [token, setToken] = useState("");
  const [matchId, setMatchId] = useState("1");
  const [minute, setMinute] = useState("1");
  const [type, setType] = useState("shot");
  const [status, setStatus] = useState("");

  async function submit(e) {
    e.preventDefault();
    const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
    const r = await fetch(base + "/admin/matches/" + matchId + "/events", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Admin-Token": token },
      body: JSON.stringify({ minute: Number(minute), type }),
    });
    setStatus(r.ok ? "Event added" : "Error " + r.status);
  }

  return (
    <main style={{ padding: 32, fontFamily: "system-ui" }}>
      <h1>Admin — add match event</h1>
      <form onSubmit={submit} style={{ display: "grid", gap: 8, maxWidth: 320 }}>
        <input placeholder="Admin token" value={token} onChange={(e) => setToken(e.target.value)} />
        <input placeholder="Match ID" value={matchId} onChange={(e) => setMatchId(e.target.value)} />
        <input placeholder="Minute" value={minute} onChange={(e) => setMinute(e.target.value)} />
        <select value={type} onChange={(e) => setType(e.target.value)}>
          {TYPES.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <button type="submit">Add event</button>
      </form>
      <p>{status}</p>
    </main>
  );
}

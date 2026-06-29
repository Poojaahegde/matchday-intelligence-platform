import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { getAnalytics, getEvents } from "../../lib/api";
import MomentumChart from "../../components/MomentumChart";

export default function MatchPage() {
  const { query } = useRouter();
  const id = query.id;
  const [analytics, setAnalytics] = useState(null);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    if (!id) return;
    getAnalytics(id).then(setAnalytics).catch(() => {});
    getEvents(id).then(setEvents).catch(() => {});

    const wsBase = process.env.NEXT_PUBLIC_WS_BASE || "ws://localhost:8000";
    const ws = new WebSocket(wsBase + "/ws/matches/" + id);
    ws.onmessage = () => getEvents(id).then(setEvents);
    const ping = setInterval(() => ws.readyState === 1 && ws.send("ping"), 5000);
    return () => {
      clearInterval(ping);
      ws.close();
    };
  }, [id]);

  return (
    <main style={{ padding: 32, fontFamily: "system-ui" }}>
      <h1>Match #{id}</h1>
      <h2>Momentum</h2>
      <MomentumChart momentum={analytics?.momentum || []} />
      <h2>Summary</h2>
      <pre>{JSON.stringify(analytics?.summary, null, 2)}</pre>
      <h2>Timeline</h2>
      <ol>
        {events.map((e) => (
          <li key={e.id}>
            {e.minute}&apos; — {e.type} {e.detail || ""}
          </li>
        ))}
      </ol>
    </main>
  );
}

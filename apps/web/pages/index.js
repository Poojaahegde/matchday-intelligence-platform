import { useEffect, useState } from "react";
import Link from "next/link";
import { getMatches } from "../lib/api";

export default function Home() {
  const [matches, setMatches] = useState([]);
  useEffect(() => {
    getMatches().then(setMatches).catch(() => {});
  }, []);
  return (
    <main style={{ padding: 32, fontFamily: "system-ui" }}>
      <h1>Matchday Intelligence</h1>
      <p>Live match dashboards and post-match analytics.</p>
      <ul>
        {matches.map((m) => (
          <li key={m.id}>
            <Link href={'/match/' + m.id}>Match #{m.id} ({m.status})</Link>
          </li>
        ))}
      </ul>
      {!matches.length && <p>No matches yet. Seed the DB to see the demo.</p>}
    </main>
  );
}

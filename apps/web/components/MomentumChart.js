export default function MomentumChart({ momentum = [] }) {
  if (!momentum.length) return <p>No momentum data yet.</p>;
  const max = Math.max(...momentum.map((m) => m.weight));
  return (
    <div style={{ display: "flex", gap: 4, alignItems: "flex-end", height: 120 }}>
      {momentum.map((m, i) => (
        <div
          key={i}
          title={'min ' + m.minute}
          style={{
            width: 14,
            height: (m.weight / max) * 100 + "%",
            background: "#2b8a3e",
          }}
        />
      ))}
    </div>
  );
}

interface Props {
  label: string;
  value: number;
}

export function ScoreBar({ label, value }: Props) {
  const pct = Math.round(value * 100);
  return (
    <div className="score-bar">
      <span className="score-bar__label">{label}</span>
      <div className="score-bar__track">
        <div className="score-bar__fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="score-bar__value">{pct}%</span>
    </div>
  );
}

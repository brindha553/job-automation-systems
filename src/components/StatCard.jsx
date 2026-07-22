function StatCard({ title, value, color }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg hover:shadow-cyan-500/20 transition">

      <h3 className="text-gray-400 text-sm font-medium">
        {title}
      </h3>

      <h2 className={`text-4xl font-bold mt-4 ${color}`}>
        {value}
      </h2>

    </div>
  );
}

export default StatCard;
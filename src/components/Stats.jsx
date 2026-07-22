import { motion } from "framer-motion";
import {
  FaBriefcase,
  FaBullseye,
  FaUsers,
  FaRobot,
} from "react-icons/fa";

function Stats() {
  const stats = [
    {
      number: "10K+",
      title: "Jobs Collected",
      icon: <FaBriefcase />,
    },
    {
      number: "95%",
      title: "Matching Accuracy",
      icon: <FaBullseye />,
    },
    {
      number: "500+",
      title: "Students",
      icon: <FaUsers />,
    },
    {
      number: "4",
      title: "AI Agents",
      icon: <FaRobot />,
    },
  ];

  return (
    <section className="bg-slate-950 py-24 px-8">

      <h2 className="text-center text-5xl font-bold text-white mb-16">
        Platform Statistics
      </h2>

      <div className="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-8">

        {stats.map((item, index) => (

          <motion.div
            key={index}
            whileHover={{ scale: 1.05, y: -5 }}
            transition={{ duration: 0.3 }}
            className="bg-slate-900 rounded-2xl p-8 text-center border border-slate-700 hover:border-cyan-400 shadow-lg hover:shadow-cyan-500/20 transition-all"
          >

            <div className="text-4xl text-cyan-400 flex justify-center mb-5">
              {item.icon}
            </div>

            <h1 className="text-5xl font-extrabold text-cyan-400">
              {item.number}
            </h1>

            <p className="text-gray-300 mt-4 text-lg">
              {item.title}
            </p>

          </motion.div>

        ))}

      </div>

    </section>
  );
}

export default Stats;
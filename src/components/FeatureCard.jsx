import { motion } from "framer-motion";

function FeatureCard({ icon, title, description }) {
  return (
    <motion.div
      whileHover={{ y: -10, scale: 1.03 }}
      transition={{ duration: 0.3 }}
      className="bg-slate-900 border border-slate-700 rounded-2xl p-6 shadow-lg hover:border-cyan-400"
    >
      <div className="text-5xl mb-5">{icon}</div>

      <h3 className="text-2xl font-bold mb-3 text-white">
        {title}
      </h3>

      <p className="text-gray-400 leading-7">
        {description}
      </p>
    </motion.div>
  );
}

export default FeatureCard;
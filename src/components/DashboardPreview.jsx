import { motion } from "framer-motion";

function DashboardPreview() {
  return (
    <section className="bg-slate-950 py-24 px-8">

      <h2 className="text-5xl font-bold text-center text-white mb-4">
        Dashboard Preview
      </h2>

      <p className="text-center text-gray-400 max-w-3xl mx-auto mb-16">
        Get personalized job recommendations, resume insights, and AI-powered career guidance—all in one dashboard.
      </p>

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-6xl mx-auto bg-slate-900 border border-slate-700 rounded-3xl p-8"
      >

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-cyan-400 text-lg font-semibold">
              Resume Score
            </h3>
            <p className="text-4xl font-bold text-white mt-4">
              92%
            </p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-cyan-400 text-lg font-semibold">
              Best Match
            </h3>
            <p className="text-2xl text-white mt-4">
              ML Engineer
            </p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-cyan-400 text-lg font-semibold">
              Recommended Jobs
            </h3>
            <p className="text-4xl font-bold text-white mt-4">
              18
            </p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-cyan-400 text-lg font-semibold">
              Skills Found
            </h3>
            <p className="text-white mt-4">
              Python • React • SQL • ML
            </p>
          </div>

        </div>

      </motion.div>

    </section>
  );
}

export default DashboardPreview;
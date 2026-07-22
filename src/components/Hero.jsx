import { motion } from "framer-motion";

function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white">

     <div className="text-center max-w-5xl mx-auto px-6">

        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="glass-text text-6xl md:text-7xl font-extrabold"
        >
          AI-Powered
          <span className="text-cyan-400">
            {" "}Job Recommendation
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: .5 }}
          className="mt-8 text-xl text-gray-300 max-w-3xl mx-auto"
        >
          Upload your resume.
          Our AI analyzes your skills,
          classifies your profile,
          and recommends the best matching jobs instantly.
        </motion.p>

        <div className="mt-10 space-x-6">

          <button className="bg-cyan-500 hover:bg-cyan-600 px-8 py-4 rounded-xl font-semibold">
            Get Started
          </button>
          <button className="border border-cyan-500 hover:bg-cyan-500/20 hover:scale-105 transition-all duration-300 px-8 py-4 rounded-xl">
           Learn More
          </button>

        </div>

      </div>

    </section>
  );
}

export default Hero;
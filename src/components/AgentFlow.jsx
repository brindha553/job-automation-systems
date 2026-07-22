import { motion } from "framer-motion";

function AgentFlow() {
  const agents = [
    {
      title: "Job Scraper",
      icon: "🌐",
      description: "Collects fresher jobs from multiple websites."
    },
    {
      title: "Job Classifier",
      icon: "🧠",
      description: "Categorizes jobs into Full Stack, AI, DevOps, Cyber Security and more."
    },
    {
      title: "Resume Analyzer",
      icon: "📄",
      description: "Analyzes resumes and predicts the student's domain."
    },
    {
      title: "Recommendation AI",
      icon: "🎯",
      description: "Matches resumes with jobs and ranks the best opportunities."
    }
  ];

  return (
    <section className="bg-slate-900 py-24 px-6">

      <h2 className="text-5xl font-bold text-center text-white mb-16">
        Multi-Agent AI Workflow
      </h2>

      <div className="max-w-7xl mx-auto grid md:grid-cols-2 lg:grid-cols-4 gap-8">

        {agents.map((agent, index) => (

          <motion.div
            key={index}
            whileHover={{ scale: 1.05 }}
            className="bg-slate-800 rounded-2xl p-8 border border-slate-700 hover:border-cyan-400 transition"
          >

            <div className="text-6xl mb-5">
              {agent.icon}
            </div>

            <h3 className="text-2xl font-bold text-white">
              {agent.title}
            </h3>

            <p className="text-gray-400 mt-4">
              {agent.description}
            </p>

          </motion.div>

        ))}

      </div>

    </section>
  );
}

export default AgentFlow;
import { motion } from "framer-motion";

function Testimonials() {
  const testimonials = [
    {
      name: "Rahul Kumar",
      role: "Full Stack Student",
      review: "The AI matched me with jobs that perfectly suited my skills."
    },
    {
      name: "Priya Sharma",
      role: "ML Student",
      review: "Resume analysis was incredibly accurate and easy to use."
    },
    {
      name: "Arun S",
      role: "DevOps Student",
      review: "A modern platform that saves hours of job searching."
    }
  ];

  return (
    <section className="bg-slate-900 py-24 px-8">
      <h2 className="text-5xl font-bold text-center text-white mb-16">
        What Students Say
      </h2>

      <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
        {testimonials.map((item, index) => (
          <motion.div
            key={index}
            whileHover={{ y: -10 }}
            className="bg-slate-800 p-8 rounded-2xl border border-slate-700 hover:border-cyan-400 transition"
          >
            <p className="text-gray-300 italic">
              "{item.review}"
            </p>

            <h3 className="text-white text-xl font-bold mt-6">
              {item.name}
            </h3>

            <p className="text-cyan-400">
              {item.role}
            </p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default Testimonials;
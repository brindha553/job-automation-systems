import FeatureCard from "./FeatureCard";

function Features() {
  const features = [
    {
      icon: "🤖",
      title: "AI Agents",
      description: "Multiple intelligent agents work together to collect, classify, and recommend jobs."
    },
    {
      icon: "📄",
      title: "Resume Analysis",
      description: "Upload your resume and automatically identify your skills and domain."
    },
    {
      icon: "💼",
      title: "Job Matching",
      description: "Find fresher jobs that closely match your profile using AI."
    },
    {
      icon: "📊",
      title: "Smart Dashboard",
      description: "Track applications, recommendations, and profile insights in one place."
    }
  ];

  return (
    <section className="bg-slate-950 py-24 px-8">

      <h2 className="text-center text-5xl font-bold text-white mb-16">
        Platform Features
      </h2>

      <div className="max-w-7xl mx-auto grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>

    </section>
  );
}

export default Features;
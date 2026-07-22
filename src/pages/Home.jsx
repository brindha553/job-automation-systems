import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import AgentFlow from "../components/AgentFlow";
import Stats from "../components/Stats";
import Testimonials from "../components/Testimonials";
import Footer from "../components/Footer";

function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navigation */}
      <Navbar />

      {/* Hero Section */}
      <section id="home">
        <Hero />
      </section>

      {/* Features */}
      <section id="features" className="py-12">
        <Features />
      </section>

      {/* AI Agent Workflow */}
      <section id="workflow" className="py-12">
        <AgentFlow />
      </section>

      {/* Statistics */}
      <section id="stats" className="py-12">
        <Stats />
      </section>

      {/* Testimonials */}
      <section id="about" className="py-12">
        <Testimonials />
      </section>

      {/* Footer */}
      <Footer />

    </div>
  );
}

export default Home;
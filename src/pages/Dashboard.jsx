import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Stats from "../components/Stats";
import UploadResumeCard from "../components/UploadResumeCard";
import RecentJobs from "../components/RecentJobs";
import ResumeInsights from "../components/ResumeInsights";
import AIAnalysis from "../components/AIAnalysis";
import RecommendedJobs from "../components/RecommendedJobs";

function Dashboard() {
  return (
    <div className="flex min-h-screen bg-slate-950">

      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8">

        {/* Topbar */}
        <Topbar />

        {/* Statistics */}
        <section className="mt-8">
          <Stats />
        </section>

        {/* Upload Resume */}
        <section id="upload" className="mt-8">
          <UploadResumeCard />
        </section>

        {/* Resume Insights & Latest Jobs */}
        <section className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-8">

          <ResumeInsights />

          <RecentJobs />

        </section>

        {/* AI Analysis */}
        <section id="analysis" className="mt-8">
          <AIAnalysis />
        </section>

        {/* AI Recommended Jobs */}
        <section id="recommended-jobs" className="mt-8">
          <RecommendedJobs />
        </section>

      </main>

    </div>
  );
}

export default Dashboard;
import { FaBell, FaSearch, FaUserCircle } from "react-icons/fa";

function Topbar() {
  return (
    <header className="flex items-center justify-between bg-slate-900 border border-slate-800 rounded-xl px-6 py-4 shadow-lg">

      {/* Left */}
      <div>
        <h1 className="text-3xl font-bold text-white">
          Welcome Back 👋
        </h1>

        <p className="text-gray-400 mt-1">
          AI Resume & Job Recommendation Dashboard
        </p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-5">

        {/* Search */}
        <div className="flex items-center bg-slate-800 px-4 py-2 rounded-lg border border-slate-700">

          <FaSearch className="text-gray-400" />

          <input
            type="text"
            placeholder="Search jobs..."
            className="bg-transparent outline-none text-white ml-3 w-52 placeholder:text-gray-500"
          />

        </div>

        {/* Notification */}
        <button className="relative text-white text-xl hover:text-cyan-400 transition">

          <FaBell />

          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] rounded-full px-1">
            3
          </span>

        </button>

        {/* User */}
        <div className="flex items-center gap-3">

          <FaUserCircle className="text-4xl text-cyan-400" />

          <div>
            <h3 className="text-white font-semibold">
              Abdul
            </h3>

            <p className="text-gray-400 text-sm">
              Student • AI Enthusiast
            </p>
          </div>

        </div>

      </div>

    </header>
  );
}

export default Topbar;
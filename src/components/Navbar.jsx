import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full bg-slate-900/80 backdrop-blur-md shadow-lg z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 py-4">

        {/* Logo */}
        <Link
          to="/"
          className="text-2xl font-bold text-cyan-400 hover:text-cyan-300 transition"
        >
          AI Job Finder
        </Link>

        {/* Navigation Links */}
        <div className="flex items-center gap-8 text-white">

          <Link
            to="/"
            className="hover:text-cyan-400 transition"
          >
            Home
          </Link>

          <a
            href="#features"
            className="hover:text-cyan-400 transition"
          >
            Features
          </a>

          <a
            href="#about"
            className="hover:text-cyan-400 transition"
          >
            About
          </a>

        </div>

        {/* Buttons */}
        <div className="flex items-center gap-4">

         <Link
            to="/login"
            className="px-5 py-2 text-white border border-cyan-400 rounded-lg hover:bg-cyan-400 hover:text-slate-900 transition"
            onClick={() => console.log("Login clicked")}
         >
            Login
         </Link>
        

          <Link
            to="/signup"
            className="px-5 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 transition"
          >
            Sign Up
          </Link>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;
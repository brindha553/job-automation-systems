import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaUser,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";

function Sidebar() {
  const menuClass = ({ isActive }) =>
    `flex items-center gap-3 p-3 rounded-lg transition ${
      isActive
        ? "bg-cyan-500 text-white"
        : "text-gray-300 hover:bg-cyan-500 hover:text-white"
    }`;

  return (
    <aside className="w-72 min-h-screen bg-slate-900 border-r border-slate-800 flex flex-col">

      {/* Logo */}
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-cyan-400">
          AI Job Finder
        </h1>

        <p className="text-gray-400 text-sm mt-1">
          Resume Intelligence System
        </p>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2">

        <NavLink to="/dashboard" className={menuClass}>
          <FaHome />
          Dashboard
        </NavLink>

        <NavLink to="/profile" className={menuClass}>
          <FaUser />
          Profile
        </NavLink>

        <NavLink to="/settings" className={menuClass}>
          <FaCog />
          Settings
        </NavLink>

      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-slate-800">
        <NavLink
          to="/"
          className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg transition"
        >
          <FaSignOutAlt />
          Logout
        </NavLink>
      </div>

    </aside>
  );
}

export default Sidebar;
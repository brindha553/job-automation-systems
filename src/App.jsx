import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";

function App() {
  return (
    <Routes>

      {/* Public Routes */}

      <Route path="/" element={<Home />} />

      <Route path="/login" element={<Login />} />

      <Route path="/signup" element={<Signup />} />

      {/* Protected Pages (Authentication can be added later) */}

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/profile" element={<Profile />} />

      {/* 404 Page */}

      <Route
        path="*"
        element={
          <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white text-3xl font-bold">
            404 | Page Not Found
          </div>
        }
      />

    </Routes>
  );
}

export default App;
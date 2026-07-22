import { motion } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import {
  FaGoogle,
  FaGithub,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";
import { useState } from "react";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");

    if (!email.trim() || !password.trim()) {
      setError("Please enter both email and password.");
      return;
    }

    try {
      setLoading(true);

      // TODO:
      // Replace this with your backend login API
      // Example:
      // await loginUser({ email, password });

      navigate("/dashboard");
    } catch (err) {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-3xl p-8 shadow-2xl"
      >

        <h1 className="text-4xl font-bold text-white text-center">
          Welcome Back 👋
        </h1>

        <p className="text-gray-400 text-center mt-2">
          Sign in to your AI Job Finder account
        </p>

        <form
          onSubmit={handleLogin}
          className="mt-8 space-y-5"
        >

          {/* Email */}

          <div>

            <label className="text-gray-300">
              Email
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mt-2 p-3 rounded-xl bg-slate-800 text-white border border-slate-700 outline-none focus:border-cyan-400"
            />

          </div>

          {/* Password */}

          <div>

            <label className="text-gray-300">
              Password
            </label>

            <div className="relative mt-2">

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 rounded-xl bg-slate-800 text-white border border-slate-700 outline-none focus:border-cyan-400"
              />

              <button
                type="button"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
                className="absolute right-4 top-4 text-gray-400 hover:text-cyan-400"
              >
                {showPassword ? (
                  <FaEyeSlash />
                ) : (
                  <FaEye />
                )}
              </button>

            </div>

          </div>

          {/* Error */}

          {error && (
            <div className="bg-red-500/20 border border-red-500 text-red-300 rounded-lg p-3 text-sm">
              {error}
            </div>
          )}

          {/* Remember */}

          <div className="flex justify-between text-sm text-gray-400">

            <label>

              <input
                type="checkbox"
                className="mr-2"
              />

              Remember me

            </label>

            <button
              type="button"
              className="hover:text-cyan-400"
            >
              Forgot Password?
            </button>

          </div>

          {/* Login */}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 text-black font-semibold py-3 rounded-xl transition"
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          <div className="text-center text-gray-500">
            OR
          </div>

          {/* Google */}

          <button
            type="button"
            className="w-full border border-slate-700 py-3 rounded-xl text-white flex items-center justify-center gap-3 hover:bg-slate-800"
          >
            <FaGoogle />
            Continue with Google
          </button>

          {/* GitHub */}

          <button
            type="button"
            className="w-full border border-slate-700 py-3 rounded-xl text-white flex items-center justify-center gap-3 hover:bg-slate-800"
          >
            <FaGithub />
            Continue with GitHub
          </button>

          <p className="text-center text-gray-400">

            Don't have an account?{" "}

            <Link
              to="/signup"
              className="text-cyan-400 hover:underline"
            >
              Sign Up
            </Link>

          </p>

        </form>

      </motion.div>

    </div>
  );
}

export default Login;
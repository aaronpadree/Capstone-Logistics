import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import backgroundImage from "../assets/fdg-background.jpg";
import logo from "../assets/logo.png";
import { supabase } from "../config/supabaseClient";
import toast from "react-hot-toast";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Check if user is already logged in
  useEffect(() => {
    const session = localStorage.getItem("session");
    if (session) {
      navigate("/dashboard", { replace: true });
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;

      // Get user profile
      const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', data.user.id)
        .single();

      if (profileError) throw profileError;

      // Store the session and profile
      localStorage.setItem("session", JSON.stringify(data.session));
      localStorage.setItem("profile", JSON.stringify(profile));
      
      toast.success("Login successful!");
      
      // Use replace: true to prevent going back to login page
      navigate("/dashboard", { replace: true });
    } catch (error) {
      toast.error(error.message || "Failed to login");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative">
      {/* Full-screen background image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ 
          backgroundImage: `url(${backgroundImage})`,
          filter: 'brightness(0.7)'
        }}
      />
      
      {/* Content overlay */}
      <div className="relative z-10 flex min-h-screen items-center justify-center p-8">
        <div className="bg-white/90 p-8 rounded-lg shadow-xl w-full max-w-md backdrop-blur-sm">
          <div className="text-center mb-6">
            <img src={logo} alt="School Logo" className="mx-auto w-20" />
            <h2 className="text-xl font-bold mt-2">Flor de Grace School, Inc</h2>
            <p className="text-gray-600">INVENTORY MANAGEMENT SYSTEM</p>
          </div>

          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold">Email</label>
              <input
                type="email"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="Enter Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 font-semibold">Password</label>
              <input
                type="password"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="Enter Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-500 text-white p-3 rounded-lg hover:bg-green-600 transition"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="text-center mt-4 space-y-2">
            <Link to="/forgot-password" className="text-blue-500 hover:underline block">
              Forgot Password?
            </Link>
            <p className="text-gray-600">
              Don't have an account?{" "}
              <Link to="/signup" className="text-blue-500 hover:underline">
                Sign Up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
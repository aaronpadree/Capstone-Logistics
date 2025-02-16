import React, { useState } from "react";
import backgroundImage from "../assets/fdg-background.jpg";
import logo from "../assets/logo.png";
import axios from "axios"; // Import axios for making HTTP requests

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/login", {
        email: email,
        password: password,
      });

      // Store user information in localStorage
      localStorage.setItem("user", JSON.stringify(response.data.user));

      // Redirect to dashboard
      window.location.href = "/dashboard";
    } catch (err) {
      setError("Invalid email or password");
    }
  };

  return (
    <div className="flex h-screen">
      {/* Left side - Background Image */}
      <div
        className="w-3/4 bg-cover bg-center"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>
      
      {/* Right side - Login Form */}
      <div className="w-1/4 flex items-center justify-center bg-gray-100 p-8">
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <div className="text-center mb-6">
            <img src={logo} alt="School Logo" className="mx-auto w-20" />
            <h2 className="text-xl font-bold mt-2">Flor de Grace School, Inc</h2>
            <p className="text-gray-600">INVENTORY MANAGEMENT SYSTEM</p>
          </div>

          <form onSubmit={handleLogin}>
            {error && <p className="text-red-500">{error}</p>}
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold">Enter Email</label>
              <input
                type="email"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="Enter Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold">Enter Password</label>
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
            >
              Login
            </button>
          </form>

          <div className="text-center mt-4">
            <a href="/forgot-password" className="text-blue-500 hover:underline">
              Forgot Password?
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
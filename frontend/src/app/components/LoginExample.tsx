// frontend/components/LoginExample.js

"use client";
import { useState } from "react";

export default function LoginExample() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [result, setResult] = useState(null);
    const [error, setError] = useState<string | null>(null);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        setResult(null);

        try {
            // Simple fetch to the login endpoint
            const response = await fetch("http://localhost:8000/api/token/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Login failed");
            }

            // Display the successful result
            setResult(data);

            // Store token in localStorage if needed
            localStorage.setItem("token", data.access);
        } catch (err) {
            setError((err as Error).message);
        }
    };

    return (
        <div className="p-4">
            <h2 className="text-xl mb-4">Simple Login Example</h2>

            <form onSubmit={handleLogin} className="mb-4">
                <div className="mb-2">
                    <label className="block mb-1">Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="border p-2 w-full"
                    />
                </div>

                <div className="mb-2">
                    <label className="block mb-1">Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="border p-2 w-full"
                    />
                </div>

                <button
                    type="submit"
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Login
                </button>
            </form>

            {error && (
                <div className="bg-red-100 p-2 mb-4 rounded">
                    <p className="text-red-700">{error}</p>
                </div>
            )}

            {result && (
                <div className="bg-green-100 p-2 rounded">
                    <h3 className="font-bold mb-2">Login Successful!</h3>
                    <p>Access Token: {result.access.substring(0, 15)}...</p>
                    <p>Name: {result.name}</p>
                    <p>Email: {result.email}</p>
                </div>
            )}
        </div>
    );
}

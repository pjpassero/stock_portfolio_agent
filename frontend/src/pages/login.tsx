import { useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { supabase } from "../services/supabase";




export default function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function ProccessLogin(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });

        if (error) {
            if (error.status === 400) {
                setError("User not found!")
            } else {
                console.error("Login failed:", error.message);
                setError("Login failed:" + error.message)

            }
            return;
        }




        console.log("User:", data.user);
        console.log("Session:", data.session);

        navigate("/");
    }
    return (
        <div className="container-fluid min-vh-100 d-flex justify-content-center align-items-center">
            <div className="row justify-content-center w-100">

                <div className="col-12 col-md-6 text-center">
                    <div className="card">
                        <div className="card-body">
                            <div className="card-title mb-3">
                                <h2>Login to FinLab</h2>
                            </div>

                            <div className="w-75 mx-auto">
                                <form onSubmit={ProccessLogin}>
                                    <div className="mb-3">
                                        <input
                                            className="form-control"
                                            type="text"
                                            placeholder="Email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <input
                                            className="form-control"
                                            type="password"
                                            placeholder="Password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                        />
                                    </div>
                                    {error && (
                                        <div className="alert alert-danger p-2">
                                            {error}
                                        </div>
                                    )}
                                    <div className="mb-3">
                                        <button
                                            type="submit"
                                            className="btn btn-lg btn-dark w-100"
                                        >
                                            Login
                                        </button>
                                    </div>

                                    <div className="mb-3">
                                        <a href="/register">
                                            Don't have an account? Register Here for Free!
                                        </a>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}
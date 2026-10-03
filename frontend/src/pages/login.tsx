import { useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { supabase } from "../services/supabase";




export default function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");


    async function ProccessLogin(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });

        if (error) {
            if (error.status === 400) {
                alert("Error - User not found!");
            } else {
                console.error("Login failed:", error.message);

            }
            return;
        }




        console.log("User:", data.user);
        console.log("Session:", data.session);

        navigate("/");
    }
    return (
        <div className="container-fluid">
            <div className="row justify-content-center">
                <div className="col-md-10 text-center">
                    <div className="form-group w-50">
                        <form onSubmit={ProccessLogin}>
                            <div className="form-control">
                                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <button
                                    type="submit"
                                    className="btn btn-dark"
                                >
                                    Login
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}
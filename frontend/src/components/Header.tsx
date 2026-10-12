import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import type { User } from "@supabase/supabase-js";

export default function Header() {
    const navigate = useNavigate();
    const [user, setUser] = useState<User | null>(null);
    const [portfolio_id, setPortfolioId] = useState("");
    useEffect(() => {

        const check_session = async () => {
            const { data: { session } } = await supabase.auth.getSession();

            if (session) {
                setUser(session.user);
                const { data, error } = await supabase.from("user")
                    .select("portfolio_id")
                    .eq("user_uuid", session.user.id)
                    .single();

                if (error) {
                    console.log("Error in database retrieval:" + error);
                } else {
                    setPortfolioId(data.portfolio_id);
                    console.log("Portfolio ID:", data.portfolio_id);
                }

            } else {
                setUser(null);
            }

        };
        check_session();

        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            setUser(session?.user ?? null);
        })

        return () => {
            subscription.unsubscribe();
        };
    }, []);


    return (
        <nav className="navbar mb-5">
            <div className="container-fluid px-0">
                <span
                    className="navbar-brand fw-bold fs-3"
                    style={{ cursor: "pointer" }}
                    onClick={() => navigate("/")}
                >
                    FinLab
                </span>

                <div className="d-flex gap-2 align-items-center">
                    {user ? (
                        <>
                            <span className="fw-semibold">
                                <a href={"results/" + portfolio_id}>{user.user_metadata.firstname ?? user.email}</a>
                            </span>

                            <button
                                className="btn btn-outline-danger"
                                onClick={() => supabase.auth.signOut()}
                            >
                                Log Out
                            </button>
                        </>
                    ) : (
                        <>
                            <button
                                className="btn btn-outline-primary"
                                onClick={() => navigate("/login")}
                            >
                                Log In
                            </button>

                            <button
                                className="btn btn-primary"
                                onClick={() => navigate("/register")}
                            >
                                Register
                            </button>
                        </>
                    )}
                </div>
            </div>
        </nav>

    );
};
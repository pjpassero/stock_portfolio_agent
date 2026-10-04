import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";
import type { User } from "@supabase/supabase-js";

export default function Home() {
    const navigate = useNavigate();
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {

        const check_session = async () => {
            const { data: { session } } = await supabase.auth.getSession();

            if (session) {
                setUser(session.user);
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
        <div className="container-fluid">
            <div className="container py-4">

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
                                        {user.user_metadata.firstname ?? user.email}
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

                <main>
                    <section className="text-center py-5 mb-5">
                        <div
                            className="mx-auto"
                            style={{ maxWidth: "750px" }}
                        >
                            <h1 className="display-4 fw-bold mb-3">
                                Meet Fin.
                            </h1>

                            <p className="lead text-muted mb-4">
                                A different way to look at your portfolio.
                                Add your investments and Fin will break down
                                your risk, diversification, and what's actually
                                going on underneath the surface.
                            </p>

                            <div className="d-flex justify-content-center gap-3 flex-wrap">
                                <button
                                    className="btn btn-primary btn-lg px-4"
                                    onClick={() => navigate("/enter_portfolio")}
                                >
                                    Analyze a Portfolio
                                </button>

                                <button
                                    className="btn btn-outline-primary btn-lg px-4"
                                    onClick={() => navigate("/register")}
                                >
                                    Create an Account
                                </button>
                            </div>
                        </div>
                    </section>

                    <section className="row justify-content-center mb-5">
                        <div className="col-lg-10">

                            <div className="card shadow-sm border-0 rounded-4">
                                <div className="card-body p-4 p-md-5">

                                    <div className="row g-5 align-items-center">

                                        <div className="col-md-6">
                                            <h2 className="fw-bold mb-3">
                                                Start with your portfolio.
                                            </h2>

                                            <p className="text-muted">
                                                Enter your positions manually or
                                                upload a portfolio file.  FinLab
                                                calculates the numbers behind your
                                                investments and looks at how they
                                                work together.
                                            </p>

                                            <p className="text-muted mb-0">
                                                You'll see things like portfolio
                                                volatility, concentration, sector
                                                exposure, correlations, beta, and
                                                risk.
                                            </p>
                                        </div>

                                        <div className="col-md-6">
                                            <div className="border rounded-4 p-4">
                                                <p className="text-muted small mb-3">
                                                    Example Portfolio
                                                </p>

                                                <div className="d-flex justify-content-between border-bottom py-2">
                                                    <span className="fw-semibold">
                                                        MU
                                                    </span>
                                                    <span className="text-muted">
                                                        15 shares
                                                    </span>
                                                </div>

                                                <div className="d-flex justify-content-between border-bottom py-2">
                                                    <span className="fw-semibold">
                                                        VOO
                                                    </span>
                                                    <span className="text-muted">
                                                        12 shares
                                                    </span>
                                                </div>

                                                <div className="d-flex justify-content-between py-2">
                                                    <span className="fw-semibold">
                                                        CVX
                                                    </span>
                                                    <span className="text-muted">
                                                        8 shares
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                    </div>

                                </div>
                            </div>

                        </div>
                    </section>

                    <section className="row justify-content-center mb-5">
                        <div className="col-lg-10">

                            <div className="text-center mb-4">
                                <h2 className="fw-bold">
                                    Then ask Fin.
                                </h2>

                                <p className="text-muted">
                                    Your portfolio doesn't have to just be a page
                                    full of numbers.
                                </p>
                            </div>

                            <div className="card shadow-sm border-0 rounded-4">
                                <div className="card-body p-4 p-md-5">

                                    <div className="mb-4">
                                        <div className="border rounded-4 p-3">
                                            <span>
                                                Why is my portfolio considered risky?
                                            </span>
                                        </div>
                                    </div>

                                    <div className="ms-md-5">
                                        <div className="bg-light rounded-4 p-4">
                                            <span className="fw-semibold">
                                                Fin
                                            </span>

                                            <p className="text-muted mt-2 mb-0">
                                                A large portion of your portfolio
                                                is concentrated in technology stocks.
                                                Those positions are also fairly
                                                correlated, so they may move together
                                                during market swings.
                                            </p>
                                        </div>
                                    </div>

                                </div>
                            </div>

                        </div>
                    </section>

                    <section className="text-center py-5">
                        <h2 className="fw-bold mb-3">
                            See what your portfolio is really doing.
                        </h2>

                        <button
                            className="btn btn-primary btn-lg px-5"
                            onClick={() => navigate("/demo")}
                        >
                            Try  FinLab
                        </button>
                    </section>
                </main>

                <footer className="bg-white border-top text-center py-4 mt-5">
                    <div className="container">
                        <p className="mb-0">
                            © {new Date().getFullYear()} FinLab Portfolio analytics provided for educational purposes only.
                            FinLab is not a financial advisory tool, and we are not responsible for investment
                            decisions made using this platform. Please consult a financial professional before
                            making investment decisons. AI-generated content may contain inaccuracies.
                        </p>
                    </div>
                </footer>

            </div>
        </div>
    );
}
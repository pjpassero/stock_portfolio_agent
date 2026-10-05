import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { supabase } from "../services/supabase";



export default function Register() {

    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstname, setFirstName] = useState("");
    const [lastname, setLastName] = useState("");
    const [form_error, setError] = useState("");

    async function ProcessRegistration(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        if (!email || !password || !firstname || !lastname) {
            setError("Please make sure all fields are complete!");
        }


        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password
        });


        if (error) {
            console.error("Registration failed");
            console.error("Status:", error.status);
            console.error("Code:", error.code);
            console.error("Message:", error.message);

            setError(error.message);
            return;
        }


        if (!data.user) {
            setError("Unable to create user!");
            return;
        }
        console.log("User created: ", data.user)
        console.log(data);
        const { error: userError } = await supabase
            .from("user")
            .insert({
                user_uuid: data.user.id,
                first_name: firstname,
                last_name: lastname,
                email: email
            });

        if (userError) {
            console.error("User table insert failed:", userError);
            return;
        }

        console.log("Fintel user created");

        navigate("/");

    }



    return (
        <div className="container-fluid min-vh-100 d-flex justify-content-center align-items-center">
            <div className="row justify-content-center w-100">

                <div className="col-12 col-md-6 text-center">
                    <div className="card">
                        <div className="card-body">
                            <div className="card-title mb-3">
                                <h2>Register for FinLab</h2>
                            </div>

                            <div className="w-75 mx-auto">
                                <form onSubmit={ProcessRegistration}>

                                    <div className="mb-3">
                                        <input
                                            className="form-control"
                                            type="email"
                                            placeholder="Email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <input
                                            className="form-control"
                                            type="text"
                                            placeholder="First Name"
                                            value={firstname}
                                            onChange={(e) => setFirstName(e.target.value)}
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <input
                                            className="form-control"
                                            type="text"
                                            placeholder="Last Name"
                                            value={lastname}
                                            onChange={(e) => setLastName(e.target.value)}
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
                                    {form_error && (
                                        <div className="alert alert-danger p-2" role="alert">
                                            {form_error}
                                        </div>
                                    )}
                                    <div className="mb-3">
                                        <button
                                            type="submit"
                                            className="btn btn-lg btn-dark w-100"
                                        >
                                            Register
                                        </button>
                                    </div>

                                    <div className="mb-3">
                                        <a href="/login">
                                            Have an Account? Login Here
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
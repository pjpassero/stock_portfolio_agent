import { useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { supabase } from "../services/supabase";



export default function Register() {

    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstname, setFirstName] = useState("");
    const [lastname, setLastName] = useState("");
    const [registerError, setRegisterError] = useState("");

    async function ProcessRegistration(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();

        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password
        });


        if (error) {
            console.error("Registration failed");
            console.error("Status:", error.status);
            console.error("Code:", error.code);
            console.error("Message:", error.message);

            setRegisterError(error.message);
            return;
        }


        if (!data.user) {
            setRegisterError("Unable to create user!");
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
            setRegisterError("Account created, but profile creation failed.");
            return;
        }

        console.log("Fintel user created");

        navigate("/");

    }



    return (
        <div className="container-fluid">
            <div className="row justify-content-center">
                <div className="col-md-10 text-center">
                    <div className="form-group w-50">
                        <form onSubmit={ProcessRegistration}>
                            <div className="form-control">
                                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <input type="text" placeholder="Firstname" value={firstname} onChange={(e) => setFirstName(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <input type="text" placeholder="Lastname" value={lastname} onChange={(e) => setLastName(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>
                            <div className="form-control">
                                <button
                                    type="submit"
                                    className="btn btn-dark"
                                >
                                    Register
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )




}
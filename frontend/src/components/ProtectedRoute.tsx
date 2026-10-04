import { Navigate, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import { supabase } from "../services/supabase";


export default function ProtectedRoute() {
    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);


    useEffect(() => {
        async function check_authentication() {
            const { data: { session } } = await supabase.auth.getSession();

            if (session) {
                setAuthenticated(true);
            } else {
                setAuthenticated(false);
            }
            setLoading(false);
        }
        check_authentication();
    }, []);

    if (loading) {
        return <div>Loading......</div>
    }

    if (!authenticated) {
        return <Navigate to="/register" replace />
    }


    return <Outlet />
}
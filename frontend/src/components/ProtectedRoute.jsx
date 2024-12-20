import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants"
import { Navigate } from "react-router-dom"
import { useState, useEffect } from "react"
import jwtDecode from "jwt-decode"
import api from "../api"


function ProtectedRoute({ children }){
    const [isAuthorized, setIsAuthorized] = useState(null);

    // Check if the user is authorized when the component mounts
    useEffect( () => {
        auth().catch(() => setIsAuthorized(false))
    }, [] )


    // Check if the user is authorized
    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);

        if (!token) {
            setIsAuthorized(false)
            return
        }

        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now + 60 ) {
            await refreshToken()
        } 
        else {
            setIsAuthorized(true)
        }
    };


    // Refresh the access token
    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        
        // If there is no refresh token, the user is not authorized
        if (!refreshToken) {
            setIsAuthorized(false)
            return
        }

        try {
            const res = await api.post("/api/token/refresh/", { refresh : refreshToken });
            
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setIsAuthorized(true)
            }

        } 
        catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    };


    // If the user is not authorized, redirect to the login page
    if  (isAuthorized === null) {
        return <div>Checking authentication...</div>
    }
    return isAuthorized ? children : <Navigate to="/login"/>; 
}

// Export the ProtectedRoute component
export default ProtectedRoute;
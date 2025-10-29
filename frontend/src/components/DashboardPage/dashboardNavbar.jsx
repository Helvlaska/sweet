import { Link } from "react-router-dom";
//import { useContext } from "react";
import { useAuth } from "../../context/AuthContext";
import profilePicture from "../../assets/images/02-illustration-ferme.png"

function NavBar() {
    const { user, loading } = useAuth();
    if (loading) {
        return <nav>Chargement...</nav>;
    }

    return (
        <nav>
            <Link to="/profile" className="profile-avatar">
                <img src={user?.profile_picture || profilePicture} alt="Profil" />
            </Link>
            <Link to="/dashboard">dashboard</Link>
            <Link to="/calendar">calendar</Link>
            <Link to="/professionals">professionals</Link>
            <Link to="/forum">forum</Link>
        </nav>
    )
}

export default NavBar

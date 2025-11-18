import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

// import des icones
import DashboardIcon from "../../assets/dashboard/navbar/NavBarIconDashboard.svg";
import CalendarIcon from "../../assets/dashboard/navbar/NavBarIconCalendar.svg";
import ProfessionalsIcon from "../../assets/dashboard/navbar/NavBarIconProMedical.svg";
import ForumIcon from "../../assets/dashboard/navbar/NavBarIconTchat.svg";
import LogoutIcon from "../../assets/dashboard/navbar/NavBarIconLogOut.svg";

function NavBar() {
    const { user, loading, logout } = useAuth();
    if (loading) {
        return <nav>Chargement...</nav>;
    }

    const handleLogout = async () => {
        try {
            await logout();
        } catch (error) {
            console.error("Erreur lors de la déconnexion :", error);
        }
    };

    return (
        <nav className="navbar">
            <div className="navbar__links">
                <div className="navbar__actions">
                    <NavLink to="/profile" className={({ isActive }) =>
                        isActive ? "navbar__profile navbar__profile--active" : "navbar__profile"
                    }>
                        <img src={user?.profile_picture} alt="Profil" className="navbar__avatar" />
                    </NavLink>
                    <button onClick={handleLogout} className="navbar__logout">
                        <img src= {LogoutIcon} />
                    </button>
                </div>
                <NavLink
                    to="/dashboard"
                    className={({ isActive }) =>
                        isActive ? "navbar__icon navbar__icon--active" : "navbar__icon"
                    }>
                    <img src={DashboardIcon} alt="Dashboard" />
                </NavLink>
                <NavLink
                    to="/calendar"
                    className={({ isActive }) =>
                        isActive ? "navbar__icon navbar__icon--active" : "navbar__icon"
                    }>
                    <img src={CalendarIcon} alt="Calendar" />
                </NavLink>
                <NavLink
                    to="/professionals"
                    className={({ isActive }) =>
                        isActive ? "navbar__icon navbar__icon--active" : "navbar__icon"
                    }>
                    <img src={ProfessionalsIcon} alt="Professionals" />
                </NavLink>
                <NavLink
                    to="/forum"
                    className={({ isActive }) =>
                    isActive ? "navbar__icon navbar__icon--active" : "navbar__icon"
                    }>
                    <img src={ForumIcon} alt="Forum" />
                </NavLink>
            </div>
        </nav>
    );
}

export default NavBar

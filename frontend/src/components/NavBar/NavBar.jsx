import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/useAuth";

import Button from "../Button/buttons";
import DefaultPicture from "../../assets/profile/default_profile_picture.webp"
import DashboardIcon from "../Icon/Icons-custom/DashboardIcon";
import CalendarIcon from "../Icon/Icons-custom/CalendarIcon";
import ProfessionalIcon from "../Icon/Icons-custom/ProfessionalIcon";
import ForumIcon from "../Icon/Icons-custom/ForumIcon";
import LogoutIcon from "../Icon/Icons-custom/LogoutIcon";

function NavBar() {
  const {user, logout} = useAuth();

  return (
    <nav className="navbar">
      <NavLink
        to="/profile"
        className="btn-nav--round"
        aria-label="Profile"
      >
        <img
          src={user?.profile_picture || DefaultPicture}
          alt="Photo de profile"
          className="navbar__avatar"
        />
      </NavLink>

      <NavLink
        to="/dashboard"
        className="btn-nav--square"
        aria-label="Dashboard"
      >
        <DashboardIcon />
      </NavLink>

      <NavLink
        to="/calendar"
        className="btn-nav--square"
        aria-label="Calendrier"
      >
        <CalendarIcon />
      </NavLink>

      <NavLink
        to="/professionals"
        className="btn-nav--square"
        aria-label="Professionnels de santé"
      >
        <ProfessionalIcon />
      </NavLink>

      <NavLink
        to="/forum"
        className="btn-nav--square"
        aria-label="Forum"
      >
        <ForumIcon />
      </NavLink>

      <Button
        onClick={logout}
        className="btn-nav--square-logout"
      >
        <LogoutIcon />
      </Button>
    </nav>
  )
}

export default NavBar

import { NavLink, Outlet } from "react-router-dom";
import NavBar from "../../components/NavBar/NavBar";
import ProfileAvatar from "./user/profileAvatar/ProfileAvatar";


function ProfileFlow() {
  return (
    <main className="profileFlow">
      <NavBar />

      <ProfileAvatar />

      <nav className="profileFlow__btn">
        <NavLink
          to="/profile/user"
          className="btn-pill-solid--orange"
        >
          Informations personnelles
        </NavLink>

        <NavLink
          to="/profile/medication"
          className="btn-pill-solid--orange"
        >
          Médications et posologies
        </NavLink>
      </nav>

      <Outlet />
    </main>
  );
}

export default ProfileFlow;

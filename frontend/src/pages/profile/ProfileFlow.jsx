import { useProfileFlow } from "./useProfileFlow";

import ProfileUser from "./user/ProfileUser";
import ProfileMedication from "./medication/ProfileMedication";
import NavBar from "../../components/NavBar/NavBar";


function ProfileFlow() {
  const { currentPage, goToMedication, goToProfile } = useProfileFlow();

  const pages = [
    <ProfileUser goToMedication={goToMedication} />,
    <ProfileMedication goToProfile={goToProfile} />
  ];

  return (
    <main className="profileFlow">
      <NavBar />
      {pages[currentPage]}
    </main>
  );
}

export default ProfileFlow;

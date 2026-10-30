import ProfileInfo from "./profileInfo/ProfileInfo";
import ProfileUsername from "./profileUsername/ProfileUsername";
import ProfilePassword from "./profilePassword/ProfilePassword";
import ProfileEmail from "./profileEmail/ProfileEmail";

function ProfileUser() {

  return (
    <div>
        <ProfileInfo />
        <ProfileEmail />
        <ProfileUsername />
        <ProfilePassword />
    </div>
  )
}

export default ProfileUser;

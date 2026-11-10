import { useProfileAvatar } from "./useProfileAvatar";

function ProfileAvatar() {
  const {
    profilePicture,
    preview,
    errors,
    isLoading,
    successMessage,
    inputRef,
    openFilePicker,
  } = useProfileAvatar();
}

export default ProfileAvatar;

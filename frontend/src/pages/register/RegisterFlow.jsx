/**
 * SWEET — Register Flow (Structure)
 * =================================
 * Container component orchestrating the display
 * of the different steps of the registration process.
 *
 * Role:
 * -----
 * - Select and render the active step of the register flow.
 * - Pass necessary callbacks and state
 *   to child components.
 * - Delegate all business logic to the useRegisterFlow hook.
 *
 * Displayed steps:
 * ----------------
 * - RegisterIntro
 * - RegisterWelcome
 * - RegisterAuth
 * - RegisterProfile
 *
 * Behavior:
 * ---------
 * - The active step is determined by currentPage.
 * - Components are stored in a pages array
 *   and rendered dynamically.
 * - Actions (next, back, skip) are provided
 *   by the useRegisterFlow hook.
 *
 * Architecture:
 * -------------
 * - This component contains only JSX structure.
 * - Progression and business logic are centralized
 *   in useRegisterFlow.js.
 * - Each step is an independent component
 *   responsible for its own structure and local logic.
 *
 * Maintenance:
 * ------------
 * - Any modification to the step order must be
 *   synchronized with useRegisterFlow.
 * - Child components should remain decoupled
 *   and receive their actions via props.
 * - This component must not contain business logic.
 */


import React from "react";
import { useRegisterFlow } from "./useRegisterFlow";

import RegisterIntro from "./registerIntro/RegisterIntro";
import RegisterWelcome from "./registerWelcome/RegisterWelcome";
import RegisterAuth from "./registerAuth/RegisterAuth";
import RegisterProfile from "./registerProfile/RegisterProfile";

function RegisterFlow() {
  const {
    currentPage,
    errors,
    isLoading,

    goNext,
    goBack,
    skipPage,

    onAuthReady,
    onProfileReady,
  } = useRegisterFlow();

  const pages = [
    <RegisterIntro onSkip={skipPage} />,
    <RegisterWelcome onNext={goNext} />,
    <RegisterAuth onBack={goBack} onNext={onAuthReady} />,
    <RegisterProfile onBack={goBack} onNext={onProfileReady} isLoading={isLoading} errors={errors} />,
  ];

  return (
    <main className="registerFlow">
      {pages[currentPage]}
    </main>
  );
}

export default RegisterFlow;

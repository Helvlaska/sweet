/**
 * SWEET — Register Intro Step (Structure)
 * ======================================
 * Component representing the introduction step
 * of the registration process.
 *
 * Current role:
 * -------------
 * - Serve as an introductory screen before the register flow begins.
 * - Allow the user to skip directly to the next step via a "skip" action.
 *
 * Context:
 * --------
 * - This step is currently simplified.
 * - It is intended to host an animated or video presentation
 *   of the application, currently in development.
 *
 * Content:
 * --------
 * - Button allowing the user to skip the introduction.
 * - Informational message explaining the provisional state.
 * - Lightweight visual placeholder (emoji).
 *
 * Interaction:
 * ------------
 * - The "skip" action is passed through the onSkip prop.
 * - This component contains no business logic.
 *
 * Architecture:
 * -------------
 * - Flow progression is centralized in useRegisterFlow.
 * - Styles are defined in the associated SCSS file.
 * - Button and Icon components come from the SWEET Design System.
 *
 * Maintenance:
 * ------------
 * - This step is designed to evolve into a
 *   video or animated introduction.
 * - Any future logic (e.g. video playback, tracking)
 *   must remain decoupled and aligned with the global flow.
 */


import React from "react";
import Button from "../../../components/Button/buttons";
import Icon from "../../../components/Icon/Icons";

function RegisterIntro({ onSkip }) {
  return (
    <div className="registerIntro">
      <div className="registerIntro__header">
        <Button onClick={onSkip} className="btn-underline-grey">
          Passer cette étape
          <Icon
            name="chevronRight"
            strokeWidth="1.5"
            className="registerIntro__header-icon"
          />
        </Button>
      </div>

      <div className="registerIntro__text">
        <p className="registerIntro__text-title">
          On vous prépare quelque chose...
        </p>

        Cette introduction animée est en cours de montage.<br />
        Vous pouvez passer cette étape et commencer votre <br />
        inscription dès maintenant.<br />
        Promis, on arrive très vite. 😉
      </div>

      <div className="registerIntro__emoji">
        🚧
      </div>
    </div>
  )
}

export default RegisterIntro;

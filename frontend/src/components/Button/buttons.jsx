/**
 * SWEET — Unified Button Component
 * ================================
 * Generic interactive surface used across SWEET.
 *
 * The Button component is responsible for:
 *  - User interaction (click, focus, disabled)
 *  - Semantic accessibility (<button>)
 *  - Visual state handling via CSS classes
 *
 * Supported content:
 *  - Text
 *  - Icon
 *  - Icon + text
 *
 * Props:
 *  - children   : ReactNode
 *      Content of the button (text, <Icon />, or both).
 *
 *  - onClick    : function
 *      Click handler (optional).
 *
 *  - disabled   : boolean
 *      Prevents interaction when true.
 *
 *  - type       : "button" | "submit" | "reset"
 *      Native button type (default: "button").
 *
 *  - className  : string
 *      CSS classes used to apply skins, sizes and states.
 *
 * NOTE:
 *  - Button does NOT handle visual styles internally.
 *    All visual variations (skin, size, states) are
 *    handled via SCSS classes.
 *
 *  - Button does NOT manage business logic or loading states.
 *
 *  - Icon rendering and SVG behavior are delegated
 *    to the Icon component.
 */


export default function Button({
  children,
  onClick,
  disabled = false,
  className = "",
  type = "button",
}) {
  return (
    <button
      type={type}
      className={`btn ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

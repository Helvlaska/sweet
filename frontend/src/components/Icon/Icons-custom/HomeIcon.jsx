/**
 * SWEET — Custom Icon Component (Filled)
 * --------------------------------------
 * This icon uses a filled SVG path (no stroke).
 * It supports the same API conventions as Lucide when applicable.
 *
 * Props:
 *  - size (number)   → icon size in pixels (default: 24)
 *  - fill (string)   → fill color (default: "currentColor")
 *
 * Notes:
 *  - stroke and strokeWidth are intentionally omitted (not used by this SVG).
 *  - Styling (hover, color presets, disabled state…) must be applied from parent or SCSS.
 */

export default function HomeIcon({ size = 24, fill = "currentColor", ...props }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 12 11"
      xmlns="http://www.w3.org/2000/svg"
      fill={fill}
      {...props}
    >
      <path d="M10.7496 9.8243C10.7495 10.4786 10.2041 10.9999 9.54364 11H2.45635C1.79592 10.9999 1.25046 10.4786 1.25044 9.8243V5.72674L0.988841 5.98084C0.760985 6.20185 0.393389 6.20036 0.167762 5.97714C-0.0578098 5.75387 -0.0555177 5.39368 0.172298 5.17259L5.14867 0.34235L5.14943 0.341609C5.61993 -0.113763 6.38005 -0.114224 6.85056 0.34235L10.5757 3.95762C10.5777 3.95958 10.5797 3.96156 10.5817 3.96355L11.8277 5.17259C12.0555 5.39368 12.0578 5.75386 11.8322 5.97714C11.6066 6.20038 11.239 6.20186 11.0111 5.98084L10.7496 5.72674V9.8243Z"/>
    </svg>
  );
}

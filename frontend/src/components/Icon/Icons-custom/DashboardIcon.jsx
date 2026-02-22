/**
 * SWEET — Custom Icon Component
 * ------------------------------
 * This component renders the custom SVG.
 * It follows the same API conventions as Lucide icons (size, color, strokeWidth).
 *
 * Props:
 *  - size (number)        → icon size in pixels (default: 24)
 *  - color (string)       → stroke color (default: "currentColor")
 *  - strokeWidth (number) → stroke width for the SVG paths (default: 1.5)
 *
 * Notes:
 *  - This file is auto-contained: the SVG path is embedded directly.
 *  - Styling (colors, hover effects…) must be applied from the parent component.
 *  - Custom icons are stored inside: /components/Icon/icons-custom/
 */

export default function DashboardIcon({
  size = 24,
  color = "currentColor",
  strokeWidth = 1.5,
  ...props
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 25 25"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <rect
        x="0.75"
        y="0.75"
        width="23.5"
        height="23.5"
        rx="2.25"
        strokeLinejoin="round"
      />
      <path d="M13 0.5V24.5" />
      <path d="M25 11L13.0049 11" />
    </svg>
  );
}

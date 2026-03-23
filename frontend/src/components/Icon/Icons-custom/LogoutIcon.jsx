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

export default function LogoutIcon({
  size = 24,
  color = "currentColor",
  strokeWidth = 1.5,
  ...props
}) {
  return (
    <svg
      width={size}
      height={(size * 24) / 22}
      viewBox="0 0 22 24"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path d="M13.4773 8.08333V3.5C13.4773 2.77065 13.1899 2.07118 12.6785 1.55546C12.167 1.03973 11.4733 0.75 10.75 0.75H3.47727C2.75395 0.75 2.06026 1.03973 1.5488 1.55546C1.03734 2.07118 0.75 2.77065 0.75 3.5V20C0.75 20.7293 1.03734 21.4288 1.5488 21.9445C2.06026 22.4603 2.75395 22.75 3.47727 22.75H10.75C11.4733 22.75 12.167 22.4603 12.6785 21.9445C13.1899 21.4288 13.4773 20.7293 13.4773 20V15.4167M17.1136 15.4167L20.75 11.75M20.75 11.75L17.1136 8.08333M20.75 11.75H5.29545" />
    </svg>
  );
}

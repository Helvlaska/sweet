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

export default function ProfessionalsIcon({
  size = 24,
  color = "currentColor",
  strokeWidth = 1.5,
  ...props
}) {
  return (
    <svg
      width={size}
      height={(size * 26) / 28}
      viewBox="0 0 28 26"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path d="M8.75 4.75V0.75H17.75V4.75" />
      <path d="M0.75 7.98214V22.2679C0.75 23.0256 1.09241 23.7523 1.7019 24.2882C2.3114 24.824 3.13805 25.125 4 25.125H23.5C24.362 25.125 25.1886 24.824 25.7981 24.2882C26.4076 23.7523 26.75 23.0256 26.75 22.2679V7.98214C26.75 7.22438 26.4076 6.49766 25.7981 5.96184C25.1886 5.42602 24.362 5.125 23.5 5.125H4C3.13805 5.125 2.3114 5.42602 1.7019 5.96184C1.09241 6.49766 0.75 7.22438 0.75 7.98214Z" />
      <path d="M13.75 10.5625V18.9375" />
      <path d="M17.9375 14.75L9.5625 14.75" />
    </svg>
  );
}

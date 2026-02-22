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

export default function ForumIcon({
  size = 24,
  color = "currentColor",
  strokeWidth = 1.5,
  ...props
}) {
  return (
    <svg
      width={size}
      height={(size * 24) / 28}
      viewBox="0 0 28 24"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path d="M24.75 7.48585C25.9287 7.83297 26.75 8.86456 26.75 10.0489V15.2875C26.75 16.676 25.6207 17.8542 24.11 17.9679C23.6567 18.0009 23.2033 18.0315 22.75 18.0559V21.8339L18.75 18.1671C16.9447 18.1671 15.158 18.0999 13.39 17.9679C13.0051 17.9394 12.6307 17.8387 12.29 17.6721M24.75 7.48585C24.544 7.42506 24.331 7.38611 24.1153 7.36974C20.5446 7.09801 16.9554 7.09801 13.3847 7.36974C11.8767 7.48463 10.75 8.66166 10.75 10.0489V15.2875C10.75 16.3105 11.3633 17.2187 12.29 17.6721M24.75 7.48585V5.19535C24.75 3.21407 23.214 1.4968 21.07 1.24135C18.3111 0.913529 15.532 0.749405 12.75 0.750002C9.93 0.750002 7.15267 0.917451 4.43 1.24135C2.286 1.4968 0.75 3.21407 0.75 5.19535V12.8051C0.75 14.7864 2.286 16.5037 4.43 16.7591C5.19933 16.8508 5.97267 16.9302 6.75 16.9962V22.7506L12.29 17.6721" />
    </svg>
  );
}

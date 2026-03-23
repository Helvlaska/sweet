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

export default function WarningIcon({
  size = 24,
  color = "currentColor",
  strokeWidth = 1.5,
  ...props
}) {
  return (
    <svg
      width={size}
      height={(size * 43) / 48}
      viewBox="0 0 48 43"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path d="M22.0009 1.43603L0.391269 38.6908C-0.720713 40.6056 0.670322 43 2.89006 43H46.1094C48.3333 43 49.7202 40.6056 48.6082 38.6908L27.0027 1.43603C25.8908 -0.478678 23.1129 -0.478678 22.0009 1.43603Z" fill="white"/>
      <path d="M26.25 14.6364L26.0511 29.2727H23.7443L23.5455 14.6364H26.25ZM24.8977 35.1591C24.4072 35.1591 23.9863 34.9834 23.6349 34.6321C23.2836 34.2808 23.108 33.8598 23.108 33.3693C23.108 32.8788 23.2836 32.4579 23.6349 32.1065C23.9863 31.7552 24.4072 31.5795 24.8977 31.5795C25.3883 31.5795 25.8092 31.7552 26.1605 32.1065C26.5118 32.4579 26.6875 32.8788 26.6875 33.3693C26.6875 33.6941 26.6046 33.9924 26.4389 34.2642C26.2798 34.536 26.0644 34.7547 25.7926 34.9205C25.5275 35.0795 25.2292 35.1591 24.8977 35.1591Z" fill="#FF8FDC"/>
    </svg>
  );
}

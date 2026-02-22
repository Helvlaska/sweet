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

export default function CalendarIcon({ size = 24, color = "currentColor", strokeWidth = 1.5, ...props}) {
  return (
    <svg
      width={size}
      height={(size * 26) / 28}
      viewBox="0 0 28 26"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke={color}
      strokeWidth={strokeWidth}
      {...props}
    >
      <path
        d="M6.16667 0.75V3.75M21.3333 0.75V3.75M0.75 21.75V6.75C0.75 5.95435 1.09241 5.19129 1.7019 4.62868C2.3114 4.06607 3.13805 3.75 4 3.75H23.5C24.362 3.75 25.1886 4.06607 25.7981 4.62868C26.4076 5.19129 26.75 5.95435 26.75 6.75V21.75M0.75 21.75C0.75 22.5457 1.09241 23.3087 1.7019 23.8713C2.3114 24.4339 3.13805 24.75 4 24.75H23.5C24.362 24.75 25.1886 24.4339 25.7981 23.8713C26.4076 23.3087 26.75 22.5457 26.75 21.75M0.75 21.75V11.75C0.75 10.9544 1.09241 10.1913 1.7019 9.62868C2.3114 9.06607 3.13805 8.75 4 8.75H23.5C24.362 8.75 25.1886 9.06607 25.7981 9.62868C26.4076 10.1913 26.75 10.9544 26.75 11.75V21.75M13.75 13.75H13.7616V13.7607H13.75V13.75ZM13.75 16.75H13.7616V16.7607H13.75V16.75ZM13.75 19.75H13.7616V19.7607H13.75V19.75ZM10.5 16.75H10.5116V16.7607H10.5V16.75ZM10.5 19.75H10.5116V19.7607H10.5V19.75ZM7.25 16.75H7.26156V16.7607H7.25V16.75ZM7.25 19.75H7.26156V19.7607H7.25V19.75ZM17 13.75H17.0116V13.7607H17V13.75ZM17 16.75H17.0116V16.7607H17V16.75ZM17 19.75H17.0116V19.7607H17V19.75ZM20.25 13.75H20.2616V13.7607H20.25V13.75ZM20.25 16.75H20.2616V16.7607H20.25V16.75Z"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

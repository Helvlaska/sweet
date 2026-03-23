/**
 * SWEET — Custom Icon Component (Filled)
 * --------------------------------------
 * This icon uses a filled SVG path (no stroke).
 * It supports Lucide-like API (size + fill) for consistency.
 *
 * Props:
 *  - size (number) → icon size in pixels (default: 24)
 *  - fill (string) → fill color (default: "currentColor")
 *
 * Notes:
 *  - stroke and strokeWidth are intentionally omitted (not used by this SVG).
 *  - Styling (hover, color presets, disabled state…) must be applied from parent or SCSS.
 */

export default function PhoneIcon({ size = 24, fill = "currentColor", ...props}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 11 11"
      xmlns="http://www.w3.org/2000/svg"
      fill={fill}
      {...props}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M0 1.57143C0 1.15466 0.165561 0.754961 0.460261 0.460261C0.754961 0.165561 1.15466 0 1.57143 0H2.2901C2.74057 0 3.13343 0.306952 3.2429 0.74381L3.82171 3.06062C3.86862 3.24814 3.85914 3.44534 3.79448 3.6275C3.72981 3.80966 3.61283 3.96869 3.45819 4.08467L2.78091 4.59276C2.71019 4.64567 2.695 4.72319 2.71491 4.77714C3.01053 5.58111 3.47736 6.31123 4.08307 6.91693C4.68877 7.52264 5.41889 7.98947 6.22286 8.2851C6.27681 8.305 6.35381 8.28981 6.40724 8.2191L6.91533 7.54181C7.03131 7.38717 7.19034 7.27019 7.3725 7.20552C7.55466 7.14086 7.75186 7.13138 7.93938 7.17829L10.2562 7.7571C10.693 7.86657 11 8.25943 11 8.71043V9.42857C11 9.84534 10.8344 10.245 10.5397 10.5397C10.245 10.8344 9.84534 11 9.42857 11H8.25C3.6939 11 0 7.3061 0 2.75V1.57143Z"
      />
    </svg>
  );
}

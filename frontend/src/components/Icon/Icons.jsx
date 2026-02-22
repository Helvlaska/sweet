/**
 * SWEET — Unified Icon Component
 * ==============================
 * Centralizes all icon rendering for SWEET.
 *
 * Supports:
 *  - Lucide icons
 *  - Custom SVGs
 *
 * Props:
 *  - name          : string (icon identifier)
 *  - size          : number | "sm" | "md" | "lg"
 *  - color         : stroke color (CSS var or raw)
 *  - fill          : fill color (CSS var or raw)
 *  - strokeWidth   : SVG stroke width
 *  - rotate        : rotate in degrees
 *  - className     : CSS classes for skins
 *
 * NOTE:
 *  - Colors are applied to the <span> wrapper via CSS
 *    which lets SCSS Phase B handle currentColor cleanly.
 */


import {
  ChevronRight,
  ChevronLeft,
  X,
  Check,
  Eye,
  EyeOff,
  Plus,
  Trash2,
  Pencil,
  ArrowUp,
  ArrowDown,
  Upload,
  MessageCircle,
  Heart,
} from "./LucideIcons";

// Custom icons
import CalendarIcon from "./Icons-custom/CalendarIcon";
import DashboardIcon from "./Icons-custom/DashboardIcon";
import ForumIcon from "./Icons-custom/ForumIcon";
import LogoutIcon from "./Icons-custom/LogoutIcon";
import ProfessionalsIcon from "./Icons-custom/ProfessionalIcon";
import WarningIcon from "./Icons-custom/WarningIcon";
import HomeIcon from "./Icons-custom/HomeIcon";
import PhoneIcon from "./Icons-custom/PhoneIcon";
import MailIcon from "./Icons-custom/MailIcon";

// ICON REGISTRY — DO NOT rename inside components
const ICONS = {
  // Lucide
  chevronRight: ChevronRight,
  chevronLeft: ChevronLeft,
  eye: Eye,
  eyeOff: EyeOff,
  pen: Pencil,
  heart: Heart,
  comment: MessageCircle,
  plus: Plus,
  trash: Trash2,
  cross: X,
  check: Check,
  arrowUp: ArrowUp,
  arrowDown: ArrowDown,
  upload: Upload,

  // Custom
  calendar: CalendarIcon,
  dashboard: DashboardIcon,
  forum: ForumIcon,
  logout: LogoutIcon,
  professionals: ProfessionalsIcon,
  warning: WarningIcon,
  home: HomeIcon,
  phone: PhoneIcon,
  mail: MailIcon,
};

// Size presets
const SIZE_PRESETS = {
  sm: 16,
  md: 20,
  lg: 25,
};

// Color presets
const COLOR_PRESETS = {
  lightGrey: "var(--light-grey)",
  mainGrey: "var(--main-grey)",
  darkGrey: "var(--dark-grey)",

  white: "var(--white)",
  black: "var(--black)",
  red: "var(--red)",
  green: "var(--green)",

  mainBlue: "var(--main-blue)",

  mainViolet: "var(--main-violet)",
  lightViolet: "var(--light-violet)",

  mainPink: "var(--main-pink)",
  darkPink: "var(--dark-pink)",

  mainLila: "var(--main-lila)",

  darkBrown: "var(--dark-brown)"
};


export default function Icon({
  name,
  size = "md",
  color = null,
  fill = null,
  strokeWidth = 2,
  rotate = 0,
  className = "",
  ...props
}) {
  const IconComponent = ICONS[name] || WarningIcon;

  // Compute numeric size
  const resolvedSize =
    typeof size === "number" ? size : SIZE_PRESETS[size] || SIZE_PRESETS["md"];

  // Resolve stroke color
  const resolvedStroke =
    color ? COLOR_PRESETS[color] || color : "currentColor";

  // Resolve fill color
  const resolvedFill =
    fill === null ? undefined : COLOR_PRESETS[fill] || fill;

  return (
    <span
      className={`icon ${className}`}
      style={{
        display: "inline-flex",
        transform: `rotate(${rotate}deg)`,
        color: resolvedStroke,
      }}
    >
      <IconComponent
        size={resolvedSize}
        color={resolvedStroke}  // for Lucide
        fill={resolvedFill}     // for custom SVG
        strokeWidth={strokeWidth}
        aria-label={name}
        {...props}
      />
    </span>
  );
}

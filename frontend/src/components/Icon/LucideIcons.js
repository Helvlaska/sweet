/**
 * SWEET — Icon Library
 * =====================
 * This file centralizes all icon imports used across the SWEET frontend.
 *
 * Usage:
 * ------
 * Import icons directly from this file instead of "lucide-react" or local SVG paths.
 *
 * Example:
 *   import { ChevronRight, EyeOff, Heart } from "@/components/Icon/LucideIcons";
 *
 * Custom Icons:
 * -------------
 * Icons that do not exist in Lucide are stored in:
 *   /components/Icon/Icons-custom/
 *
 * Add their exports below the Lucide ones to keep everything centralized.
 *
 * Maintenance:
 * ------------
 * - When adding a new icon, always check whether Lucide already provides it.
 * - If switching to a different icon style (filled, outline, soft…),
 *   update the export here so the change is propagated throughout the app.
 * - Keep naming clear and consistent with SWEET’s design system.
 *
 * Important:
 * ----------
 * This file imports icons only.
 * The styling (colors, sizes, variants) is handled inside <Icon /> or the component using it.
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
  Mail,
  Upload,
  MessageCircle,
  Heart,
} from "lucide-react";

export {
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
  Mail,
  Upload,
  MessageCircle,
  Heart,
};

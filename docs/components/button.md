# SWEET — Button Component Documentation

This document describes the `<Button />` component used in the SWEET application.

The Button component represents **any interactive clickable surface**:
action buttons, navigation buttons, icon buttons, etc.

## 1. Purpose of the Button Component

The `<Button />` component is responsible for:

- user interaction (click, focus, disabled)
- button structure (clickable surface)
- consistent behaviors (hover, active, disabled)

It does NOT handle:

- colors directly
- icons themselves
- business logic

---

## 2. Basic Usage

```jsx
import Button from "@/components/Button/Button";

<Button className="btn-pill-outline-pink">
  Save
</Button>
```

The Button component is intentionally simple and neutral:
all styling is applied through explicit CSS classes.

---

## 3. Button with Icon

```jsx
<Button className="btn-pill-outline-pink">
  <Icon name="heart" className="icon-size--sm" />
  Add to favorites
</Button>
```

Important rule:

- Button handles the interactive surface
- Icon handles SVG visual rendering

---

## 4. Shapes and Sizes

Shapes are defined in SCSS through composed classes:

- Pill button (text / icon + text)
- Round button (icon only)
- Navbar button

Icon sizes are always handled by the Icon system,
never directly by the Button component.

---

## 5. Managed States

The Button component manages the following states:

- hover
- active (persistent)
- keyboard focus (aligned with hover)
- disabled

Example:

```jsx
<Button className="btn-pill-solid-mainKaki" disabled>
  Submit
</Button>
```

---

## 6. Best Practices

- Use only existing button classes
- Keep JSX readable and explicit
- Centralize styles in _button.scss
- Keep the Button component free of business logic

---

## 7. What Not to Do

- Add inline styles
- Create “magic” variants via props
- Handle colors directly in JSX
- Merge Button and Icon into a complex component

---

## 8. Possible Evolutions

- Add new concrete skins when needed
- Adjust visuals without impacting JSX
- Improve accessibility if required

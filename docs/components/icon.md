# SWEET — Icon Component

This document describes the `<Icon />` component used in the SWEET application.

The Icon component is responsible for **SVG icon rendering**
(Lucide icons or custom icons).

## 1. Purpose of the Icon Component

The `<Icon />` component provides:

- unified SVG rendering
- consistent size management
- usage of `currentColor`
- compatibility with Lucide and custom icons

It does NOT handle:

- user interactions
- hover / active states
- click logic

---

## 2. Basic Usage

```jsx
import Icon from "@/components/Icon/Icon";

<Icon name="heart" />
```

The component automatically resolves:

- the matching SVG
- default parameters

---

## 3. Size Management

Sizes are controlled through CSS classes:

```css
icon-size--xs
icon-size--sm
icon-size--md
icon-size--lg
icon-size--xl
icon-size--nav
```

Example:

```jsx
<Icon name="trash" className="icon-size--sm" />
```

---

## 4. Colors and currentColor

Icons rely on currentColor:
they inherit their color from their parent
(usually a Button).

```jsx
<Button className="btn-pill-outline-pink">
  <Icon name="heart" className="icon-size--sm" />
  Favorite
</Button>
```

---

## 5. SVG Variants

Some classes affect the SVG only:

```css
icon--filled
icon--outline
icon--flip-x
```

Example:

```jsx
<Icon name="heart" className="icon--filled icon-size--sm" />
```

---

## 6. Best Practices

- Always define an explicit size
- Use Icon inside a Button for actions
- Keep Icon purely visual
- Centralize rules in _icon.scss

---

## 7. What Not to Do

- Attach click handlers to Icon
- Handle interactive states in Icon
- Manually override SVG width / height
- Duplicate SVGs outside the Icon component

---

## 8. Possible Evolutions

- Add new sizes if required
- Optimize SVG assets
- Integrate Storybook in the long term

# SWEET — SelectedField Component Documentation

This document describes the `<SelectedField />` component used in the SWEET application.

The SelectedField component represents **a custom accessible select field**
used across SWEET forms.

It replaces the native `<select>` element to provide:

- full styling control
- consistent interaction behavior
- keyboard navigation support
- accessible combobox structure

## 1. Purpose of the SelectedField Component

The `<SelectedField />` component is responsible for:

- rendering a custom combobox surface
- managing open / close behavior
- handling keyboard navigation
- displaying the selected value or placeholder
- normalizing change events for form compatibility

It does NOT handle:

- form validation
- business logic
- submission handling
- color definitions

---

## 2. Basic Usage

```jsx
import SelectedField from "@/components/Form/SelectedField/SelectedField";

<SelectedField
  name="gender"
  placeholder="Select your gender"
  options={genderOptions}
  value={formData.gender}
  onChange={handleChange}
/>
```

The component behaves like a controlled form field.

---

## 3. Options Format

Options must follow this structure:

```jsx
[
  { value: "male", label: "Male" },
  { value: "female", label: "Female" }
]
```

- value → stored value
- label → displayed value

---

## 4. Accessibility

SelectedField follows ARIA combobox best practices:

- role="combobox"
- role="listbox"
- aria-expanded
- aria-selected

Keyboard navigation includes:

- ArrowDown
- ArrowUp
- Enter
- Escape
- Tab

The component is fully usable without a mouse.

---

## 5. Managed States

SelectedField manages:

- open / closed state
- active option (keyboard hover)
- selected option
- disabled state

Icon rotation is automatically handled via aria-expanded.

---

## 6. Best Practices

- Keep SelectedField controlled (value + onChange)
- Use standardized option format
- Do not inject inline styles
- Keep logic inside useSelectedField
- Do not mix validation inside the component

## 7. What Not to Do

- Do not use it for extremely large datasets
- Do not override styles inline
- Do not mix business logic into the component
- Do not replace native `<select>` everywhere without necessity

---

## 8. Possible Evolutions

- Add loading state support
- Add searchable mode
- Add grouped options
- Improve accessibility if required

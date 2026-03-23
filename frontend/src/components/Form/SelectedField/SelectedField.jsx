/**
 * SWEET — SelectedField Component
 * ================================
 * Custom accessible select field used across SWEET forms.
 *
 * SelectedField replaces the native <select> element
 * to provide full control over styling, accessibility,
 * keyboard navigation and visual behavior.
 *
 * Responsibilities:
 *  - Render an accessible combobox interface
 *  - Manage open/close interaction state
 *  - Handle keyboard navigation (arrows, enter, escape)
 *  - Display selected value or placeholder
 *  - Delegate business logic to useSelectedField hook
 *
 * Architecture:
 *  - Logic is handled inside useSelectedField
 *  - Rendering is handled in this component
 *  - Visual styling is handled via SCSS classes
 *
 * Props:
 *  - name         : string
 *      Unique field identifier (used for ARIA attributes).
 *
 *  - placeholder  : string
 *      Text displayed when no option is selected.
 *
 *  - options      : array
 *      Array of options in the format:
 *      { value: string | number, label: string }
 *
 *  - value        : string | number
 *      Currently selected value.
 *
 *  - onChange     : function
 *      Callback triggered when selection changes.
 *
 *  - disabled     : boolean
 *      Prevents interaction when true.
 *
 * Accessibility:
 *  - Uses role="combobox" and role="listbox"
 *  - Supports keyboard navigation
 *  - Uses aria-expanded and aria-selected
 *
 * NOTE:
 *  - SelectedField does NOT manage business validation.
 *  - SelectedField does NOT handle form submission.
 *  - All visual variants must be handled via SCSS.
 *  - Icon rendering is delegated to the Icon component.
 */


import React from "react";
import { useSelectedField } from "./useSelectedField";
import Icon from "../../Icon/Icons";

export default function SelectedField(props) {

  const {
    name,
    placeholder,
    options,
    value,
    onChange,
    disabled,
    className
  } = props;

  const {
    isOpen,
    activeIndex,
    selectedLabel,
    fieldRef,
    optionsRef,

    toggleField,
    selectOption,
    setActiveOption,
    handleKeyboardNavigation
  } = useSelectedField(name, options, value, onChange, disabled);

  return (
    <div className={"selectedField" + (className ? " " + className : "")} ref={fieldRef}>
      <div
        className="selectedField__control"
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-controls={name + "-listbox"}
        tabIndex={disabled ? -1 : 0}
        onClick={toggleField}
        onKeyDown={handleKeyboardNavigation}
      >
        <span
          className={
            value
              ? "selectedField__value"
              : "selectedField__placeholder"
          }
        >
          {value ? selectedLabel : placeholder}
        </span>

        <Icon
          name="arrowDown"
          strokeWidth="1.5"
          className="selectedField__icon icon-size--xs"
        />
      </div>

      {isOpen && (
        <ul
          id={name + "-listbox"}
          role="listbox"
          className="selectedField__list"
        >
          {options.map(function (option, index) {
            const isActive = index === activeIndex;
            const isSelected = option.value === value;
            return (
              <li
                key={option.value}
                role="option"
                aria-selected={isSelected}
                ref={function (element) {
                  optionsRef.current[index] = element;
                }}
                className={
                  "selectedField__option" +
                  (isActive ? " selectedField__option--active" : "") +
                  (isSelected ? " selectedField__option--selected" : "")
                }
                onMouseEnter={function () {
                  setActiveOption(index);
                }}
                onClick={function () {
                  selectOption(index);
                }}
              >
                {option.label}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

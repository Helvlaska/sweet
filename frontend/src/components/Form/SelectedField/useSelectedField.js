import { useState, useRef, useEffect } from "react";

export function useSelectedField(name, options, value, onChange, disabled) {

  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);

  const fieldRef = useRef(null);
  const optionsRef = useRef([]);


  let selectedLabel = "";

  if (value && options && options.length > 0) {

    const selectedOption = options.find(function (option) {
      return option.value === value;
    });

    if (selectedOption) {
      selectedLabel = selectedOption.label;
    }
  }


  function openField() {

    if (disabled) {
      return;
    }

    if (!options || options.length === 0) {
      return;
    }

    setIsOpen(true);
    setActiveIndex(0);
  }

  function closeField() {
    setIsOpen(false);
    setActiveIndex(0);
  }

  function toggleField() {

    if (isOpen) {
      closeField();
    } else {
      openField();
    }
  }


  function setActiveOption(index) {
    setActiveIndex(index);
  }


  function selectOption(index) {

    if (!options || options.length === 0) {
      return;
    }

    const selectedOption = options[index];

    if (selectedOption) {
      onChange({
        target: {
          name: name,
          value: selectedOption.value
        }
      });
    }

    closeField();
  }


  function handleKeyboardNavigation(event) {

    if (disabled) {
      return;
    }

    const key = event.key;

    if (!isOpen) {

      if (key === "Enter" || key === "ArrowDown" || key === "ArrowUp") {
        event.preventDefault();
        openField();
      }

      return;
    }

    if (!options || options.length === 0) {
      return;
    }

    if (key === "ArrowDown") {
      event.preventDefault();

      setActiveIndex(function (previousIndex) {
        const nextIndex = (previousIndex + 1) % options.length;
        return nextIndex;
      });
    }

    if (key === "ArrowUp") {
      event.preventDefault();

      setActiveIndex(function (previousIndex) {
        const nextIndex =
          (previousIndex - 1 + options.length) % options.length;
        return nextIndex;
      });
    }

    if (key === "Enter") {
      event.preventDefault();
      selectOption(activeIndex);
    }

    if (key === "Escape") {
      closeField();
    }

    if (key === "Tab") {
      closeField();
    }
  }


  useEffect(function () {

    function handleMouseDown(event) {

      if (!fieldRef.current) {
        return;
      }

      if (!fieldRef.current.contains(event.target)) {
        closeField();
      }
    }

    document.addEventListener("mousedown", handleMouseDown);

    return function () {
      document.removeEventListener("mousedown", handleMouseDown);
    };

  }, []);


  useEffect(function () {

    if (!isOpen) {
      return;
    }

    const currentOption = optionsRef.current[activeIndex];

    if (currentOption && currentOption.scrollIntoView) {
      currentOption.scrollIntoView({
        block: "nearest"
      });
    }

  }, [activeIndex, isOpen]);

  return {
    isOpen,
    activeIndex,
    selectedLabel,

    fieldRef,
    optionsRef,

    toggleField,
    selectOption,
    setActiveOption,
    handleKeyboardNavigation
  };
}

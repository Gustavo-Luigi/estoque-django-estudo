const labels = document.querySelectorAll("label");
const inputs = document.querySelectorAll("input");

labels.forEach((label) => {
  label.classList.add("form-label");
});

inputs.forEach((input) => {
  if (input.type == "checkbox") {
    input.classList.add("form-control-input");
  } else {
    input.classList.add("form-control");
  }
});

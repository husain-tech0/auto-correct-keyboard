const input = document.getElementById("textInput");
const output = document.getElementById("outputText");

let timeout = null;

input.addEventListener("input", function () {

  clearTimeout(timeout);

  timeout = setTimeout(() => {

    fetch("/correct", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: input.value })
    })
    .then(res => res.json())
    .then(data => {
      output.style.opacity = 0;
      setTimeout(() => {
        output.textContent = data.corrected;
        output.style.opacity = 1;
      }, 200);
    });

  }, 400); // slight delay for smooth typing

});
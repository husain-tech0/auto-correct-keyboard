document.addEventListener("DOMContentLoaded", function () {

  const wordInput = document.getElementById("wordInput");
  const correctBtn = document.getElementById("correctBtn");
  const bestCorrection = document.getElementById("bestCorrection");
  const suggestionsList = document.getElementById("suggestionsList");

  correctBtn.addEventListener("click", function () {

    const word = wordInput.value.trim();

    console.log("Button clicked, sending request...");

    fetch("/correct", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ word: word })
    })
      .then((response) => response.json())
      .then((data) => {

        console.log("Data received:", data);

        bestCorrection.innerText = data.best_correction;

        suggestionsList.innerHTML = "";

        if (data.suggestions.length > 0) {
          data.suggestions.forEach((item) => {
            const li = document.createElement("li");
            li.innerText = item;
            suggestionsList.appendChild(li);
          });
        } else {
          suggestionsList.innerHTML = "<li>No suggestions found</li>";
        }
      })
      .catch((error) => {
        console.log("Fetch Error:", error);
        bestCorrection.innerText = "Server not connected!";
        suggestionsList.innerHTML = "<li>Backend error</li>";
      });

  });

});

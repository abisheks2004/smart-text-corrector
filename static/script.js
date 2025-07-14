document.addEventListener("DOMContentLoaded", function () {
  const modeToggle = document.getElementById("modeToggle");
  const body = document.body;

  modeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    const icon = modeToggle.querySelector("i");
    icon.dataset.feather = icon.dataset.feather === "sun" ? "moon" : "sun";
    feather.replace();
  });

  const input = document.getElementById("liveInput");
  const output = document.getElementById("liveOutput");
  const method = document.getElementById("method");

  let timeout = null;
  input.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      fetch("/live-correct", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: input.value,
          method: method.value
        }),
      })
      .then(res => res.json())
      .then(data => {
        output.innerHTML = data.corrected;
        output.style.display = "block";
      });
    }, 500);
  });
});

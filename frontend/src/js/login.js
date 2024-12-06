document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username, password }),
    });

    if (response.ok) {
      window.location.href = "/";
    } else {
      const errorData = await response.json();
      alert(`Login failed: ${errorData.detail || "Unknown error"}`);
    }
  } catch (error) {
    alert("An error occurred while trying to log in.");
    console.error(error);
  }
});

document.getElementById("signupForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("signupUsername").value;
  const password = document.getElementById("signupPassword").value;

  try {
    const response = await fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: username,
        password: password,
      }),
    });

    if (response.ok) {
      window.location.href = "/authorize";
    } else {
      const errorData = await response.json();
      alert(`Signup failed: ${errorData.detail || "Unknown error"}`);
    }
  } catch (error) {
    alert("An error occurred while trying to sign up.");
    console.error(error);
  }
});

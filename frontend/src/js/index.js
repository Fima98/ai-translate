function getAccessToken() {
  const name = "access_token=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookies = decodedCookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

async function translateText() {
  const text = document.getElementById("text").value;
  const languages = document.getElementById("languages").value;
  const loadingSpinner = document.getElementById("loadingSpinner");
  const translationsContainer = document.getElementById("translations");

  if (!text || !languages) {
    alert("Please provide both text and target languages.");
    return;
  }

  loadingSpinner.style.display = "block";

  const accessToken = getAccessToken();
  if (!accessToken) {
    alert("Access token not found. Please log in.");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        content: text,
        languages: languages.split(",").map((lang) => lang.trim()),
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to initiate translation");
    }

    const taskResponse = await response.json();
    const taskId = taskResponse.task_id;

    checkTranslationStatus(
      taskId,
      accessToken,
      translationsContainer,
      loadingSpinner
    );
  } catch (error) {
    console.error(error);
    alert("Error during translation request");
    loadingSpinner.style.display = "none";
  }
}

async function checkTranslationStatus(
  taskId,
  accessToken,
  translationsContainer,
  loadingSpinner
) {
  try {
    const response = await fetch(`http://localhost:8000/translate/${taskId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch translation status");
    }

    const translationData = await response.json();

    if (translationData.status === "pending") {
      setTimeout(
        () =>
          checkTranslationStatus(
            taskId,
            accessToken,
            translationsContainer,
            loadingSpinner
          ),
        2000
      );
    } else if (translationData.status === "completed") {
      displayTranslationResult(
        translationData.translations,
        translationsContainer
      );
      loadingSpinner.style.display = "none";
    }
  } catch (error) {
    console.error(error);
    alert("Error fetching translation status");
    loadingSpinner.style.display = "none";
  }
}

function displayTranslationResult(translations, translationsContainer) {
  translationsContainer.innerHTML = "";
  for (const [language, translation] of Object.entries(translations)) {
    const translationElement = document.createElement("div");
    translationElement.classList.add("translation-container");
    translationElement.innerHTML = `
<div class="translation"><strong>${language}</strong>: ${translation}</div>
`;
    translationsContainer.appendChild(translationElement);
  }
}

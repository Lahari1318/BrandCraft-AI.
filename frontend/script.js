
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("idea-input");
  const sendBtn = document.getElementById("send-btn");
  const chatMessages = document.getElementById("chat-messages");
  const newChatBtn = document.getElementById("new-chat-btn");
  const featureButtons = document.querySelectorAll(".feature-btn");
  const chatItems = document.querySelectorAll(".chat-item");

  const API = "http://127.0.0.1:8000/api/chat";

  let currentFeature = null;
  let currentQuestionIndex = 0;
  let userAnswers = {};
  let sessionId = newSessionId();
  let busy = false;

  function newSessionId() {
    return "brandcraft-" + Date.now() + "-" +
      Math.random().toString(36).slice(2);
  }

  function escapeHTML(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatText(value) {
    return escapeHTML(value).replace(/\n/g, "<br>");
  }

  const welcomeMessage = `
    <div class="flex items-start gap-4">
      <div class="w-10 h-10 rounded-full bg-brand-purple
                  flex items-center justify-center text-white">
        <i class="fa-solid fa-robot"></i>
      </div>
      <div class="bg-gray-100 rounded-2xl px-5 py-4 max-w-[85%]">
        <p>
          Hi! I'm your BrandCraft AI assistant.
          <br><br>
          I can help with YouTube thumbnails, brand names,
          taglines, social captions, content writing,
          and complete brand strategies.
        </p>
      </div>
    </div>
  `;

  chatMessages.innerHTML = welcomeMessage;

  // ------------------------------------
  // FEATURE QUESTIONS
  // ------------------------------------

  const questions = {
    "brand-name": [
      "Which industry does your brand belong to?",
      "Who is your target audience?",
      "What personality should the name have?",
      "Any themes or keywords to include?",
      "Any words or styles to avoid?"
    ],

    "tagline": [
      "What is your brand name?",
      "What is your main brand promise?",
      "Do you want a short or long tagline?",
      "What tone do you prefer?",
      "Any keywords to include?",
      "Do you already have a tagline?"
    ],

    "social-captions": [
      "Is this for a formal or informal platform?",
      "What is your brand name?",
      "What product or category are you promoting?",
      "What is your campaign goal?",
      "What tone do you prefer?",
      "Which social media platforms?",
      "Do you want short, medium, or long captions?"
    ],

    "content-writing": [
      "What type of content do you need?",
      "What is the topic or title?",
      "Who is your target audience?",
      "What tone do you prefer?",
      "What approximate length?",
      "Any SEO keywords?"
    ],

    "thumbnails": [
      "What is your YouTube video topic?",
      "What emotion should the thumbnail create?",
      "What big text should appear on the thumbnail?",
      "What colors do you prefer?",
      "What style do you want? (bold, cinematic, gaming, clean...)"
    ],

    "full-brand": [
      "Describe your business or product.",
      "Who is your ideal customer?",
      "What are your brand values?",
      "Do you have any existing brand ideas?",
      "Which brands inspire you?",
      "Where will your brand appear?",
      "Any budget or special requirements?"
    ]
  };

  // ------------------------------------
  // CHAT DISPLAY
  // ------------------------------------

  function scrollDown() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function addMessage(content, isUser = false) {
    const wrapper = document.createElement("div");

    wrapper.className = isUser
      ? "flex items-start gap-4 justify-end"
      : "flex items-start gap-4";

    if (isUser) {
      wrapper.innerHTML = `
        <div class="bg-brand-purple text-white rounded-2xl
                    px-5 py-4 max-w-[85%]">
          <p>${formatText(content)}</p>
        </div>
        <div class="w-10 h-10 rounded-full bg-gray-300
                    flex items-center justify-center">
          <i class="fa-solid fa-user"></i>
        </div>
      `;
    } else {
      wrapper.innerHTML = `
        <div class="w-10 h-10 rounded-full bg-brand-purple
                    flex items-center justify-center text-white
                    flex-shrink-0">
          <i class="fa-solid fa-robot"></i>
        </div>
        <div class="bg-gray-100 rounded-2xl px-5 py-4
                    max-w-[85%] overflow-hidden">
          <div class="response-content">${formatText(content)}</div>
        </div>
      `;
    }

    chatMessages.appendChild(wrapper);
    scrollDown();

    return wrapper;
  }

  function addError(error) {
    addMessage(
      "Something went wrong: " + error.message +
      "\nPlease check your backend terminal."
    );
  }

  // ------------------------------------
  // THUMBNAIL DISPLAY AND DOWNLOAD
  // ------------------------------------

  function showImages(data) {
    const images = data.image_urls || [];

    const wrapper = addMessage(data.reply || "Here are your designs.");

    if (!images.length) {
      return;
    }

    const content = wrapper.querySelector(".response-content");

    const heading = document.createElement("h3");
    heading.textContent = "Your YouTube Thumbnail Designs";
    heading.style.cssText =
      "font-weight:bold;font-size:18px;margin:18px 0;";

    content.appendChild(heading);

    images.forEach((url, index) => {
      if (!url.startsWith("data:image/svg+xml;base64,")) {
        return;
      }

      const card = document.createElement("div");

      card.style.cssText = `
        margin:18px 0;
        padding:12px;
        background:white;
        border-radius:16px;
        border:1px solid #e5e7eb;
      `;

      const label = document.createElement("p");
      label.textContent = "Design " + (index + 1);
      label.style.cssText =
        "font-weight:bold;margin-bottom:10px;";

      const image = document.createElement("img");
      image.src = url;
      image.alt = "YouTube Thumbnail " + (index + 1);
      image.style.cssText = `
        width:100%;
        max-width:650px;
        aspect-ratio:16/9;
        object-fit:contain;
        border-radius:12px;
        display:block;
      `;

      const download = document.createElement("a");
      download.href = url;
      download.download =
        "BrandCraft-Thumbnail-" + (index + 1) + ".svg";

      download.textContent = "Download Thumbnail";

      download.style.cssText = `
        display:inline-block;
        margin-top:12px;
        padding:10px 18px;
        background:#7C3AED;
        color:white;
        border-radius:10px;
        text-decoration:none;
        font-weight:bold;
      `;

      card.appendChild(label);
      card.appendChild(image);
      card.appendChild(download);
      content.appendChild(card);
    });

    const note = document.createElement("p");
    note.textContent =
      "Free SVG designs • Type 'alternative' for more layouts.";

    note.style.cssText = `
      font-size:13px;
      color:#6b7280;
      margin-top:12px;
    `;

    content.appendChild(note);
    scrollDown();
  }

  // ------------------------------------
  // BACKEND REQUEST
  // ------------------------------------

  async function sendToBackend(payload) {
    if (busy) return;

    busy = true;
    sendBtn.disabled = true;

    try {
      const response = await fetch(API, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...payload,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        let message = "Backend error: " + response.status;

        try {
          const errorData = await response.json();
          if (errorData.detail) {
            message += " - " + errorData.detail;
          }
        } catch (_) {}

        throw new Error(message);
      }

      const data = await response.json();

      if (data.session_id) {
        sessionId = data.session_id;
      }

      if (data.image_urls && data.image_urls.length) {
        showImages(data);
      } else {
        addMessage(data.reply || "No response received.");
      }

    } catch (error) {
      console.error(error);
      addError(error);

    } finally {
      busy = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  // ------------------------------------
  // GUIDED QUESTIONS
  // ------------------------------------

  function askNextQuestion() {
    if (!currentFeature) return;

    const list = questions[currentFeature] || [];

    if (currentQuestionIndex >= list.length) {
      finishFeature();
      return;
    }

    let summary = "";

    const answers = userAnswers[currentFeature] || {};

    const previous = Object.values(answers);

    if (previous.length) {
      summary = "So far you've said:\n";

      previous.forEach((answer, index) => {
        summary += (index + 1) + ". " + answer + "\n";
      });

      summary += "\n";
    }

    addMessage(summary + list[currentQuestionIndex]);

    input.placeholder = "Type your answer...";
  }

  async function finishFeature() {
    const feature = currentFeature;
    const answers = { ...userAnswers[feature] };

    currentFeature = null;
    currentQuestionIndex = 0;

    input.placeholder = "Describe your idea...";

    addMessage(
      "Thank you! Generating your " +
      feature.replace(/-/g, " ") + " now..."
    );

    await sendToBackend({
      text: "Generate final result",
      feature: feature,
      answers: answers
    });
  }

  // ------------------------------------
  // FEATURE BUTTONS
  // ------------------------------------

  featureButtons.forEach(button => {
    const feature = button.dataset.feature;

    // Remove logo feature from the interface
    if (feature === "logo") {
      button.style.display = "none";
      return;
    }

    button.addEventListener("click", () => {
      if (busy) return;

      featureButtons.forEach(btn => {
        btn.classList.remove("highlight");
      });

      button.classList.add("highlight");

      currentFeature = feature;
      currentQuestionIndex = 0;

      userAnswers[feature] = {};

      askNextQuestion();
    });
  });

  // ------------------------------------
  // HANDLE MESSAGES
  // ------------------------------------

  async function handleSend() {
    if (busy) return;

    const text = input.value.trim();

    if (!text) return;

    input.value = "";

    addMessage(text, true);

    if (currentFeature) {
      const feature = currentFeature;

      const key = "q" + (currentQuestionIndex + 1);

      userAnswers[feature][key] = text;

      currentQuestionIndex++;

      askNextQuestion();

      return;
    }

    await sendToBackend({
      text: text,
      feature: null,
      answers: null
    });
  }

  sendBtn.addEventListener("click", handleSend);

  input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  });

  // ------------------------------------
  // NEW CHAT
  // ------------------------------------

  function resetChat() {
    if (busy) return;

    currentFeature = null;
    currentQuestionIndex = 0;
    userAnswers = {};
    sessionId = newSessionId();

    chatMessages.innerHTML = welcomeMessage;

    input.value = "";
    input.placeholder = "Describe your brand / video idea...";

    featureButtons.forEach(button => {
      button.classList.remove("highlight");
    });

    input.focus();
  }

  if (newChatBtn) {
    newChatBtn.addEventListener("click", resetChat);
  }

  // Existing chat items are placeholders, not saved histories
  chatItems.forEach(item => {
    item.addEventListener("click", () => {
      resetChat();
      addMessage(
        "This version does not yet save chat history. " +
        "You can start a new conversation here."
      );
    });
  });

});

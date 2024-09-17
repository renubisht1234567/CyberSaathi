// Function to read email content
function readEmailContent() {
  const emailContentElement = document.querySelector('.ii.gt');

  if (emailContentElement) {
    const emailText = emailContentElement.innerText;
    const emailSnippet = emailText.slice(0, 1000);
    const emailHash = hashEmail(emailSnippet);

    // Remove this check to always display the prediction
    // const processedEmails = JSON.parse(localStorage.getItem("processedEmails")) || [];
    // if (!processedEmails.includes(emailHash)) {

    console.log('Email content snippet:', emailSnippet);
    predictSpam(emailSnippet, emailHash);
    // }
  } else {
    console.log('No email content found with the given selector.');
  }
}
// Function to hash the email content for uniqueness
function hashEmail(emailText) {
  let hash = 0;
  for (let i = 0; i < emailText.length; i++) {
    const char = emailText.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;  // Convert to 32-bit integer
  }
  return hash.toString();
}

// Function to send the email content to the ML model and get the spam prediction
function predictSpam(emailText, emailHash) {
  fetch('http://localhost:5000/predict', {  // Replace with your actual API URL
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ emailText: emailText })
  })
  .then(response => response.json())
  .then(data => {
    console.log('API response:', data);  // Log API response
    if (data.isSpam) {
      alert("This email is predicted to be spam.");
    } else {
      alert("This email is not spam.");
    }

    // After alert is shown, store the email hash to prevent future alerts for the same email
    const processedEmails = JSON.parse(localStorage.getItem("processedEmails")) || [];
    processedEmails.push(emailHash);
    localStorage.setItem("processedEmails", JSON.stringify(processedEmails));
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Debounce function to limit excessive triggering
let debounceTimer;
const debounce = (callback, delay) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(callback, delay);
};

// Observer to detect when an email is opened
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'childList' && mutation.addedNodes.length) {
      debounce(() => {
        if (document.querySelector('.ii.gt')) {
          console.log("Email content detected.");
          readEmailContent();
        }
      }, 500);  // Wait 500ms before executing to prevent multiple calls
    }
  });
});

// Observe the body for changes, indicating that an email has been opened
observer.observe(document.body, {
  childList: true,
  subtree: true
});

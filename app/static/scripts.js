// scripts.js
abc = copyText()

function copyText() {
    const selectedText = window.getSelection().toString();
  
    navigator.clipboard.writeText(selectedText)
      .then(() => {
        console.log('Text copied successfully');
      })
      .catch((error) => {
        console.error('Error copying text:', error);
      });
  }
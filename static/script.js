// ---------------------------------------------------------------------
// Basic Encryption & Decryption Using Caesar Cipher — Frontend Logic
// Talks to the Flask backend (/encrypt and /decrypt) via fetch().
// ---------------------------------------------------------------------

const plaintextEl   = document.getElementById('plaintext');
const shiftEl        = document.getElementById('shift');
const errorEl        = document.getElementById('error-msg');
const verifyEl       = document.getElementById('verify-msg');

const outOriginal    = document.getElementById('out-original');
const outEncrypted   = document.getElementById('out-encrypted');
const outDecrypted   = document.getElementById('out-decrypted');

const btnEncrypt     = document.getElementById('btn-encrypt');
const btnDecrypt     = document.getElementById('btn-decrypt');
const btnClear       = document.getElementById('btn-clear');
const formulaBadge   = document.getElementById('live-formula');

function clearMessages() {
  errorEl.textContent = '';
  verifyEl.textContent = '';
  verifyEl.className = 'verify-msg';
}

function showError(message) {
  errorEl.textContent = message;
  verifyEl.textContent = '';
  verifyEl.className = 'verify-msg';
}

function showVerified(isVerified) {
  if (isVerified) {
    verifyEl.textContent = '✓ Encryption and decryption verified successfully';
    verifyEl.className = 'verify-msg ok';
  } else {
    verifyEl.textContent = '✗ Verification failed — decrypted text did not match the original.';
    verifyEl.className = 'verify-msg fail';
  }
}

async function postJSON(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  let data;
  try {
    data = await response.json();
  } catch (err) {
    throw new Error('The server returned an unexpected response. Please try again.');
  }

  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Something went wrong. Please try again.');
  }

  return data;
}

async function handleEncrypt() {
  clearMessages();
  const text = plaintextEl.value;
  const shift = shiftEl.value;

  formulaBadge.textContent = 'E(x) = (x + n) mod 26';

  try {
    const data = await postJSON('/encrypt', { text, shift });
    outOriginal.textContent = data.original;
    outEncrypted.textContent = data.result;
    outDecrypted.textContent = '—';
    showVerified(data.verified);
  } catch (err) {
    showError(err.message);
    outEncrypted.textContent = '—';
  }
}

async function handleDecrypt() {
  clearMessages();
  formulaBadge.textContent = 'D(x) = (x − n) mod 26';

  // Decrypt whatever is currently shown as the encrypted output,
  // falling back to the textarea if the user typed ciphertext directly.
  const currentEncrypted = outEncrypted.textContent.trim();
  const hasEncryptedOutput = currentEncrypted && currentEncrypted !== '—';
  const text = hasEncryptedOutput ? currentEncrypted : plaintextEl.value;
  const shift = shiftEl.value;

  try {
    const data = await postJSON('/decrypt', { text, shift });
    outDecrypted.textContent = data.result;

    if (hasEncryptedOutput) {
      const originalMatches = data.result === outOriginal.textContent;
      showVerified(originalMatches);
    }
  } catch (err) {
    showError(err.message);
    outDecrypted.textContent = '—';
  }
}

function handleClear() {
  plaintextEl.value = '';
  shiftEl.value = 3;
  outOriginal.textContent = '—';
  outEncrypted.textContent = '—';
  outDecrypted.textContent = '—';
  clearMessages();
  formulaBadge.textContent = 'E(x) = (x + n) mod 26';
  plaintextEl.focus();
}

btnEncrypt.addEventListener('click', handleEncrypt);
btnDecrypt.addEventListener('click', handleDecrypt);
btnClear.addEventListener('click', handleClear);

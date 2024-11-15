document.querySelector('form').addEventListener('submit', (e) => {
  const email = document.querySelector('input[name="email"]').value;
  localStorage.setItem('email', email);
});
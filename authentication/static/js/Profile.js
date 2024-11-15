window.onload = () => {
  const email = localStorage.getItem('email');
  if (!email) {
      alert("You need to log in to access this page!");
      window.location.href = '/accounts/login/';
  }
};
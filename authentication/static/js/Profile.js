// Function to trigger the file input when the "Select Picture" button is clicked
function triggerFileInput() {
  document.getElementById("profile-picture-input").click();
}

// Function to show the preview of the selected image
function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById("profile-picture-preview");
  
  if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = "block"; // Show the image
      };
      reader.readAsDataURL(input.files[0]); // Read the file as a data URL
  }
}

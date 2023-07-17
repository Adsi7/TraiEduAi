function openModal(modalId) {
  $('#'+modalId).modal('show');
}

        const toggleButton = document.querySelector('.druck');
    // Get the filter wrapper element
    const filterWrapper = document.querySelector('#navbarSupportedContent');

    // Add event listener to toggle button
    toggleButton.addEventListener('click', function() {
      filterWrapper.classList.toggle('show');
    });
console.log("test");

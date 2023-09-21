const slideshowContainers = document.querySelectorAll('.slideshow-container');

slideshowContainers.forEach((container) => {
  const slidesContainer = container.querySelector('.slides');
  const slides = container.querySelectorAll('.slides img');
  const dots = container.querySelectorAll('.dot');
  let currentIndex = parseInt(container.dataset.initialIndex) || 0;

  function showSlide(index) {
    slidesContainer.style.transform = `translateX(-${index * 100}%)`;
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

  function autoSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      currentIndex = i;
      showSlide(currentIndex);
    });
  });

  const slideTime = parseInt(container.dataset.slideTime) || 10000;
  if (slideTime !== -1) {
    setInterval(autoSlide, slideTime);
  }

  showSlide(currentIndex);
});
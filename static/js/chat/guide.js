const guideExamples = document.querySelectorAll('.guide-example');

if (guideExamples != null){
  guideExamples.forEach((guideExample) => {
    const deleteLink = guideExample.querySelector('.delete-link');

    guideExample.addEventListener('mouseenter', showDeleteLink);
    guideExample.addEventListener('mouseleave', hideDeleteLink);

    function showDeleteLink() {
      deleteLink.style.display = 'block';
    }

    function hideDeleteLink() {
      deleteLink.style.display = 'none';
    }
  });
}
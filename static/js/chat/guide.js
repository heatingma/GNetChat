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



var wrapper = document.querySelector("#guide-hidden-show");
var guide_content = document.querySelector("#guide-content");
var guide_down_right = document.querySelector("#guide-down-right");

if (wrapper != null){
  wrapper.addEventListener("click", function() {
      guide_content.classList.toggle("guide-content-display-hidden");
      guide_down_right.classList.toggle("mdi-chevron-right");
  });
}
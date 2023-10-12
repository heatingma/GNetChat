// 获取所有的 guide-example 元素
const guideExamples = document.querySelectorAll('.guide-example');

// 遍历每个 guide-example 元素并添加事件监听器
guideExamples.forEach((guideExample) => {
  const deleteLink = guideExample.querySelector('.delete-link');

  // 添加鼠标悬停事件监听器
  guideExample.addEventListener('mouseenter', showDeleteLink);
  guideExample.addEventListener('mouseleave', hideDeleteLink);

  // 鼠标悬停时显示 delete-link 元素
  function showDeleteLink() {
    deleteLink.style.display = 'block';
  }

  // 鼠标离开时隐藏 delete-link 元素
  function hideDeleteLink() {
    deleteLink.style.display = 'none';
  }
});
scrollUpButton()

function scrollUpButton() {
  var body = document.querySelector('body');
  var button = document.createElement('div');
  var offset = (document.querySelector('body').clientWidth - document.querySelector('main').clientWidth) / 2;
  window.showScrollUp = false

  button.id = 'scroll-up-button'
  css(button, {
    position: "fixed",
    width: "40px",
    height: "40px",
    bottom: "30px",
    right: `${offset + 30}px`,
    color: "#333333 !important",
    opacity: 0,
    cursor: 'pointer',
    visibility: 'hidden',
    transition: '0.3s ease opacity'
  })

  button.innerHTML += `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-arrow-up-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 0 0 8a8 8 0 0 0 16 0zm-7.5 3.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V11.5z"/>
  </svg>`

  var svg = button.querySelector('svg')
  css(svg, {
    borderRadius: '20px',
    background: 'white'
  })

  button.addEventListener("click", () => {
    window.scrollTo(0, 0);
  })

  body.append(button)

  document.addEventListener("scroll", () => {
    if (window.scrollY > window.innerHeight && !window.showScrollUp) {
      var el = document.getElementById('scroll-up-button');
      window.showScrollUp = true
      css(el, { opacity: 1, visibility: 'visible' })
    }
    if (window.scrollY < window.innerHeight && window.showScrollUp) {
      var el = document.getElementById('scroll-up-button');
      window.showScrollUp = false
      css(el, { opacity: 0 })
      setTimeout(() => css(el, { visibility: 'hidden' }), 300)
    }
  });
}

function css(element, style) {
  for (const property in style)
    element.style[property] = style[property];
}
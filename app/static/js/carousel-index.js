// Sets the glider in the index page at the glider element

new Glider(document.querySelector('.glider'), {
  slidesToShow: 3.5,
  draggable: true,
  dots: '.dots',
  arrows: {
    prev: '.glider-prev',
    next: '.glider-next'
  },
  responsive: [
    {
      breakpoint: 0,
      settings: {
        slidesToShow: 1.1
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2.1
      }
    },
    {
      breakpoint: 1000,
      settings: {
        slidesToShow: 3.5
      }
    },
  ]
});
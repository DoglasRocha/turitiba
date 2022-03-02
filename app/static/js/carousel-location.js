new Glider(document.querySelector('.glider'), {
    slidesToShow: 2.5,
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
          slidesToShow: 2.5
        }
      },
    ]
  });
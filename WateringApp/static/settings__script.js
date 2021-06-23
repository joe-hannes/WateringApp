$('document').ready( () =>
{

  $('#reset-water-level').on('click', () =>
{
  console.log('clicked reset');
  $.ajax({
    url:'/reset_water_level',
    method:'POST',
    success: (result) =>
    {
      console.log(result);
      $('div#refill-message').fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
    }
  });
});

});

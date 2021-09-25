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

var slider = document.getElementById("activation-level");
var output = document.getElementById("range-value");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}

$('#rb-external-db').on('click', () =>
{

  {
      $('#div-external-db').css({'display':'block'});
  }
})

});

function openSetting(name)
{
  var i;
  var x = document.getElementsByClassName("setting");
  var tabs = document.getElementsByClassName("tab");
  for (var i = 0; i < x.length; i++)
  {
    x[i].style.display = "none";
    tabs[i].style.background = "#7E888A";
  }
  document.getElementById(name).style.display = "block";
  document.getElementById(name + "-tab").style.backgroundColor = "white";
}

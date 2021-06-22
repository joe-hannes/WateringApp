
$(document).ready(() =>
{

console.log('display: ' + $('#menu_items').css("display"));

  $('#app-bar').on('click', () =>
  {
    if ($('#menu-items').css("display") == "block")
    {

      $('#menu-items').css({"display":'none'});

    }
    else
    {

      $('#menu-items').css({"display":'block'});

    }
  });



  });

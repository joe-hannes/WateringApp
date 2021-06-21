
$(document).ready(() =>
{
  getActivationLevel();

$('#app-bar').on('click', () =>
{
  if ($('#restart-item').css("display") == "block")
  {
    $('#restart-item').css({"display":'none'});
    $('#activation-level-item').css({"display":'none'});
    $('#user-item').css({"display":'none'});
    $('#statistics-item').css({"display":'none'});
    $('#widget-item').css({"display":'none'});
    $('#settings-item').css({"display":'none'});
  }
  else
  {
    $('#restart-item').css({"display":'block'});
    $('#activation-level-item').css({"display":'block'});
    $('#user-item').css({"display":'block'});
    $('#statistics-item').css({"display":'block'});
    $('#widget-item').css({"display":'block'});
    $('#settings-item').css({"display":'block'});


  }
});

$('#statistics-item').on('click', () =>
{

  if($(window).width() < 767)
  {
    window.location.href ="http://192.168.178.41:3000/d/FgnUzHRgz/watering-system-dashboard-mobile?orgId=1&from=now-30m&to=now";

  }

  else
  {
    window.location = '/statistics'
  }

});


$('#settings-item').on('click', () =>
{
    window.location = '/settings'
});

$('#user-item').on('click', () =>
{
    window.location = '/user'
});







$('#widget-item').on('click', () =>
{
  window.location = '/'
});

// $('#range-div').css({'display': 'flex', 'justify-content':'center'})




$('body').on('input', '#activation-input', () =>
{
  $('#range-value').text('\xa0' + $('#activation-input').val() + " %");
});

$('body').on('mouseup', '#activation-input', () =>
{
  console.log("mouseupevent");
  updateActivationLevel()
});

$('#restart-item').on('click', () =>
{
  restart();
});


function updateActivationLevel()
{

  data = $('#activation-input').val()
  console.log(data);
  $.ajax(
    {
       type: 'POST',
       url: "/updateActivationLevel",
       data: {data: data},

       success: (result) =>
        {
          console.log("Activation Level Updated Successfully");
        }
    });
}

function getActivationLevel()
{
  $.ajax(
    {
     url:'/getActivationLevel',
     type:'POST',
     success: (result) =>
      {
        console.log('activation_val: ' + result);
        $('#activation-input').val(result)
        $('#range-value').text('\xa0' + result + "%");
      }
    });
}

function restart()
{
  $.ajax({ url:'/restart', success: (result) =>
  {
    console.log("Restarting");
  }});
}
}

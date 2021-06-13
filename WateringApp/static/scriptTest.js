
$(document).ready(() =>
{

  getActivationLevel();

  ajaxRequest();

  function ajaxRequest()
  {

    $.ajax({url:'/json', success: (result) =>
  {
      var obj = JSON.parse(result);
      console.log("result: " + result);
      // console.log("json: " + obj[0]["value"]);
      // console.log("json: " + obj[0])
      i = 0;
      for (element of obj["results"]["channel"] )
      {
        $('.value-div').append('<div id = "channel' + i + '" > </div>');
        // $('#channel' + i).append("<iframe src='/'></iframe>");
        $('#channel' + i).append("<tr><td>Channel</td><td class='value'>" + element["channel"] + "</td></tr>");
        $('#channel' + i).append("<tr><td>Value</td><td class='value'>" + element["value"] + "</td></tr>");
        $('#channel' + i).append("<tr><td>Percent </td> <td class='value'>" + element["percentString"] + "</td></tr>");

        if (element['active'] == 1)
        {
          $('#channel' + i).append("<tr><td>Active </td> <td id='activeCell" + i + "' class='value'></td></tr>");
          $('#activeCell' + i).append('<div style="border-radius:5px; height:10px; width:10px; background-color:green"> </div>');
        }
        else
        {
          $('#channel' + i).append("<tr><td>Inactive </td> <td id='activeCell" + i + "' class='value'  ></td></tr>");
          $('#activeCell' + i).append('<div style="border-radius:5px; height:10px; width:10px; background-color:red"> </div>');
        }

        $('#channel' + i).css({'border': 1 + 'px solid red', 'margin' : 10 + 'px', 'padding' : 10 + 'px', 'width': 8 + 'em' });
        i++;
      }


      $('.avg-div').append('<tr><td> Average  Value</td><td class="value">' + obj.results.average.value + "\xa0" + ' </tr></td>');
      $('.avg-div').append('<tr><td>Percent</td> <td class="value">' + obj.results.average.percentString + ' </tr></td>');


}});

//  CSS Styling

$('body').css({'background':'grey', 'text-color':'white'});
$('.avg-div').css({"margin": "auto", "width": 100 + '%', 'border': 1 + 'px solid red', 'display':'flex', "justify-content":"center", 'flex-wrap':'wrap'});
$('.value').css({ 'padding-left': 5 + 'px' });
$('.value-div').css({'border': 1 + 'px solid red'});
$('.value-div').css({'display':'flex', "justify-content":"center", 'flex-wrap':'wrap'});
$('#menu').css({'text-align':'center'});
$('#app-bar').css({'text-align':'center', color:'black'});
$('div').css({'color':'white'});
$('.fa-bars').css({'text-align':'left', 'color':'black'});
$('#restart-item').css({ 'color':'black'});
$('#restart-item').css({ 'display':'none'});

$('#widget-item').css({ 'color':'black'});
$('#widget-item').css({ 'display':'none'});

$('#user-item').css({ 'display':'none'});
$('#user-item').css({ 'color':'black'});
$('#statistics-item').css({ 'display':'none'});
$('#statistics-item').css({ 'color':'black'});
$('#activation-level-item').css({ 'display':'none'});
$('#range-div').css({'color':'black'});
$('#range-value').css({'color':'black'});
$('#pump-activation-label').css({'color':'black'});


// $('#app-bar').css({'display':'flex', 'justify-content':'left'});


//  On- Click Handlers

$('#app-bar').on('click', () =>
{
  if ($('#restart-item').css("display") == "block")
  {
    $('#restart-item').css({"display":'none'});
    $('#activation-level-item').css({"display":'none'});
    $('#user-item').css({"display":'none'});
    $('#statistics-item').css({"display":'none'});
    $('#widget-item').css({"display":'none'});
  }
  else
  {
    $('#restart-item').css({"display":'block'});
    $('#activation-level-item').css({"display":'block'});
    $('#user-item').css({"display":'block'});
    $('#statistics-item').css({"display":'block'});
    $('#widget-item').css({"display":'block'});

  }
});

$('#statistics-item').on('click', () =>
{
  window.location = '/statistics'
})



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

$('#widget-item').on('click', () =>
{
  window.location = '/'
});

// $('#range-div').css({'display': 'flex', 'justify-content':'center'})
}

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



  });



$(document).ready(() =>
{

//   var socket = io.connect('http://' + document.domain + ':' + location.port);
//
//   socket.on('message', (msg) =>
// {
// console.log(msg);
// });

  getWidgetState();
// make a request to the server every 500ms and update
  setInterval(ajaxRequest, 5000);




function sendMessage()
{
      socket.send('joined');
}

// make get request to server and update the droplet widget accordingly
function ajaxRequest()
{
  $.ajax({url:'/json', success: (result) =>
{
  // console.log('result: ' + result);
  var obj = JSON.parse(result);
  console.log(obj);
  $('#value-text').html(obj["results"]["channel"][1].percentString);
  console.log('water_level: ' + obj["results"]["water_level"]);
  $('.ocean').css('height', obj["results"]["water_level"] + 'vh');
  animateProgressBar(obj["results"]["channel"][1].percent);
}});
}

function toggleWidgetState()
{
  console.log("Widget Function");
  $.ajax({url:'/toggleAutoMode', success: (result) =>
  {
    console.log(result);
  }});
}

function getWidgetState()
{
  console.log("Widget Function");
  $.ajax({url:'/getWidgetState', success: (result) =>
  {

    switch (result)
    {
      case "False":
        console.log("False Case");
        $('#playtopause').css('visibility', 'visible');
        $('#pausetoplay').css('visibility', 'hidden');
        $('#active-icon').css('visibility', 'hidden');
        $('#error-icon').css('visibility', 'visible');
        $('#active-text').css('visibility', 'hidden');
        $('#pause-text').css('visibility', 'visible');
        $('#status-area').css('fill', '#d35f60');
        $('#status').css('stroke', '#d35f60');
        break;

      case "True":
        $('#playtopause').css('visibility', 'hidden');
        $('#pausetoplay').css('visibility', 'visible');
        $('#active-text').css('visibility', 'visible');
        $('#pause-text').css('visibility', 'hidden');
        $('#active-icon').css('visibility', 'visible');
        $('#error-icon').css('visibility', 'hidden');
        $('#status-area').css('fill', '#79ab64');
        $('#status-area').css('stroke', '#79ab64');
        break;


    }
  }
  });
}


function activatePump()
{
  $.ajax({url:'/activatePump', success: (result) =>
{
  console.log("Successfully activated pump");
}});
}

// code to make the progress bar have a fill effect
function animateProgressBar(data)
{
  const meters = $('svg[data-value] #progress-bar');
  var path = meters.get(0);

  // Get the length of the path
  let length = path.getTotalLength();

  // console.log(length);
  let value = parseInt(path.parentNode.parentNode.getAttribute('data-value'));
  // console.log(value);
  // Calculate the percentage of the total length
  // let to = length * ((100 - value) / 100);
  let to =  (length/100) *  (100 - data);


  // Trigger Layout in Safari hack https://jakearchibald.com/2013/animated-line-drawing-svg/
  path.getBoundingClientRect();
  // Set the Offset
  path.style.strokeDashoffset = Math.max(0, to);
}

// onClick Event Handlers
// handle button clicks pause-buttonn




$('#drop-circle').on('click', () =>
{
  activatePump();
  $( "div#pump-message" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
});



$('#cog-circle').on('click', () =>
{
  window.location = '/home';
});



// $('#play-btn').on('click', () =>
// {
//   $('#play-btn').css('visibility', 'hidden');
//   $('#pause-btn').css('visibility', 'visible');
//   $('#active-text').css('visibility', 'visible');
//   $('#pause-text').css('visibility', 'hidden');
//   $('#active-icon').css('visibility', 'visible');
//   $('#error-icon').css('visibility', 'hidden');
//   $('#status-area').css('fill', '#79ab64');
//   $('#status-area').css('stroke', '#79ab64');
// });
//
// // handle button click play-button
//
// $('#pause-btn').on('click', () =>
// {
//   $('#play-btn').css('visibility', 'visible');
//   $('#pause-btn').css('visibility', 'hidden');
//   $('#active-icon').css('visibility', 'hidden');
//   $('#error-icon').css('visibility', 'visible');
//   $('#active-text').css('visibility', 'hidden');
//   $('#pause-text').css('visibility', 'visible');
//   $('#status-area').css('fill', '#d35f60');
//   $('#status').css('stroke', '#d35f60');
// });

$('#pause-circle').on('click', () =>
{
  toggleWidgetState();
  $("div#wsys-message").fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
  // $('#play-btn').css('visibility', 'visible');
  // $('#pause-btn').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'hidden');
  $('#error-icon').css('visibility', 'visible');
  $('#active-text').css('visibility', 'hidden');
  $('#pause-text').css('visibility', 'visible');
  $('#status-area').css('fill', '#d35f60');
  $('#status-area').css('stroke', '#d35f60');
});

$('#play-circle').on('click', () =>
{
  toggleWidgetState();
  $( "div#wsys-message" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
  // $('#play-btn').css('visibility', 'hidden');
  // $('#pause-btn').css('visibility', 'visible');
  $('#active-text').css('visibility', 'visible');
  $('#pause-text').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'visible');
  $('#error-icon').css('visibility', 'hidden');
  $('#status-area').css('fill', '#79ab64');
  $('#status-area').css('stroke', '#79ab64');
});


$('#pause-circle2').on('click', () =>
{
  toggleWidgetState();
  $('#play-btn').css('visibility', 'visible');
  $('#pause-btn').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'hidden');
  $('#error-icon').css('visibility', 'visible');
  $('#active-text').css('visibility', 'hidden');
  $('#pause-text').css('visibility', 'visible');
  $('#status-area').css('fill', '#d35f60');
  $('#status-area').css('stroke', '#d35f60');
});

$('#play-circle2').on('click', () =>
{
  toggleWidgetState();
  // $('#play-btn').css('visibility', 'hidden');
  // $('#pause-btn').css('visibility', 'visible');
  $('#active-text').css('visibility', 'visible');
  $('#pause-text').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'visible');
  $('#error-icon').css('visibility', 'hidden');
  $('#status-area').css('fill', '#79ab64');
  $('#status-area').css('stroke', '#79ab64');
});


});

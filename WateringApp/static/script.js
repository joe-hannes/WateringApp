

$(document).ready(() =>
{

  getWidgetState();
// make a request to the server every 500ms and update
  setInterval(ajaxRequest, 500);



// make get request to server and update the droplet widget accordingly
function ajaxRequest()
{
  $.ajax({url:'/json', success: (result) =>
{
  console.log('result: ' + result);
  var obj = JSON.parse(result);
  console.log(obj);
  $('#value-text').html(obj[0].percentString)
  animateProgressBar(obj[0].percent)
}});
}

function toggleWidgetState()
{
  console.log("Widget FUnction");
  $.ajax({url:'/toggleAutoMode', success: (result) =>
  {
    console.log(result);
  }});
}

function getWidgetState()
{
  console.log("Widget FUnction");
  $.ajax({url:'/getWidgetState', success: (result) =>
  {

    switch (result)
    {
      case "False":
        console.log("FLase Case");
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

  console.log(length);
  let value = parseInt(path.parentNode.parentNode.getAttribute('data-value'));
  console.log(value);
  // Calculate the percentage of the total length
  // let to = length * ((100 - value) / 100);
  let to =  (length/100) *  (100 - data)


  // Trigger Layout in Safari hack https://jakearchibald.com/2013/animated-line-drawing-svg/
  path.getBoundingClientRect();
  // Set the Offset
  path.style.strokeDashoffset = Math.max(0, to);
}

// onClick Event Handlers
// handle button clicks pause-button




$('#drop-circle').on('click', () =>
{
  activatePump();
  $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
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
  // $('#status-area').css('fill', '#79ab64');
  // $('#status-area').css('stroke', '#79ab64');
});


});

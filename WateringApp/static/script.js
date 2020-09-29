

$(document).ready(() =>
{


// make a request to the server every 500ms and update
  setInterval(ajaxRequest, 500);



// make get request to server and update the droplet widget accordingly
function ajaxRequest()
{
  $.ajax({url:'/json', success: (result) =>
{
  console.log('result: ' + result);
  var obj = JSON.parse(result);
  $('#value-text').html(obj.percentString)
  animateProgressBar(obj.percent)
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
  let to = length * ((100 - parseInt(data)) / 100);


  // Trigger Layout in Safari hack https://jakearchibald.com/2013/animated-line-drawing-svg/
  path.getBoundingClientRect();
  // Set the Offset
  path.style.strokeDashoffset = Math.max(0, to);
}

// onClick Event Handlers
// handle button clicks pause-button

$('#play-btn').on('click', () =>
{
  $('#play-btn').css('visibility', 'hidden');
  $('#pause-btn').css('visibility', 'visible');
  $('#active-text').css('visibility', 'visible');
  $('#pause-text').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'visible');
  $('#error-icon').css('visibility', 'hidden');
  $('#status-area').css('fill', '#79ab64');
  $('#status-area').css('stroke', '#79ab64');
});

// handle button click play-button

$('#pause-btn').on('click', () =>
{
  $('#play-btn').css('visibility', 'visible');
  $('#pause-btn').css('visibility', 'hidden');
  $('#active-icon').css('visibility', 'hidden');
  $('#error-icon').css('visibility', 'visible');
  $('#active-text').css('visibility', 'hidden');
  $('#pause-text').css('visibility', 'visible');
  $('#status-area').css('fill', '#d35f60');
  $('#status').css('stroke', '#d35f60');
});

});

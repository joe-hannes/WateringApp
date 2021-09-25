

$(document).ready(() =>
{

  getWidgetState();
// make a request to the server every 500ms and update
  setInterval(ajaxRequest, 500);



// make get request and update the droplet widget accordingly
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
});

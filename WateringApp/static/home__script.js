

$(document).ready(() =>
{
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

}

//  CSS Styling


$('.avg-div').css({"margin": "auto", "width": 100 + '%', 'border': 1 + 'px solid red', 'display':'flex', "justify-content":"center", 'flex-wrap':'wrap', 'color': 'white'});
$('.value').css({ 'padding-left': 5 + 'px', 'color': 'white' });
$('.value-div').css({'border': 1 + 'px solid red', 'color': 'white'});
$('.value-div').css({'display':'flex', "justify-content":"center", 'flex-wrap':'wrap'});





  });

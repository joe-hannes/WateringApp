
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
        // obj = JSON.parse(element);
        // console.log(obj);

        $('.value-div').append('<div id = channel' + i + '> </div>')
        $('#channel' + i).append("<tr><td>Channel </td><td>" + element["channel"] + "</td></tr>");
        $('#channel' + i).append("<tr><td>Value</td><td>" + element["value"] + "</td></tr>");
        $('#channel' + i).append("<tr><td>Percent </td> <td>" + element["percentString"] + "</td></tr>");
        $('#channel' + i).append("<tr><td>Active </td> <td id='activeCell" + i + "'  ></td></tr>");
        if (element['active'] == 1)
        {
          $('#activeCell' + i).append('<div style="border-radius:5px; height:10px; width:10px; background-color:green"> </div>');
        }
        else
        {
          $('#activeCell' + i).append('<div style="border-radius:5px; height:10px; width:10px; background-color:red"> </div>');
        }
        $('#channel' + i).css({'border': 1 + 'px solid red', 'float' : 'left', 'margin' : 10 + 'px', 'padding' : 10 + 'px'});
        i++;
      }
      $('.value-div').append("<tr><td>Average </td> <td>" + obj["results"]["average"] + "</td></tr>");

  }});
  }
});

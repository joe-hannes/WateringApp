
$(document).ready(() =>
{


  ajaxRequest();

  function ajaxRequest()
  {

    $.ajax({url:'/json', success: (result) =>
  {
      var obj = JSON.parse(result);
      console.log("result: " + result);
      console.log("json: " + obj[0]["value"]);
      // console.log("json: " + obj[0])
      for (element of obj )
      {
        // obj = JSON.parse(element);
        // console.log(obj);
        $('.value-div').append("<tr><td>Value</td><td>" + element["value"] + "</td></tr>");
        $('.value-div').append("<tr><td>Percent</td> <td>" + element["percentString"] + "</td></tr>");
      }

  }});
  }
});

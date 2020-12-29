
$(document).ready(() =>
{


  ajaxRequest();

  function ajaxRequest()
  {

    $.ajax({url:'/json', success: (result) =>
  {
      var obj = JSON.parse(result);
      console.log("json: " + result);
      console.log("json: " + obj);
      obj = obj
      $('.value-div').append("<tr><td>Value</td><td>" + obj.value + "</td></tr>");
      $('.value-div').append("<tr><td>Percent</td> <td>" + obj.percentString + "</td></tr>");
  }});
  }
});

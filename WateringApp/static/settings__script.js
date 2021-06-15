$('document').ready(() =>
{
  $('#settings-submit').on('click', () =>
  {

      locationValue = $('#input-location').val()
      reservoirSize = $('#input-reservoir').val()
      reservoirWarn = $('#input-reservoir-warn').val()
      activationLevel = $('#input-activation-level').val()

      var data = {
        location: locationValue,
        reservoir_size: reservoirSize,
        reservoir_warn_level: reservoirWarn
        // activation_level: activationLevel
      }

      json_data = JSON.stringify(data)

      console.log(json_data);
      $.ajax(
        {
          type: 'POST',
          contentType:'application/json; charset=utf-8',
          url:'/updateUser',

          data: json_data,

          success: (result) =>
          {
            console.log(result)
          }
      })
  });


  $('#temperature-submit').on('click', () =>
  {
      $.ajax(
        {
          type: 'POST',
          url:'/getTemperature',
          success: (result) =>
          {
            $('#temp').html(result)
          }
      })
  });


})

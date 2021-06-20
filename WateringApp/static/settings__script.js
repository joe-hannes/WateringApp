$('document').ready(() =>
{
  $('#settings-submit').on('click', () =>
  {

      locationValue = $('#input-location').val()
      reservoirSize = $('#input-reservoir').val()
      reservoirWarn = $('#input-reservoir-warn').val()
      // activationLevel = $('#input-activation-level').val()
      consumption = $('#input-consumption').val()

      var data = {
        location: locationValue,
        reservoir_size: reservoirSize,
        reservoir_warn_level: reservoirWarn,
        consumption: consumption
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


  $('#settings-item').on('click', () =>
  {
      window.location = '/settings'
  });

  $('#user-item').on('click', () =>
  {
      window.location = '/user'
  });







  $('#widget-item').on('click', () =>
  {
    window.location = '/'
  });

  // $('#range-div').css({'display': 'flex', 'justify-content':'center'})




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


});

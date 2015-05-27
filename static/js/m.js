(function(){
    var $ = jQuery;
    var $html = $('html');
    var google = window.google;
    var initMaps = function () {
        var geocoder;
        var map;
        var location;

        if( google && $('body').find('#map-canvas').length )
        {
          //Initialize map
          geocoder = new google.maps.Geocoder();
          var latlng = new google.maps.LatLng(64.139107, -21.928057);
          var mapOptions = {
            zoom: 13,
            center: latlng
          }
          map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

          //Get geocode for address and draw marker
          var address = $('.address').text() + ", " + $('.city').text() + ", "+ $('.country').text();
          geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
              location = results[0].geometry.location;
              map.setCenter(location);
              var marker = new google.maps.Marker({
                  map: map,
                  position: location
              });
            }
            else
            {
              ;;;window.console&&console.log( 'oh noes map address did not pan out' );
            }
          });
        }

        };

    var tempCountries = [];
    $('#continents').on('change', function (e) {
        $('#countries .hideopts option').unwrap('<span class="hideopts"></span>');

        var continent = $(this).val(),
            countries = $('#countries option[data-continent!="'+ continent +'"]').not(':first');

        if( continent !== 'Any' )
        {
          countries.wrap('<span class="hideopts"></span>');
        }
    });


    //Country list autocomplete
    var countries = [];
    $('.countries li').each(function () {
        countries.push( $(this).text() );
      });

    $('#country, #countries').autocomplete({
        source: countries
    });

    //Append more file attachments fields
    var attachment = $('.file_input'),
        no_attachments = attachment.length;

    $('<a class="add_attachment" href="#">..more</a>').insertAfter(attachment);

    $('body').on('click', '.add_attachment', function (e) {
        e.preventDefault();

        var link = $(this);
        var attachmentClone = attachment.clone(),
            name = attachment.find('input').attr('name').split('_')[0] + "_" + (no_attachments++);

        attachmentClone.find('input').attr('name', name);

        attachmentClone.insertBefore( link );
      });


    //Datepicker stuff
    $('#start_date, #end_date, #searchdate').datepicker({
        minDate: 0,
        dateFormat: 'yy-mm-dd'
    }).on('change', function (e) {
        if( $(this).is('#start_date') )
        {
            var newMinDate = $(this).val();
            $('#end_date').datepicker( 'option', 'minDate', newMinDate );
        }
      });


    var confirmDelete = function () {
            var deleteBtn = $('.delete');

            deleteBtn
                .on('click', function (e) {
                    e.preventDefault();
                    var link = $(this);
                    if ( confirm("Are you sure you want to delete this event?") )
                    {
                      $html.addClass('ajax-wait');
                      $.get(
                            link.attr('href')
                          )
                        .done(function(data) {
                            link.parents('tr').remove();
                          })
                        .always(function() {
                            $html.removeClass('ajax-wait');
                          });
                    }
                  });
      };

    //Google maps
    initMaps();

    //Confirm delete in admin part
    confirmDelete();

})();

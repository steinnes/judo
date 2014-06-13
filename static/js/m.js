(function(){
    var $ = jQuery;

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

    var countries = [];

    $('.countries li').each(function () {
        countries.push( $(this).text() );
      });

    $('#country').autocomplete({
        source: countries
    });


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

})();
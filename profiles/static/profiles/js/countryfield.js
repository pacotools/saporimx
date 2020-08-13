// Make the country field itself as well as all its options except for the first one black by default.
// Then I'll make the first option element the colour of the placeholder (grey)

// So I'll get the value of the country field when the page loads and store in a variable. The value will
// be an empty string if the first option is selected.  

let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});
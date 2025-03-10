(function($){
    $(document).ready(function(){
        const unitField = $('#id_unit');  // Unit field
        const courseField = $('#id_course');  // Course field
        
        // Trigger when unit field changes
        unitField.on('change', function() {
            const unitId = unitField.val();  // Get selected unit ID

            if (unitId) {
                // Make AJAX request to fetch the course for the selected unit
                $.ajax({
                    url: '/get_course_for_unit/' + unitId + '/',
                    method: 'GET',
                    success: function(response) {
                        if (response.course_id) {
                            courseField.val(response.course_id);  // Populate the course field
                        }
                    },
                    error: function() {
                        alert('Error fetching course for unit');
                    }
                });
            }
        });
    });
})(django.jQuery);

$( document ).ready(function() {
    var tmpImg = new Image();
    tmpImg.src= image_url;
    $(tmpImg).one('load',function(){
        //Prepare image editor parameters
        window.image_editor = window.image_editor || {};
        window.image_editor.border_width    = 1;
        window.image_editor.types           = types;
        window.image_editor.url             = image_url;
        window.image_editor.karnel_size     = karnel_size;
        window.image_editor.width           = tmpImg.width;
        window.image_editor.height          = tmpImg.height;
        window.image_editor.columns         = Math.floor(window.image_editor.width/window.image_editor.karnel_size);
        window.image_editor.rows            = Math.floor(window.image_editor.height/window.image_editor.karnel_size);
        window.image_editor.actual_width    = window.image_editor.columns * window.image_editor.karnel_size;
        window.image_editor.actual_height   = window.image_editor.rows * window.image_editor.karnel_size;
        window.image_editor.start_left      = (window.image_editor.width - window.image_editor.actual_width)/2;
        window.image_editor.start_top       = (window.image_editor.height - window.image_editor.actual_height)/2;
        window.image_editor.editor_width    = window.image_editor.actual_width + (window.image_editor.columns * 2 * window.image_editor.border_width);
        window.image_editor.editor_height   = window.image_editor.actual_height + (window.image_editor.rows * 2 * window.image_editor.border_width);

        //Update view
        $('.image-marker').css('width', window.image_editor.editor_width + 'px');
        $('.image-marker').css('height', window.image_editor.editor_height + 'px');
        $('.image-marker-control').css('width', window.image_editor.editor_width + 'px');
        $('.image-marker-instructions').css('width', window.image_editor.editor_width + 'px');

        for(r = 0; r < window.image_editor.rows; r++)
        for(c = 0; c < window.image_editor.columns; c++)
        {
            var x = (window.image_editor.start_left + (window.image_editor.karnel_size * c));
            var y = (window.image_editor.start_top + (window.image_editor.karnel_size * r));
            //Create the UI
            var fraction = document.createElement("div");
            fraction.id                         = 'fraction-' + c + '-' + r;
            fraction.style.width                = window.image_editor.karnel_size + 'px';
            fraction.style.height               = window.image_editor.karnel_size + 'px';
            fraction.style.backgroundImage      = "url('" + window.image_editor.url + "')";
            fraction.style.backgroundPositionX  = '-' + x + 'px';
            fraction.style.backgroundPositionY  = '-' + y + 'px';
            fraction.className                  = 'fraction';

            fraction.setAttribute('column', c);
            fraction.setAttribute('row', r);
            fraction.setAttribute('x', x);
            fraction.setAttribute('y', y);
            fraction.setAttribute('sequence', (r * window.image_editor.columns) + c);

            $('.image-marker').append(fraction);
        }

        $('.fraction').on('click', function(){
            $(this).toggleClass('selected');
        });

        window.image_editor.selection_types     = [];
        window.image_editor.current_selection   = 0;

        $.each(window.image_editor.types, function(key, value) {
            if(value) {
                window.image_editor.default_type = key;
            } else {
                window.image_editor.selection_types.push({'name' : key, 'default' : value, 'selection' : []});
            }
        });

        selectType(window.image_editor.selection_types[window.image_editor.current_selection]);        
    });

    function selectType(itemType) {
        txt = "<p>Please select the square with: <b>" + itemType.name + "</b></p>";
        $('.image-marker-instructions').html(txt);
        //Setup other configurations to keep track of the selections
    }
});
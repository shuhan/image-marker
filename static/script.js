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
        window.image_editor.marks           = {};

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
            var sequence = (r * window.image_editor.columns) + c;
            //Create the UI
            var fraction = document.createElement("div");
            fraction.id                         = 'fraction-' + c + '-' + r;
            fraction.style.width                = window.image_editor.karnel_size + 'px';
            fraction.style.height               = window.image_editor.karnel_size + 'px';
            fraction.style.backgroundImage      = "url('" + window.image_editor.url + "')";
            fraction.style.backgroundPositionX  = '-' + x + 'px';
            fraction.style.backgroundPositionY  = '-' + y + 'px';
            fraction.className                  = 'fraction sequence-' + sequence;

            fraction.setAttribute('column', c);
            fraction.setAttribute('row', r);
            fraction.setAttribute('x', x);
            fraction.setAttribute('y', y);
            fraction.setAttribute('sequence', sequence);

            window.image_editor.marks[sequence] = [];

            $('.image-marker').append(fraction);
        }

        /**
         *  Handle click on each image tiles
         */
        $('.fraction').on('click', function(){
            $(this).toggleClass('selected');

            var sequence = $(this).attr('sequence');

            if($(this).hasClass('selected')) {
                if(window.image_editor.marks[sequence].indexOf(window.image_editor.current_item.name) === -1) {
                    window.image_editor.marks[sequence].push(window.image_editor.current_item.name);
                }
            } else {
                if(window.image_editor.marks[sequence].indexOf(window.image_editor.current_item.name) !== -1) {
                    window.image_editor.marks[sequence].splice(window.image_editor.marks[sequence].indexOf(window.image_editor.current_item.name), 1 );
                }
            }
        });

        /**
         * Handle click on next
         */
        $('.marker-button.next').on('click', function() {
            window.image_editor.current_index++;
            if(window.image_editor.current_index > window.image_editor.selection_types.length - 1)
                window.image_editor.current_index = window.image_editor.selection_types.length - 1;
            selectType()
        });

        /**
         * Handle click on previous
         */
        $('.marker-button.previous').on('click', function() {
            window.image_editor.current_index--;
            if(window.image_editor.current_index < 0)
                window.image_editor.current_index = 0;
            selectType()
        });

        /**
         * Handle click on submit
         */
        $('.marker-button.submit').on('click', function() {
            //Set default value
            $.each(window.image_editor.marks, function(key, value) {
                if(value.length === 0)
                    window.image_editor.marks[key].push(window.image_editor.default_type);
            });

            window.image_editor.response = {
                'url'           : window.image_editor.url,
                'karnel_size'   : window.image_editor.karnel_size,
                'width'         : window.image_editor.width,
                'height'        : window.image_editor.height,
                'start_left'    : window.image_editor.start_left,
                'start_top'     : window.image_editor.start_top,
                'marks'         : window.image_editor.marks
            };

            $.ajax({
                type: "POST",
                url: '/submit',
                data: JSON.stringify(window.image_editor.response),
                contentType:"application/json; charset=utf-8",
                dataType:"json",
                success: function(data, textStatus, jqXHR) {
                    if(data['success']) {
                        image_url = data['image_url'];  //For now don't worry just refresh the page
                        location.reload();
                    } else {
                        alert(data['message']);
                        $('.marker-button.submit').prop("disabled", true);
                    }
                }
            });
        });

        window.image_editor.selection_types = [];
        window.image_editor.current_index   = 0;

        $.each(window.image_editor.types, function(key, value) {
            if(value) {
                window.image_editor.default_type = key;
            } else {
                window.image_editor.selection_types.push({'name' : key, 'default' : value});
            }
        });

        selectType();        
    });

    function selectType() {
        window.image_editor.current_item = window.image_editor.selection_types[window.image_editor.current_index];

        txt = "<p>Please select the square with: <b>" + window.image_editor.current_item.name + "</b></p>";
        $('.image-marker-instructions').html(txt);

        $('.fraction').removeClass('selected');

        $.each(window.image_editor.marks, function(key, value) {
            if(value.indexOf(window.image_editor.current_item.name) !== -1) {
                $('.fraction.sequence-' + key).addClass('selected');
            }
        });

        if(window.image_editor.current_index === 0) {
            if(!$('.marker-button.previous').hasClass('hidden'))
                $('.marker-button.previous').addClass('hidden');
        } else {
            if($('.marker-button.previous').hasClass('hidden'))
                $('.marker-button.previous').removeClass('hidden');
        }
        if(window.image_editor.current_index === window.image_editor.selection_types.length - 1) {
            if(!$('.marker-button.next').hasClass('hidden'))
                $('.marker-button.next').addClass('hidden');
            if($('.marker-button.submit').hasClass('hidden'))
                $('.marker-button.submit').removeClass('hidden');
        } else {
            if($('.marker-button.next').hasClass('hidden'))
                $('.marker-button.next').removeClass('hidden');
            if(!$('.marker-button.submit').hasClass('hidden'))
                $('.marker-button.submit').addClass('hidden');
        }
    }
});
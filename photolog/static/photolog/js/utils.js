$(document).ready(function() {
    // show/hide rotation icon.
    $('.photo').hover(
        function(){
            $(this).find('span.rotation').show();
        }, function(){
            $(this).find('span.rotation').hide();
        }
    );

    // edit photo's caption.
    $('span.edit-caption').click(function(){
        $(this).parent().find('.update-photo-caption').fadeIn('slow');
        $('input[type=submit]', $(this).parent().find('.update-photo-caption form')).removeAttr('disabled');
    });

    $('div.update-photo-caption form').submit(function(e){
        var $form = $(this);
        $('input[type=submit]', this).attr('disabled', 'disabled');

        $.ajax({
            url: '/update-photo-caption/',
            type: 'post',
            data: $form.serialize(),
            success: function(data) {
                if ( data == '1' ) {
                    alert('不能为空');
                } else if ( data == '2' ) {
                    alert('没有权限');
                } else {
                    $form.parent().parent().find('.photo-caption').html(data);
                }
                $('input[type=submit]', $form).removeAttr('disabled');
                $form.parent().fadeOut('slow');
            },
            error: function(requestObject, error, errorThrown) {
                alert("服务器错误！(" + error + ", " + errorThrown + ")");
                $('input[type=submit]', $form).removeAttr('disabled');
                $form.parent().fadeOut('slow');
            }
        });
        e.preventDefault();
    });

    $('.closeform').click(function(){
        $(this).parent().parent().fadeOut('slow');
    });

    // hide photo.
    $('span.hide-photo').click(function(){
        var $this = $(this);
        var id = $this.parent().attr('id').split('-')[1];
        var hidden = $this.hasClass('hidden') ? true : false;
        var confirm_text;
        if ( hidden ) {
            confirm_text = "是否显示这张照片？"
        } else {
            confirm_text = "是否隐藏这张照片？"
        }

        var do_act = function(){
            $this.hide();

            $.ajax({
                url: '/hide-photo/',
                type: 'post',
                data: {'id': id},
                success: function(data) {
                    if ( $this.hasClass('hidden') ) {
                        $this.removeClass('hidden');
                        $this.parent().find('.hiddenP').css({
                            'background': '#efefef url(/static/photolog/images/show.png) center center no-repeat',
                        });
                        $this.css({
                            'background-position': '0 0',
                        });
                        // $this.unbind('click');
                    } else {
                        $this.parent().html('<div class="hiddenP" style="width:'+$this.parent().width()+'px;">hidden</div>');
                    }
                }
            });
        };

        var dialog = $('<div id="confirm" title="请确认"><p>' + confirm_text + '</p></div>');
        dialog.dialog({
            autoOpen: false,
            modal: true,
            buttons : {
                "确认": function(){
                    $(this).dialog("close");
                    do_act();
                },
                "取消": function(){
                    $(this).dialog("close");
                }
            }
        });
        dialog.dialog("open");
    });

    // rotation photo.
    $('span.rotation').click(function(){
        var $this = $(this);

        var id = $(this).parent().attr('id').split('-')[1];
        var r = ( $this.hasClass('s-rotation') ) ? 's' : 'n';

        var confirm_text;
        if ( r == "s" ) {
            confirm_text = "是否将这张照片顺时针旋转90°？";
        } else {
            confirm_text = "是否将这张照片逆时针旋转90°？";
        }
        var do_act = function(){
            $this.hide();
            $.ajax({
                url: '/rotation-photo/',
                type: 'post',
                data: {
                    'id': id,
                    'r': r
                },
                success: function(data) {
                    var d = new Date();
                    var imgsrc = $('img', $this.parent()).attr("src");
                    if ( data == '1' ) {
                        setTimeout(function() {
                            $('img', $this.parent()).removeAttr("src").attr("src", imgsrc + "?v=" + d.getTime());
                        }, 1000);
                    }

                    $this.show();
                }
            });
        };

        var dialog = $('<div id="confirm" title="请确认"><p>' + confirm_text + '</p></div>');
        dialog.dialog({
            autoOpen: false,
            modal: true,
            buttons : {
                "确认": function(){
                    $(this).dialog("close");
                    do_act();
                },
                "取消": function(){
                    $(this).dialog("close");
                }
            }
        });
        dialog.dialog("open");
    });

    // post comment.
    $('#comments form').submit(function(e){
        var $form = $(this);
        $('input[type=submit]', this).attr('disabled', 'disabled');

        var ctype = $('#id_content_type', $form).val();
        var object_pk = $('#id_object_pk', $form).val();

        $.ajax({
            url: $form.attr('action'),
            type: 'post',
            data: $(this).serialize(),
            success: function(data) {
                var d = new Date();
                $.get( "/get-comments/", { 'ctype': ctype, 'object_pk': object_pk, 'key': d.getTime() }, function( data ) {
                    $('#cl').hide();
                    $('#cl').html(data);
                    $('#cl').show('slow');
                    $('input[type=submit]', $form).removeAttr('disabled');
                });
            }
        });

        e.preventDefault();
    });

});

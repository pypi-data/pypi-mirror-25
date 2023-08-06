!function($) {
  $.suggestionsDialog = function(options) {

    var title = 'Please check these possible duplicates:';
    var title_no_suggestions = 'Please check these possible duplicates:';
    var message = 'We have found a list of possible duplicates based on your title choice:';
    var message_no_suggestions = 'There are no suggestions for duplicate content based on the title';
    var text_data = $.ajax({
        url: $('base').attr('href').split('portal_factory')[0] + 'get_suggestions_text',
        type: 'get',
        async: false,
        dataType: 'json',
        success: function(data){
            if (data[0]){
                title = data[0];
            }
            if (data[1]){
                message = data[1];
            }
            if (data[2]){
                title_no_suggestions = data[2];
            }
            if (data[3]){
                message_no_suggestions = data[3];
            }
        }
    });
    var settings = {
      title : title,
      message: message,
      title_no_suggestions : title_no_suggestions,
      message_no_suggestions: message_no_suggestions,
      counter: 0,
      dialog_width: 383
    };

    $.extend(settings, options);

    var SuggestionsDialog = {
      setupDialog: function() {
        var self = this;
        //self.destroyDialog();

        var suggestions = Object.keys(options.suggestions).length;
        var current_title;
        var current_message;

        if (suggestions){
            current_title = settings.title;
            current_message = settings.message;
        } else {
            current_title = settings.title_no_suggestions;
            current_message = settings.message_no_suggestions;
        }
        var list = $('<ul/>');
        $.each(settings.suggestions, function(url, sugg){
            list.append($('<li/>')
                .append(
                    $('<a/>')
                        .attr('title', 'Similarity score: ' + sugg[4])
                        .attr('href', url).append(sugg[0])
                )
                .append($('<span>').attr('class', 'suggestion-details')
                    .append(' (similarity score: ' + sugg[4] + ')')
                )
                .append($('<div/>')
                    .attr('class', 'suggestion-details')
                    .append($('<span>')
                        .attr('class', 'portalType').text(sugg[1]))
                    .append($('<span>').attr('class', 'docDate creationDate')
                        .append(
                            $('<span>').attr('class', 'byline-separator')
                        )
                        .append('Created ' + sugg[2])
                    )
                    .append($('<span>').attr('class', 'docDate publishDate')
                        .append(
                            $('<span>').attr('class', 'byline-separator')
                        )
                        .append('Published ' + sugg[3])
                    )
                )
            );
        });
        var html = $('<div/>').attr('id', 'similarity-dialog')
                        .append($('<p/>').attr('id', 'similarity-message')
                            .append(current_message)
                        );
        html.append(list)
        .appendTo('body')
        .dialog({
          modal: false,
          width: settings.dialog_width,
          minHeight: 'auto',
          zIndex: 10000,
          closeOnEscape: true,
          draggable: false,
          resizable: false,
          dialogClass: 'similarity-dialog',
          title: current_title,
          show: {
                  effect: "fade",
                  duration: 1000
                },
          position: { my: "right top", at: "right bottom", of: window }
        });

      },

      destroyDialog: function() {
        if ($("#similarity-dialog").length) {
          $(this).dialog("close");
          $('#similarity-dialog').remove();
        }
      }

    };

    SuggestionsDialog.setupDialog();
  };
}(window.jQuery);


function suggestions_dialog(){
    var url = window.location.href;
    var portal_type = url.split('/')[url.split('/').indexOf('portal_factory')+1];
    title = $('#title').val();
    $('#similarity-dialog').remove();
    var suggestions = $.get(
        $('base').attr('href').split('portal_factory')[0] + 'get_suggestions',
        {'portal_type': portal_type, 'title': title},
        function(data){
            $.suggestionsDialog({
                'suggestions': data
            });
        },
        'json');
}


$().ready(function(){
    var title;
    $('body').on('focusin', '#title', function(){
      if(!$('#get-suggestions').length){
        $(this).parent().parent().parent().parent().parent().parent().css({
            'overflow': 'hidden'
        });
        $(this)
          .animate({width: '95%'}, 600)
          .parent().append(
            $('<a/>')
              .attr('id', 'get-suggestions')
              .attr('title', 'Get suggestions for similar items')
              .attr('href', 'javascript:void(0)')
              .text('\u2248')
              .css({
                'font-size': '26px',
                'position': 'absolute',
                'border': '1px solid #ccc',
                'width': '25px',
                'text-align': 'center',
                'border-left': 'none',
                'height': '35px',
                'line-height': '1',
                'border-top-right-radius': '5px',
                'border-bottom-right-radius': '5px',
                'display': 'none'
            })
            .append(
                $('<div>')
                    .text('Click to get suggestions for similar items')
                    .addClass('similarities-helper')
                    .css({
                        'padding': '.5rem',
                        'position': 'absolute',
                        'top': '-62px',
                        'right': '-15px',
                        'z-index': '9999',
                        'font-size': '12px',
                        'line-height': '1.2',
                        'width': '160px',
                        'background': 'white',
                        'box-shadow': '0px 0px 4px #ccc',
                        'border-radius': '5px'
                    })
                    .append(
                        $('<span>')
                            .text('\u25BC')
                            .css({
                              'content':'\u25BC',
                              'position':'absolute',
                              'left':'75%',
                              'width':'0',
                              'height':'0',
                              'color':'white',
                              'text-shadow':'0px 3px 2px #ccc',
                              'font-size':'2em',
                              'pointer-events':'none',
                              'top': '33px'
                            })
                    )
            )
          );
      }
      $('#get-suggestions').animate(
          {opacity: 'show'},
          {duration: 600,
           complete: function(){
              $('.similarities-helper').animate(
                  {opacity: 'show'},
                  {duration: 600,
                   complete: function(){
                      setTimeout(function(){
                          $('.similarities-helper').animate({opacity: 'hide'}, 600);
                      }, 5000);
                   }
                  }
              );
           }
          }
      );
//      $('#get-suggestions').animate({opacity: 'show'}, 600);
      title = $('#title').val();
    });
    var url = window.location.href;
    $("head").append($('<style>.similarities-helper:after {content:\u25BC; position:absolute; left:45%; width:0; height:0; color:white; text-shadow:0px 2px 3px #aaa; font-size:2em; pointer-events:none}</style>'));
    $('#title')
      .parent().append(
        $('<a/>')
            .attr('id', 'get-suggestions')
            .attr('title', 'Get suggestions for similar items')
            .attr('href', 'javascript:void(0)')
            .text('\u2248')
            .css({
              'font-size': '26px',
              'position': 'absolute',
              'border': '1px solid #ccc',
              'width': '22px',
              'text-align': 'center',
              'border-left': 'none',
              'height': '32px',
              'line-height': '1',
              'border-top-right-radius': '5px',
              'border-bottom-right-radius': '5px',
              'display': 'none'
            })
            .append(
                $('<div>')
                    .text('Click to get suggestions for similar items')
                    .addClass('similarities-helper')
                    .css({
                        'padding': '.5rem',
                        'position': 'absolute',
                        'top': '-62px',
                        'right': '-67px',
                        'z-index': '9999',
                        'font-size': '12px',
                        'line-height': '1.2',
                        'width': '160px',
                        'background': 'white',
                        'box-shadow': '0px 0px 4px #ccc',
                        'border-radius': '5px',
                        'display': 'none'
                    })
                    .append(
                        $('<span>')
                            .text('\u25BC')
                            .css({
                              'content':'\u25BC',
                              'position':'absolute',
                              'left':'45%',
                              'width':'0',
                              'height':'0',
                              'color':'white',
                              'text-shadow':'0px 3px 2px #ccc',
                              'font-size':'2em',
                              'pointer-events':'none',
                              'top': '33px'
                            })
                    )

            )
      );
    setTimeout(function(){
        $('#title')
          .animate({width: '96%'}, 600);
        $('#get-suggestions').animate(
            {opacity: 'show'},
            {duration: 600,
             complete: function(){
                $('.similarities-helper').animate(
                    {opacity: 'show'},
                    {duration: 600,
                     complete: function(){
                        setTimeout(function(){
                            $('.similarities-helper').animate({opacity: 'hide'}, 600);
                        }, 5000);
                     }
                    }
                );
             }
            }
        );
    }, 2000);

    $('body').on('click', '#get-suggestions', function(){
      title = $('#title').val();
      suggestions_dialog();
    });
    $('body').on('focusout', '#title', function(){
      if ($('#title').val() != title){
          suggestions_dialog();
      }
    });
});


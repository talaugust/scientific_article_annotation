  // https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }



  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });



  
  Annotator.Plugin.StoreLogger = function (element) {
  return {
    pluginInit: function () {
      this.annotator
          .subscribe("annotationCreated", function (annotation) {
            console.info(annotation)
            if ((annotation['text'] != null) && (annotation['text'].toUpperCase() == 'INT')){
              num_int_annotations += 1;
            }
            num_annotations += 1;
          })
          .subscribe("annotationUpdated", function (annotation) {
            console.info("The annotation: %o has just been updated!", annotation)
          })
          .subscribe("annotationDeleted", function (annotation) {
            console.info("The annotation: %o has just been deleted!", annotation)
            if ((annotation['text'] != null) && (annotation['text'].toUpperCase() == 'INT')){
              num_int_annotations -= 1
            }
            num_annotations -= 1;
          })
          .subscribe("annotationsLoaded", function(annotations) {
            console.log('Here')
            console.log(annotations)
          })
    }
  }
};

  var DEBUG = false; 
  // var content = $('#storyContainer').annotator();
  // var article_id = $('#storyContainer').data('id');
  var num_annotations = 0;
  var num_int_annotations = 0

  // content.annotator('addPlugin', 'Permissions');

  // content.annotator('addPlugin', 'Tags')


  // function for setting up an annotator
  var setupAnnotator = function(area, article_id, options){
  
    // https://2ality.com/2011/11/keyword-parameters.html
    if (options === undefined){
      options = {};
      search_user = undefined
      type_choice = undefined
      read_only =  false
      no_load = false
    } else{
      search_user = options.search_user
      type_choice = options.type_choice
      read_only =  options.read_only
      no_load = options.no_load
    }
  
    var content = $(area).annotator({
        readOnly: read_only
    });

    console.log(search_user, type_choice, read_only, no_load);
    content.annotator('addPlugin', 'StoreLogger');
    content.annotator('addPlugin', 'Tags');

    content.annotator('addPlugin', 'Store', {
      // The endpoint of the store on your server.
      prefix: '/api',

      // Attach the uri of the current page to all annotations to allow search.
      annotationData: {
        'uri': DEBUG? 'https://www.test.com':window.location.href,
        'article': article_id, 
      },
      urls: {
        // These are the default URLs.
        create:  '/annotations/',
        update:  '/annotations/:id/',
        destroy: '/annotations/:id',
        search:  '/annotations/'
      },
      // This will perform a "search" action when the plugin loads. Will
      // request the last 20 annotations for the current url.
      loadFromSearch: no_load? false: {
        'id': article_id,
        'limit': 100,
        'search_user':search_user,
        'annotation_type':type_choice,
      },
    });

    return content;
    
    };


    // TODO: SET TO INTEREST ANNOTATIONS SPECIFICALLY NOW
    $('#HIT-form').on('submit', function(e) {
      console.log(num_annotations);
      if (num_int_annotations < 1) {
        $('#annotationWarning').show();
        return false;
      } else {
        $('#annotationWarning').hide();
      }
      return true;
    })

  // $('#storyContainer').data('annotator').plugins['Permissions'].setUser("3");
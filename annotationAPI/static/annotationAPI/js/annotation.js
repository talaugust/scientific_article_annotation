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
            num_annotations += 1;
          })
          .subscribe("annotationUpdated", function (annotation) {
            console.info("The annotation: %o has just been updated!", annotation)
          })
          .subscribe("annotationDeleted", function (annotation) {
            console.info("The annotation: %o has just been deleted!", annotation)
            num_annotations -= 1;
          })
    }
  }
};

  var DEBUG = false; 
  var content = $('#storyContainer').annotator();
  var article_id = $('#storyContainer').data('id');
  var num_annotations = 0;

  // content.annotator('addPlugin', 'Permissions');
  // content.annotator('addPlugin', 'Tags')
  content.annotator('addPlugin', 'StoreLogger')
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
      loadFromSearch: {
        'id': DEBUG? 'https://www.test.com':article_id,
        'limit': 20,
      },
    });


    $('#HIT-form').on('submit', function(e) {
      console.log(num_annotations);
      if (num_annotations < 1) {
        $('#annotationWarning').show();
        return false;
      } else {
        $('#annotationWarning').hide();
      }
      return true;
    })

  // $('#storyContainer').data('annotator').plugins['Permissions'].setUser("3");
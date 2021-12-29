    // using jQuery
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


    $(".vote-up").on("click", function(ev) {
        console.log("test")
        const $this = $(this)
        const csrftoken = getCookie('csrftoken');    

        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            url: 'http://127.0.0.1:8000/vote/',
            data: { 'id': $this.data('id'), 'content':$this.data('cont') },
        })

        .done(function (msg) {
            span = document.querySelector("#qLikes")
            console.log("{{ question.get_likes }}")
            console.log((Number("{{ question.get_likes }}") + 1).toString(10))
            span.innerText = (Number("{{ question.get_likes }}") + 1).toString(10)
        })
    })


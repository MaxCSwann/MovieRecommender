$('.review_bar').autoResize();

$(document).ready(function() {
    $("#login-page-signup-modal").on('click',function() {
        $("#signup_modal").modal('show')
    });

    $("#login-form").submit(function(event) {
        email = $("#loginEmField")
        pw = $("#loginPwField")
        if (email.val().length <= 0 || pw.val().length <= 0) {
            event.preventDefault()
        }
    });

    $('#review-form').keypress(function(e) {
        if(e.which == 13) {
            jQuery(this).blur();
            jQuery('#review-button').focus().click();
        }
    });

    $("#review-form").submit(function(event){
        mov_id = $('input[name=movie-ID]').val();
        $.ajax({
            type:"POST",
            url:"/recommender/"+mov_id+"/",
            data: {
                'csrfmiddlewaretoken' : $('input[name=csrf_token]').val(),
                'text': $('#review-bar').val(),
            },
            success: function(data){
                //on success clear text input from bar and display reviews
                $('#review-bar').val('');
                updateReviews(data);

            },
            error: function(){
                console.log('error');
            }
        });
        return false;
    });
});

function updateReviews(reviews){
    let arr = JSON.parse(reviews);
    console.log(arr);
    $(".reviews").html(function(){
        htmlstr = "";
        for(review in arr){
        htmlstr += 
            '<div class = "col-12">\
                    <div class = "row single_review justify-content-center">\
                        <div class = "col-3 align-self-center">\
                            <img src="'+arr[review]['fields']['author'][1]+'" class="rounded" alt="Profile" width="40" height="40">\
                        </div>\
                        <div class = "col-9 align-self-center">\
                            <div class = "row review_text text-left">\
                                    <p>'+arr[review]['fields']['text']+'</p>\
                            </div>\
                            <div class = "row">\
                                <div class = "col-12 d-flex justify-content-start text-left review_details">\
                                    '+arr[review]['fields']['author'][0]+'\
                                    '+arr[review]['fields']['created_date']+'\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </a>\
            </div>';    
        }
        return htmlstr;
    });
}
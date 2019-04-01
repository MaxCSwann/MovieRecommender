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
               console.log(typeof data);

               //TODO:
               //Need way to show user data in updateReviews
               //atm author equals the author id
               //want to somehow query with id to get name and image
                updateReviews(data);

            },
            error: function(){
                console.log('error');
            }
        });
        return false;
    });

   /*$("#review-bar").addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
          // Cancel the default action, if needed
          event.preventDefault();
          // Trigger the button element with a click
          document.getElementById("#review-button").click();
        }
      });*/
});

//TODO: fix image not displaying
//author is the foreign key held by the review model
//this means that when we send back the jsonresponse
//we only have an int that represents our author
//we want to be able to get the user's profile and details 
//could potentially write a getMember view which returns a member given as an id
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
                            <img src="/images/'+arr[review]['fields']['author']+'/" class="rounded" alt="Profile" width="40" height="40">\
                        </div>\
                        <div class = "col-9 align-self-center">\
                            <div class = "row review_text">\
                                <div class = "col-12 d-flex justify-content-start text-left group_details">\
                                    <p>'+arr[review]['fields']['text']+'</p>\
                                </div>\
                            </div>\
                            <div class = "row">\
                                <div class = "col-12 d-flex justify-content-start text-left review_details">\
                                    '+arr[review]['fields']['author']+'\
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
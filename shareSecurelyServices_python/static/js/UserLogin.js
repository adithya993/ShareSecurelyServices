$("#newuserregistration").click(function(e) {
	/*alert("logic for registration submit")
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/SaveUserRecord",
        async:false,
        data: { 
        	email: $('[name="signup_email"]').val(), // < note use of 'this' here
        	fname: $('[name="signup_fname"]').val(),
        	lname: $('[name="signup_lname"]').val(),
        	pass: $('[name="signup_confirmpassword"]').val(),
        	groups: $('[name="signup_group"]').val().toString()
        },
        success: function(result) {
            alert('ok: ',result);
        },
        error: function(result) {
            alert('error');
        }
    });*/
});

$(".btn-list-users").click(function() {
	$(".form-signin").toggleClass("form-signin-left");
	$(".form-signup").toggleClass("form-signup-left");
	$(".frame").toggleClass("frame-long");
	$(".signup-inactive").toggleClass("signup-active");
	$(".signin-active").toggleClass("signin-inactive");
	$(".forgot").toggleClass("forgot-left");
	$(this).removeClass("idle").addClass("active");
});

$(".btn-signup").click(function() {
	$(".nav").toggleClass("nav-up");
	$(".form-signup-left").toggleClass("form-signup-down");
	$(".success").toggleClass("success-left");
	$(".frame").toggleClass("frame-short");
});


$(".btn-signin").click(function() {
	$(".btn-animate").toggleClass("btn-animate-grow");
	$(".welcome").toggleClass("welcome-left");
	$(".cover-photo").toggleClass("cover-photo-down");
	$(".frame").toggleClass("frame-short");
	$(".profile-photo").toggleClass("profile-photo-down");
	$(".btn-goback").toggleClass("btn-goback-up");
	$(".forgot").toggleClass("forgot-fade");
});

$("#signup_email").on({
    keydown: function(e) {
      if (e.which === 32)
        return false;
    },
    change: function() {
      this.value = this.value.replace(/\s/g, "");
    }
  });
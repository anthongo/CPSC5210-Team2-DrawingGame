$(window).on('load', () => setUp())

//https://www.freecodecamp.org/news/javascript-debounce-example/
//https://codepen.io/ondrabus/pen/WNGaVZN
function debounce(func, timeout = 100){
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}
const processChange = debounce(() => validateUsername())

function validateUsername(){
    let username =  $('#username')[0];
    username.reportValidity();
    if (!username.checkValidity()) return;
    let newUsername = username.value;
    $.get(window.location.origin+'/user/'+newUsername)
        .done(() => {
            $('#username').css("border", "2px solid red");
            $('#overlapAlert').text("Username already taken.")
                .css('visibility','visible')
                .toggleClass("alert-error", true)
                .toggleClass("alert-success", false)
        })
        .fail(() => { // No duplicate user exists
            $('#username').css("border", "2px solid green");
          $('#overlapAlert').text("Valid username.")
            .css('visibility','visible')
            .toggleClass("alert-error", false)
            .toggleClass("alert-success", true);

        });
}

function setUp(){
    // $('#username').click(editUsername);
    $('#editUsernameBtn').click(editUsername);
}

function editUsername(){
    let oldUser = $('#username').text();
    $('#username').replaceWith($(`<input type='text' id='username' 
      value='${$('#username').text()}' pattern='[a-zA-z0-9_]+'
      oninvalid="setCustomValidity('Username can only use letters, numbers, and underscores')"
        oninput="setCustomValidity('')">`));
    $('#username').change(processChange).keypress(function (e) {
        if (e.which == 13 && username.checkValidity()){ //Submit when pressing enter
            saveUsername(oldUser);
            return false;
        }
    })
    $('#editUsernameBtn').text("Save").off('click').click(() => saveUsername(oldUser));
}

function saveUsername(oldUser){
    let newUsername = $('#username').val();
    if (newUsername === oldUser){
        resetChanges(oldUser);
    }
    else {
        $.post(window.location.pathname, {"username": newUsername})
        .done( (msg) => window.location.href = "/user/"+newUsername)
        .fail( (xhr, status, error) => {
            resetChanges(oldUser);
        });
    }
}

function resetChanges(oldUser){
    $('#username').replaceWith(`<span id="username">${oldUser}</span>`)
    $('#editUsernameBtn').text("Edit").off('click').click(editUsername);
    $('#overlapAlert').css('visibility','hidden');
}
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const registerx = document.getElementById('registerx');
const signinx = document.getElementById('signinx');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
registerx.onclick = function(){
    const pwd2 = document.getElementById('password2').value;
    const pwd3 = document.getElementById('password3').value;
    if(pwd2 === pwd3){
        window.location.href = "home";
    }
    else{
        document.getElementById('error2').textContent = "Passwords don't Match";
    }
}
signinx.onclick = function(){
    const usr = document.getElementById('username1').value;
    const pwd1 = document.getElementById('password1').value;
    if(usr === `Siu` && pwd1 === `Nigga`){
        window.location.href = "home";
    }
    else{
        document.getElementById('username1').textContent = ``;
        document.getElementById('password1').textContent = ``;
        document.getElementById('error1').textContent = "Invalid Username or Password";
    }
}
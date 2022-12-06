// dom
const signInbtn = document.querySelector(".s_i_btn");
const signUpbtn = document.querySelector(".s_u_btn");
const signInPageBox = document.querySelector(".s_i_page_box");
const signUpPageBox = document.querySelector(".s_u_page_box");
const signInMsg = document.querySelector(".s_i_msg");
const signUpMsg = document.querySelector(".s_u_msg");
const signInUpLi = document.querySelector(".sign_in_up");
const signOutLi = document.querySelector(".sign_out");
const signPage = document.querySelector(".sign_page");

// input
const SUName = document.querySelector(".s_u_name");
const SUEmail = document.querySelector(".s_u_email");
const SUPwd = document.querySelector(".s_u_pwd");
const SIEmail = document.querySelector(".s_i_email");
const SIPwd = document.querySelector(".s_i_pwd");

// regex
const EmailPattern = /^\S+@\S+$/;
const PwdPattern = /^(?=.*\d)(?=.*[a-z])[0-9a-zA-Z]{2,}$/;

let signInkeyWait = true;
let signUpkeyWait = true;


/*  show signIn page  */
function showSignIn(){
  let pageBox = document.querySelector(".s_i_page_box");
  if(!signPage.classList.contains("sign_page_show")){
    signPage.classList.add("sign_page_show");
  }
  setTimeout(()=>{
    pageBox.classList.add("page_box_show");
  }, 150)
}

const inIcon = document.querySelector(".s_i_exit_icon");
inIcon.addEventListener("click", ()=>{
  fadeOut(".s_i_page_box", true)
})


function toggleSignIn(){
  showSignIn();
  fadeOut(".s_u_page_box", false);
}


/*  show signUp page  */
function showSignUp(){
  let pageBox = document.querySelector(".s_u_page_box");
  signPage.classList.add("sign_page_show");
  fadeOut(".s_i_page_box", false);
  setTimeout(()=>{
    pageBox.classList.add("page_box_show");
  }, 150)
}

const upIcon = document.querySelector(".s_u_exit_icon");
upIcon.addEventListener("click", function upExit(){
  fadeOut(".s_u_page_box", true)
})


/*  press X to exit  */
function fadeOut(boxClass, pressX){
  let pageBox = document.querySelector(boxClass);
  if(pressX){
    signPage.classList.remove("sign_page_show");
    setTimeout(()=>{
      SUName.value = "";
      SUEmail.value = "";
      SUPwd.value = "";
      SIEmail.value = "";
      SIPwd.value = "";
    }, 1000)
  }

  setTimeout(()=>{
    pageBox.classList.remove("page_box_show");
  }, 150)
}


/*  press enter to submit  */
document.addEventListener("keydown", (e)=>{
  let singInOpacity = getComputedStyle(signInPageBox).opacity;
  let singUpOpacity = getComputedStyle(signUpPageBox).opacity;

  if(signInkeyWait && singInOpacity){
    pressEnter(e, signIn, "signIn");
  }else if(signUpkeyWait && singUpOpacity){
    pressEnter(e, signUp, "signUp");
  }
})

function pressEnter(e, callback, status){
  if(e.key == "Enter" && signInkeyWait && status=="signIn"){
    callback();
    signInkeyWait = false;
    setTimeout(()=>{
      signInkeyWait = true;
    }, 2000)
  }
  if(e.key == "Enter" && signUpkeyWait && status=="signUp"){
    callback();
    signUpkeyWait = false;
    setTimeout(()=>{
      signUpkeyWait = true;
    }, 2000)
  }
}


/*  sign up  */
function signUp(){
  let validatedEmail = EmailPattern.test(SUEmail.value);
  let validatedPwd = PwdPattern.test(SUPwd.value);

  signUpbtn.style.pointerEvents = "none";

  if(!SUName.value){
    signUpMsg.textContent = "請輸入姓名";
    showMsg(signUpMsg, signUpbtn, false);
    return;
  }
  if(!validatedEmail){
    signUpMsg.textContent = "信箱格式錯誤";
    showMsg(signUpMsg, signUpbtn, false);
    return;
  }
  if(!validatedPwd){
    signUpMsg.textContent = "密碼格式錯誤";
    showMsg(signUpMsg, signUpbtn, false);
    return;
  }

  fetch("/api/user", {
    method: "post",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "name": SUName.value,
      "email": SUEmail.value,
      "password": SUPwd.value,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.error){
      signUpMsg.textContent = data.message;
      showMsg(signUpMsg, signUpbtn, false);
      return;
    }
    if(data.data){
      signUpMsg.textContent = "註冊成功";
      showMsg(signUpMsg, signUpbtn, true);
      SUName.value = "";
      SUEmail.value = "";
      SUPwd.value = "";
    }
  })
}


/*  sign in  */
function signIn(){
  let validatedEmail = EmailPattern.test(SIEmail.value);
  let validatedPwd = PwdPattern.test(SIPwd.value);

  signInbtn.style.pointerEvents = "none";

  if(!validatedEmail){
    signInMsg.textContent = "信箱格式錯誤";
    showMsg(signInMsg, signInbtn, false);
    return;
  }
  if(!validatedPwd){
    signInMsg.textContent = "密碼格式錯誤";
    showMsg(signInMsg, signInbtn, false);
    return;
  }

  fetch("/api/user/auth", {
    method: "put",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "email": SIEmail.value,
      "password": SIPwd.value,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.error){
      signInMsg.textContent = data.message;
      showMsg(signInMsg, signInbtn, false);
      return;
    }
    if(data.data){
      signInMsg.textContent = "登入成功";
      showMsg(signInMsg, signInbtn, true);
      SIEmail.value = "";
      SIPwd.value = "";
      auth(true);
    }
  })
}


function auth(needRefresh){
  fetch("/api/user/auth")
  .then((response) => response.json())
  .then((data) => {
    if(data.ok){
      signInUpLi.classList.add("li_out");
      signOutLi.classList.remove("li_out");
    }
    // if(data.error){

    // }
    if(needRefresh){
      history.go(0);
    }
  })
}

function signOut(){
  fetch("/api/user/auth", {
    method: "delete",
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.ok){
      history.go(0);
    }
  })
}



function showMsg(el, btn ,bool){
  if(bool){
    el.style.color = "rgb(20, 138, 73)";
  }else{
    el.style.color = "rgb(208, 35, 35)";
  }
  setTimeout(()=>{
    el.style.height = "20px";
    el.style.opacity = "1";
  }, 1)
  setTimeout(()=>{
    el.style.height = "0";
    el.style.opacity = "0";
    btn.style.pointerEvents = "auto";
  }, 2000)
}


function hideDisplayBug(){
  setTimeout(()=>{
    signPage.style.display = "block";
  },600)
}



export default {
  signIn,
  signUp,
  signOut,
  auth,
  showSignIn,
  showSignUp,
  toggleSignIn,
  hideDisplayBug,
}
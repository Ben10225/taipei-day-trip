import attr from "./attr_func.js"
import lib from "../lib/lib.js"


window.morningClick = attr.morningClick;
window.eveningClick = attr.eveningClick;

const id = window.location.href.split("/").pop();

window.showSignIn = lib.showSignIn;
window.showSignUp = lib.showSignUp;
window.toggleSignIn = lib.toggleSignIn;

window.signIn = lib.signIn;
window.signUp = lib.signUp;
window.signOut = lib.signOut;

lib.hideDisplayBug();
lib.auth(false);

attr.catchAttraction(id);



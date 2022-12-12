import attr from "./attr_func.js"
import nav from "../nav/nav_setting.js"

window.showSignIn = nav.showSignIn;
window.showSignUp = nav.showSignUp;
window.toggleSignIn = nav.toggleSignIn;

window.signIn = nav.signIn;
window.signUp = nav.signUp;
window.signOut = nav.signOut;
window.toBooking = nav.toBooking;


window.morningClick = attr.morningClick;
window.eveningClick = attr.eveningClick;
window.clickBtnOpen = attr.clickBtnOpen;

nav.hideDisplayBug();

(async()=>{
  await nav.auth(false);
  let bool = nav.signStatus();
  attr.signStatus(bool);
  await attr.getReserveData();
  attr.clickBtnOpenIfValue();
})()


const id = window.location.href.split("/").pop();

attr.setDateMixAndMax();
attr.catchAttraction(id);




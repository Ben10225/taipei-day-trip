import attr from "./index_func.js"
import lib from "../lib/lib.js"


window.keywordSelect = attr.keywordSelect;
window.showCategory = attr.showCategory;
window.showSignIn = lib.showSignIn;
window.showSignUp = lib.showSignUp;
window.toggleSignIn = lib.toggleSignIn;
window.signIn = lib.signIn;
window.signUp = lib.signUp;
window.signOut = lib.signOut;

lib.hideDisplayBug();
lib.auth(false);

attr.catchCategories();
attr.catchAttractions(attr.page);

attr.observer.observe(attr.target);

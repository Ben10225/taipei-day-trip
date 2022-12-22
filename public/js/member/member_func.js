const emailLabel = document.querySelector(".email_label");
const emailInput = document.querySelector(".email_input");
const nameLabel = document.querySelector(".name_label");
const nameInput = document.querySelector(".name_input");
const historyBox = document.querySelector(".history_box");
const details = document.querySelectorAll(".details");

const orders = document.querySelectorAll(".order");
const arrows = document.querySelectorAll(".arrow_down");
const arrowsIcon = document.querySelectorAll(".arrow_down i");
const attractionImages = document.querySelectorAll(".attraction_img");
const order_items = document.querySelectorAll(".order_item");


let originName = null;
let tempHeight = 0;
// let deg = 0;

const originHeight = historyBox.offsetHeight;
setHistoryBoxHeightAdd(0, 0);
attractionImageArrow();
orderItemInit();


function getHistoryOrders(){
  fetch("/api/history")
  .then((response) => response.json())
  .then((data) => {
    originName = nameInput.value;
    if(data.error){
      return;
    }
    if(data.data){
      createHistoryDOM(data.data);
    }
  })
}


function inputStyleInit(){
  emailInput.addEventListener("blur", ()=>{
    if(!emailInput.value){
      emailLabel.style = "left: 7px; top:24px; transition: 0.4s; font-size: 21px; color: #999;"
    }
  })
  emailInput.addEventListener("focus", ()=>{
    emailLabel.style = "left:8; top: 4; transition: 0.4s; font-size: 16px; color: #000;"
  })
  nameInput.addEventListener("blur", ()=>{
    if(!nameInput.value){
      nameLabel.style = "left: 7px; top:22px; transition: 0.4s; font-size: 21px; color: #999; background: transparent;"
    }
  })
  nameInput.addEventListener("focus", ()=>{
    nameLabel.style = "left:8; top: 4; transition: 0.4s; font-size: 16px; color: #444;"
  })
}


function createHistoryDOM(data){
  let html = "";
  data.forEach(element => {
    let txt = `
    <div class="order">
      <h3 class="order_number">${element.orderNumber}</h3>
      <h3 class="time">${element.time.slice(0,-3)}</h3>
      <div class="details">
      </div>
    </div>
    `;
    html += txt;
  });  
  historyBox.insertAdjacentHTML('beforeEnd', html);

  orders.forEach(order => {
    order.addEventListener("click", (e)=>{
      let orderNumber = order.children[0].textContent
      fetch(`/api/order/${orderNumber}`)
      .then((response) => response.json())
      .then((data) => {
        if(data.error){
          return;
        }
        if(data.data){
          console.log(data.data);
        }
      })
    })
  })
}


function changeUserName(){
  if(originName === nameInput.value || !nameInput.value){
    nameInput.style = "border: 1.2px solid rgb(206, 44, 44); box-shadow:0 0 15px #ed9e9e;"
      setTimeout(()=>{
        nameInput.style = "border: 1.2px solid rgba(#999, 0.5)"
      }, 1000)
    return
  }
  fetch("/api/history/name", {
    method: "post",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "name": nameInput.value,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.ok){
      nameInput.style = "border: 1.2px solid rgb(102, 190, 100); box-shadow:0 0 15px #9eeda1;"
      setTimeout(()=>{
        nameInput.style = "border: 1.2px solid rgba(#999, 0.5)"
      }, 1000)
      originName = nameInput.value;
      return;
    }
  })
}


function setHistoryBoxHeightAdd(height, index){
  let detailHeight = details[index].offsetHeight;
  historyBox.style = `height: ${detailHeight + height}px`
}

function setHistoryBoxHeightMinus(height, index){
  let detailHeight = details[index].offsetHeight;
  historyBox.style = `height: ${detailHeight - height +index*150}px`
}

function attractionImageArrow(){
  arrows.forEach((arrow, i) =>{
    let deg = 0;
    arrow.onclick = ()=>{
      if(attractionImages[i].classList.contains("attraction_img_hide")){
        setHistoryBoxHeightAdd(150+ Math.floor(i/2)*80, Math.floor(i/2));
        tempHeight += 150;
      }else{
        setHistoryBoxHeightMinus(150+ Math.floor(i/2)*80, Math.floor(i/2));
        tempHeight -= 150;
      }
      deg += 180;
      attractionImages[i].classList.toggle("attraction_img_hide");
      arrowsIcon[i*2].style = `transform: rotate(${deg}deg); transition: 0.4s;`;
      arrowsIcon[i*2+1].style = `transform: rotate(${deg}deg); transition: 0.4s;`;
      if(deg == 360){
        arrow.style = "pointer-events: none; opacity: 0.8;"
        setTimeout(()=>{
          arrowsIcon[i*2].style = `transform: rotate(0deg);`;
          arrowsIcon[i*2+1].style = `transform: rotate(0deg);`;
          arrow.style = "pointer-events: auto;"
        }, 500)
        deg = 0;
      }
    }
  })
}

function orderItemInit(){
  order_items.forEach((order, i)=>{
    order.onclick = ()=>{
      order.classList.toggle("active");
      details[i].classList.toggle("show");
      setHistoryBoxHeightAdd(80*i, i);
      arrowsIcon.forEach(icon=>{
        icon.style = `transform: rotate(0deg);`;
      })

      order_items.forEach((order, j)=>{
        if(j != i){
          order.classList.remove("active");
          details[j].classList.remove("show");
          attractionImageArrow();
          attractionImages[j*2].classList.add("attraction_img_hide");
          attractionImages[j*2+1].classList.add("attraction_img_hide");
        }
      })
      if(!order.classList.contains("active")){
        setHistoryBoxHeightMinus(0);
      }
    }
  })
}


export default {
  inputStyleInit,
  emailInput,
  nameInput,
  getHistoryOrders,
  createHistoryDOM,
  changeUserName,
}
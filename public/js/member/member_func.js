const emailLabel = document.querySelector(".email_label");
const emailInput = document.querySelector(".email_input");
const nameLabel = document.querySelector(".name_label");
const nameInput = document.querySelector(".name_input");
const historyBox = document.querySelector(".history_box");

let originName = null;

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

  const orders = document.querySelectorAll(".order");
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


export default {
  inputStyleInit,
  emailInput,
  nameInput,
  getHistoryOrders,
  createHistoryDOM,
  changeUserName,
}
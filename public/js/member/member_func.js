const emailLabel = document.querySelector(".email_label");
const emailInput = document.querySelector(".email_input");
const nameLabel = document.querySelector(".name_label");
const nameInput = document.querySelector(".name_input");
const historyBox = document.querySelector(".history_box");
const section = document.querySelector("section");
const details = document.querySelectorAll(".details");

const orders = document.querySelectorAll(".order");



let originName = null;
let tempHeight = 0;
let tempClick = null;
let ct =0;


// setHistoryBoxHeightAdd(0, 0);
// attractionImageArrow();
// orderItemInit();
// hideDetailsStart();


function getHistoryOrders(){
  fetch("/api/history")
  .then((response) => response.json())
  .then((data) => {
    originName = nameInput.value;
    if(data.error){
      return;
    }
    if(data.data){
      // console.log(data.data)
      createHistoryDOM(data.data);
      setHistoryBoxHeightAdd(0, null);
      attractionImageArrow();
      orderItemInit();
      hideDetailsStart();
    }
  })
}


function createHistoryDOM(data){
  let html = "";
  data.forEach((element, wholeIndex)=> {
    let attractions = "";
    element.trips.forEach((attr, i) => {
      attractions += `
      <h5 class="order_index">行程 <span>${i+1}</span></h5>
      <p>景點： ${attr.attraction_name}</p>
      <p>時間： ${attr.attraction_time}</p>
      <p>費用： NT <span class="price">${attr.attraction_price}</span>$</p>
      <p>地點： ${attr.attraction_address}</p>
      <div class="arrow_down" index="${wholeIndex}">
        <i class="fa-solid fa-chevron-down"></i>
        <i class="fa-solid fa-chevron-down"></i>
      </div>
      <div class="attraction_img attraction_img_hide" 
      style="background-image: url('${attr.attraction_image}');"></div>
      `;
      if(i != element.trips.length-1){
        attractions += "<hr>"
      }
    })

    let txt = `
    <div class="order">
      <div class="order_item">
        <h3 class="order_number">${element.orderNumber}</h3>
        <h3 class="time">${element.time.slice(0,-3)}</h3>
      </div>
      <div class="details">
        <div class="contact_info">
          <h5>訂單金額</h5>
          <p>總金額： NT <span class="total_price">${element.totalPrice}</span>$</p>
          <h5>聯絡人</h5>
          <p>姓名： ${element.contactName}</p>
          <p>信箱： ${element.contactEmail}</p>
          <p>電話： ${element.contactPhone}</p>
        </div>
        <hr class="big_hr">
        <div class="attraction_info">
          ${attractions}
        </div>
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
          // console.log(data.data);
        }
      })
    })
  })
}


function setHistoryBoxHeightAdd(height, index){
  if(index === null){
    historyBox.style = `${historyBox.offsetHeight}`
    return
  }
  let details = document.querySelectorAll(".details");

  let detailHeight = details[index].offsetHeight;
  historyBox.style = `height: ${detailHeight + height}px`

}

function setHistoryBoxHeightMinus(height, index){
  if(index === null){
    setTimeout(()=>{
      historyBox.style = `${historyBox.offsetHeight}`
    },700)
    return
  }
  let details = document.querySelectorAll(".details");

  let detailHeight = details[index].offsetHeight;
  historyBox.style = `height: ${detailHeight - height +index*150}px`

}

function attractionImageArrow(){
  const arrows = document.querySelectorAll(".arrow_down");
  const arrowsIcon = document.querySelectorAll(".arrow_down i");

  let attractionImages = document.querySelectorAll(".attraction_img");

  arrows.forEach((arrow, i) =>{
    let deg = 0;
    arrow.onclick = ()=>{
      let arrowWholeIndex = arrow.getAttribute("index");
      if(attractionImages[i].classList.contains("attraction_img_hide")){
        setHistoryBoxHeightAdd(150+ arrowWholeIndex*80, arrowWholeIndex);
        tempHeight += 150;
      }else{
        setHistoryBoxHeightMinus(150+ arrowWholeIndex*80, arrowWholeIndex);
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

  let arrowsIcon = document.querySelectorAll(".arrow_down i");
  let order_items = document.querySelectorAll(".order_item");
  let bigHr = document.querySelectorAll(".big_hr");
  let contactInfo = document.querySelectorAll(".contact_info");
  let attractionInfo = document.querySelectorAll(".attraction_info");
  let details = document.querySelectorAll(".details");

  // let attractionImages = document.querySelectorAll(".attraction_img");


  order_items.forEach((order, i)=>{
    order.onclick = ()=>{
      if(!section.classList.contains("move_left")){
        // section.classList.add("move_left");
        // historyBox.classList.add("move_left");
      }else{
        // setTimeout(()=>{
        //   section.classList.remove("move_left");
        //   historyBox.classList.remove("move_left");
        // }, 1200)
      }
      if(bigHr[i].classList.contains("hr_ani_out") && !order_items[i].classList.contains("active")){
        bigHr[i].classList.remove("hr_ani_out");
      }

      ct++ ;
      order.classList.toggle("active");
      if(!details[i].classList.contains("show")){
        details[i].style = "display: block;";

        section.classList.add("move_left");
        historyBox.classList.add("move_left");
      }else{
        setTimeout(()=>{
          details[i].style = "display: none;";
        }, 1500)

        setTimeout(()=>{
          section.classList.remove("move_left");
          historyBox.classList.remove("move_left");
        }, 1200)
      }
      details[i].classList.toggle("show");


      setTimeout(()=>{
        bigHr[i].classList.toggle("hr_ani");
      },100)

      setTimeout(()=>{
        contactInfo[i].classList.toggle("contact_info_show");
      }, 400)

      setTimeout(()=>{
        attractionInfo[i].classList.toggle("attraction_info_show");
      }, 700)

      setHistoryBoxHeightAdd(80*i, i);
      arrowsIcon.forEach(icon=>{
        icon.style = `transform: rotate(0deg);`;
      })

      if(ct > 1){
        if(tempClick !== i){
          details[tempClick].classList.toggle("show");
          order_items[tempClick].classList.toggle("active");
          contactInfo[tempClick].classList.remove("contact_info_show");
          attractionInfo[tempClick].classList.remove("attraction_info_show");
          bigHr[tempClick].classList.remove("hr_ani");

          let tempImgs = attractionInfo[tempClick].querySelectorAll(".attraction_img");
          tempImgs.forEach(img => {
            img.classList.add("attraction_img_hide");
          })
          tempClick = null;

        }else if(tempClick === i){
          bigHr[tempClick].classList.toggle("hr_ani_out");
          tempClick = null;
          ct = 0;
        }
      }
      if(!order.classList.contains("active")){
        setHistoryBoxHeightMinus(0, null);
      }
      order_items.forEach((it)=>{
        it.style = "pointer-events: none;";
        setTimeout(()=>{
          it.style = "pointer-events: auto;";
        }, 1500)
      })
      tempClick = i;
    }
  })
}


function hideDetailsStart(){
  // details.forEach(detail => {
  //   detail.style = "display: none";
  // })
  historyBox.style = "display: none";
  setTimeout(()=>{
    historyBox.style = "display: block";
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
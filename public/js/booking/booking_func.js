const bookingBox = document.querySelector(".booking_box")


function getBooking(){
  return fetch("/api/booking")
  .then((response) => response.json())
  .then((data) => {
    if(data.data){
      data.data.forEach((book, i)=> {
        createBookingDOM(book, i);
      });
      let hr = document.createElement("hr");
      bookingBox.appendChild(hr);
      let userName = document.querySelector(".user_name");
      userName.textContent = data.name;
    }
  })
}


function createBooking(id, date, time){
  let price;
  time === "morning" ? price = 2000 : price = 2500;
  fetch("/api/booking", {
    method: "post",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "attractionId": id,
      "date": date,
      "time": time,
      "price": price,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.ok){
      window.location.href = "/booking";
    }
    if(data.error){
      console.log(data.message);
    }
  })
}

function createBookingDOM(data, i){
  let bookingItem = document.createElement("div");
  bookingItem.className = "booking_item";
  bookingBox.appendChild(bookingItem);

  let img = document.createElement("div");
  img.className = "img";
  img.style.cssText = `background-image: url('${data.url}')`;

  let iconDelete = document.createElement("div");
  iconDelete.className = "icon_delete";

  let content =  document.createElement("div");
  content.className = "content";

  let el = document.querySelector(`.booking_item:nth-child(${i+2})`);
  el.appendChild(img);
  el.appendChild(iconDelete);
  el.appendChild(content);

  el = document.querySelector(`.booking_item:nth-child(${i+2}) > .content`);

  let h6 = document.createElement("h6");
  h6.textContent = "台北一日遊： ";
  let attractionName = document.createElement("span");
  attractionName.className = "attraction_name";
  attractionName.textContent = data.name;
  h6.appendChild(attractionName);

  let date = document.createElement("h5");
  date.textContent = "日期： ";
  let dateSpan = document.createElement("span");
  dateSpan.textContent = data.date;
  date.appendChild(dateSpan);

  let time = document.createElement("h5");
  time.textContent = "時間： ";
  let timeSpan = document.createElement("span");
  if(data.time === "morning"){
    timeSpan.textContent = "早上 7 點到下午 3 點";
  }else{
    timeSpan.textContent = "下午 1 點到晚上 9 點";
  }
  time.appendChild(timeSpan);

  let cost = document.createElement("h5");
  cost.textContent = "費用： ";
  let costSpan = document.createElement("span");
  costSpan.textContent = `新台幣 ${data.price} 元`;
  cost.appendChild(costSpan);

  let address = document.createElement("h5");
  address.textContent = "地點： ";
  let addressSpan = document.createElement("span");
  addressSpan.textContent = data.address;
  address.appendChild(addressSpan);

  el.appendChild(h6);
  el.appendChild(date);
  el.appendChild(time);
  el.appendChild(cost);
  el.appendChild(address);
}


export default {
  createBooking,
  getBooking,
}
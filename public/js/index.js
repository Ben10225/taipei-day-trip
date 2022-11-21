(function () {
  catchAttractions()
}());

function catchAttractions(){
  fetch("/api/attractions?page=0", {
    method: 'GET',
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.nextPage){
      for(let i=0;i<data.data.length;i++){
        createDOM(data, i)
      }
    }
  })
}


function createDOM(data, i){
  // 容器
  let attractionsGroup = document.querySelector(".attractions_group");
  // div attraction 
  let attraction = document.createElement('div');
  attraction.className= "attraction";
  attractionsGroup.appendChild(attraction);
  // div attraction_img 
  let attractionInside = document.querySelector(`.attraction:nth-child(${i+1})`);
  let attractionImg = document.createElement('div');
  attractionImg.className = "attraction_img";
  attractionImg.style.cssText = `background-image: url('${data.data[i].images[0]}')`;
  attractionInside.appendChild(attractionImg);
  // div attraction_name_group
  let attractionImgInside = document.querySelector(`.attraction:nth-child(${i+1}) .attraction_img`);
  let attractionNameGroup = document.createElement('div');
  attractionNameGroup.className = "attraction_name_group";
  attractionImgInside.appendChild(attractionNameGroup);
  // h6 attraction_name 
  let attractionNameGroupInside = document.querySelector(`.attraction:nth-child(${i+1}) .attraction_name_group`);
  let attractionName = document.createElement('h6');
  let nameNode = document.createTextNode(`${data.data[i].name}`);
  attractionName.appendChild(nameNode);
  attractionName.className = "attraction_name";
  attractionNameGroupInside.appendChild(attractionName);
  // div infos 
  let infos = document.createElement('div');
  infos.className = "infos";
  attractionInside.appendChild(infos);
  // h6 mrt_station category 
  let infosInside = document.querySelector(`.attraction:nth-child(${i+1}) > .infos`);
  let mrt_station = document.createElement('h6');
  let mrtNode = document.createTextNode(`${data.data[i].mrt}`);
  mrt_station.appendChild(mrtNode);
  mrt_station.className = "mrt_station";
  infosInside.appendChild(mrt_station);

  let category = document.createElement('h6');
  let categoryNode = document.createTextNode(`${data.data[i].category}`);
  category.appendChild(categoryNode);
  category.className = "category";
  infosInside.appendChild(category);
}
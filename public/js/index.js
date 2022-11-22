
let end;
let page = 0;
let ct = 0;
let sum = 0;
let keywordValue = "";

catchCategories();
catchAttractions(page);

// infiniteScroll
let options = {
  root: null,
  rootMargin: "50px 50px 50px 50px",
  threshold: 0.5,
}

let callback = (entries, observer) => {
  entries.forEach(entry => {
      ct ++;
      if(ct > 2){
        if(ct % 2 == 1){
          catchAttractions(page, keywordValue)
          observer.unobserve(target);
        }
      }
  })
}

let observer = new IntersectionObserver(callback, options)

const target = document.querySelector('.target')
observer.observe(target)




// fetch category
function catchCategories(){
  fetch("/api/categories", {
    method: 'GET',
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.data){
      let category_ul = document.querySelector(".category_ul");
      for(let i=0;i<data.data.length;i++){
        let li = document.createElement('li');
        let liNode = document.createTextNode(`${data.data[i]}`);
        li.appendChild(liNode);
        category_ul.appendChild(li);
        
        // add category btn listener
        li.addEventListener("click", ()=>{
          document.querySelector(".keyword").value = data.data[i];
        })
      }
    }
  })
}


function keywordSelect(){
  observer.unobserve(target);
  page = 0;
  sum = 0;
  let keyword = document.querySelector(".keyword");
  let attractionsGroup = document.querySelector(".attractions_group");
  attractionsGroup.replaceChildren();
  keywordValue = keyword.value;
  catchAttractions(page, keywordValue);
}


function showCategory(){
  let category_box = document.querySelector(".category_box");
  category_box.style.display = "block";
  setTimeout(() => {
    category_box.style.visibility = "visible";
    category_box.style.opacity = "1";
    category_box.style.transform = "translateY(3px)";
  },1)
  let wrapper = document.querySelector(".wrapper");
  let category_ul = document.querySelector(".category_ul");

  setTimeout(() => {
    wrapper.addEventListener("click", function out(e){
      if (!category_ul.contains(e.target)) {
        categoryOut(category_box, wrapper, out)
        return
      }
      let category_lis = document.querySelectorAll(".category_ul li");
      for(let i of category_lis){
        if(i.contains(e.target)){
          categoryOut(category_box, wrapper, out)
        }
      }
    })
  },300)
}

function categoryOut(dom, outter, lintener){
  dom.style.visibility = "hidden";
  dom.style.opacity = "0";
  dom.style.transform = "translateY(-3px)";
  outter.removeEventListener("click", lintener);
}

// fetch page
async function catchAttractions(pg, keyword){
  let url
  if(keyword){
    url = `/api/attractions?page=${pg}&keyword=${keyword}`
  }else{
    url = `/api/attractions?page=${pg}`
  }
  await fetch(url, {
    method: 'GET',
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.error){
      createError(data.message);
      return;
    }
    if(data.nextPage){
      for(let i=0;i<data.data.length;i++){
        // console.log(data.data[i].images)
        createDOM(data, i, page * data.data.length + i);
      }
      page = data.nextPage;
      sum += data.data.length;
      observer.unobserve(target);
      setTimeout(() => {
        observer.observe(target);
      }, 500);
    }else{
      for(let i=0;i<data.data.length;i++){
        createDOM(data, i, sum + i);
      }
      end = true;
      observer.unobserve(target);
      return;
    }
  })
}


// appendChild
function createDOM(data, i, index){
  // 容器
  let attractionsGroup = document.querySelector(".attractions_group");
  // div attraction 
  let attraction = document.createElement('div');
  attraction.className= "attraction";
  attractionsGroup.appendChild(attraction);
  // div attraction_img 
  let attractionInside = document.querySelector(`.attraction:nth-child(${index+1})`);
  let attractionImg = document.createElement('div');
  attractionImg.className = "attraction_img";
  attractionImg.style.cssText = `background-image: url('${data.data[i].images[0]}')`;
  attractionInside.appendChild(attractionImg);
  // div attraction_name_group
  let attractionImgInside = document.querySelector(`.attraction:nth-child(${index+1}) .attraction_img`);
  let attractionNameGroup = document.createElement('div');
  attractionNameGroup.className = "attraction_name_group";
  attractionImgInside.appendChild(attractionNameGroup);
  // h6 attraction_name 
  let attractionNameGroupInside = document.querySelector(`.attraction:nth-child(${index+1}) .attraction_name_group`);
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
  let infosInside = document.querySelector(`.attraction:nth-child(${index+1}) > .infos`);
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


function createError(err){
  let attractionsGroup = document.querySelector(".attractions_group");
  let errMsg = document.createElement('h2');
  let errNode = document.createTextNode(err);
  errMsg.appendChild(errNode);
  errMsg.className= "error_message";
  attractionsGroup.appendChild(errMsg);
}
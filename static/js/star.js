let stars = document.getElementsByClassName("select-rating");
let rating = document.getElementById("rating");
rating.value=0
stars[0].addEventListener("click", function(e){
    for (let index = 0; index < stars.length; index++) {
        if (index == 0){
            stars[index].classList.add("fas")
            stars[index].classList.remove("far")
        }else{
            stars[index].classList.add("far")
            stars[index].classList.remove("fas")
        }    
    }
    rating.value = 1;
})
stars[1].addEventListener("click", function(e){
    for (let index = 0; index < stars.length; index++) {
        if (index <= 1){
            stars[index].classList.add("fas")
            stars[index].classList.remove("far")
        }else{
            stars[index].classList.add("far")
            stars[index].classList.remove("fas")
        }
    }
    rating.value = 2;
})
stars[2].addEventListener("click", function(e){
    for (let index = 0; index < stars.length; index++) {
        if (index <= 2){
            stars[index].classList.add("fas")
            stars[index].classList.remove("far")
        }else{
            stars[index].classList.add("far")
            stars[index].classList.remove("fas")
        }
    }
    rating.value = 3;
})
stars[3].addEventListener("click", function(e){
    for (let index = 0; index < stars.length; index++) {
        if (index <= 3){
            stars[index].classList.add("fas")
            stars[index].classList.remove("far")
        }else{
            stars[index].classList.add("far")
            stars[index].classList.remove("fas")
        }
    }
    rating.value = 4;
})
stars[4].addEventListener("click", function(e){
    for (let index = 0; index < stars.length; index++) {
        if (index <= 4){
            stars[index].classList.add("fas")
            stars[index].classList.remove("far")
        }else{
            stars[index].classList.add("far")
            stars[index].classList.remove("fas")
        }
    }
    rating.value = 5;
})



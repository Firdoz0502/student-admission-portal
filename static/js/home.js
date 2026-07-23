// Mobile Menu

const menu=document.querySelector(".menu-toggle");
const nav=document.querySelector(".nav-links");

menu.onclick=()=>{

nav.classList.toggle("active");

};

// Hero Animation

window.onload=()=>{

document.querySelector(".hero").classList.add("show");

};

// Counter

const counters=document.querySelectorAll(".counter");

const speed=50;

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

counters.forEach(counter=>{

const update=()=>{

const target=+counter.dataset.target;

const count=+counter.innerText;

const inc=Math.ceil(target/speed);

if(count<target){

counter.innerText=count+inc;

setTimeout(update,30);

}

else{

counter.innerText=target+"+";

}

};

update();

});

}

});

});

observer.observe(document.querySelector(".stats"));

// Dark Mode

const dark=document.getElementById("darkToggle");

dark.onclick=()=>{

document.body.classList.toggle("dark");

};

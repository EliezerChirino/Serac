
document.addEventListener("keyup", e=>{

    if (e.target.matches("#buscador")){
        document.querySelectorAll(".card-header").forEach(nombre=>{

            nombre.textContent.toLowerCase().includes(e.target.value.toLowerCase())
            ?nombre.classList.remove("filter")
                :document.getElementById("grupo").classList.add(filter); 
                //nombre.classList.add("filter")

        })
    }
})


//const d = document

/*d.addEventListener("keyup", (e)=>{
    if(e.target.matches("#buscador")){
        console.log(e.target.value);
        d.querySelectorAll(".card-header").forEach(el=> el.textContent.toLocaleLowerCase().includes(e.target.value)
        ?el.classlist.remove("filter")
        :el.classList.add(filter)
        );
        
    }
});*/
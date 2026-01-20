document.addEventListener("DOMContentLoaded",()=>{

    document.getElementById("form-skills").onsubmit = () =>{
        const user_skill = document.querySelector("#text-skills").value;
        console.log(user_skill);
        document.querySelector("#text-skills").value = "";
        skillsUpdate(user_skill);
        return false;
    };

    document.getElementById("list-skill").addEventListener("click",(e)=>{
        if(e.target.classList.contains("delete-btn")){
            delete_skill(e.target.dataset.id);
            return false;
        }

    });


});

function skillsUpdate(user_skill){

    const CSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new XMLHttpRequest();
    request.open("POST","skill-update");
    request.setRequestHeader("X-CSRFToken",CSRFToken);
    request.onload = () =>{

        const data = JSON.parse(request.responseText);
        if(data.success){
            const ul = document.getElementById("list-skill");
            ul.innerHTML = "";
            data.skills.forEach(skill=>{
                    const li = document.createElement("li");
                    li.classList.add("list-group-item","ms-2","mt-2",
                        "shadow","shadow-sm","rounded");

                    const span = document.createElement("span");
                    span.textContent = skill.name;

                    const button = document.createElement("button");
                    button.style.fontSize = "7px";
                    button.style.marginLeft = "4px";
                    button.classList.add("btn","btn-close","btn-dark","delete-btn");
                    button.dataset.id = skill.id;

                    li.append(span);
                    li.append(button);
                    ul.append(li);
             });
               
        } else{
            document.querySelector(".modal-body").innerHTML = "You've already added this skill";
            const modal = new bootstrap.Modal(document.getElementById("exampleModal"));
            modal.show();
        }

    };
    const formData = new FormData();
    formData.append("skills",user_skill);
    request.send(formData);
}

const delete_skill = (id) =>{

    const CSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new XMLHttpRequest();
    request.open("POST","skill-delete");
    request.setRequestHeader("X-CSRFToken",CSRFToken);
    request.onload = () =>{

        const data = JSON.parse(request.responseText);
        if(data.success){
            
            const ul = document.getElementById("list-skill");
            ul.innerHTML = "";

            data.skills.forEach(skill=>{

                const li = document.createElement("li");
                li.classList.add("list-group-item","ms-2","mt-2",
                    "shadow","shadow-sm","rounded");


                const span = document.createElement("span");
                span.textContent = skill.name;

                const button = document.createElement("button");
                button.style.fontSize = "7px";
                button.style.marginLeft = "4px";
                button.classList.add("btn","btn-close", "btn-dark","delete-btn");
                button.dataset.id = skill.id;

                li.append(span);
                li.append(button);
                ul.append(li);

            });    
            
        } else{
            document.querySelector(".modal-body").innerHTML = "Unable to delete skill";
            const modal = new bootstrap.Modal(document.getElementById("exampleModal"));
            modal.show();
        }
            
           
    };
    const formData = new FormData();
    formData.append("skill_id",id);
    request.send(formData);

}
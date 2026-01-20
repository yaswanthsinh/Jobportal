document.addEventListener("DOMContentLoaded",()=>{

    document.querySelectorAll("#see-more").forEach(btn=>{
        btn.onclick = () =>{
            hideout(btn.dataset.id,btn);
        };
    });

    document.querySelectorAll("#apply_button").forEach( btn=>{
        btn.onclick = () =>{
            console.log(btn.dataset.job_id);
            apply_for_job(btn.dataset.job_id);
            return false;
        };

    }); 

});

const hideout = (id,btn) =>{

    const content = document.querySelector(`#more-${id}`);
    if(content.style.display === "none"){
        content.style.display = "block";
        btn.textContent = "see less";
        btn.classList.remove("btn-warning");
        btn.classList.add("btn-info");
    }else{
        content.style.display = "none";
        btn.textContent = "see more";
         btn.classList.remove("btn-info");
        btn.classList.add("btn-warning");
    }

};

const apply_for_job = (id) =>{
    
    const CSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new XMLHttpRequest();
    request.open("POST","apply-for-job");
    request.setRequestHeader("X-CSRFToken",CSRFToken);
    request.onload = () =>{

        const data = JSON.parse(request.responseText);
        if(data.status){
            document.querySelector(".modal-body").innerHTML = data.message;
        }else{
            document.querySelector(".modal-body").innerHTML = data.message;
        }
        const modal = new bootstrap.Modal(document.getElementById('exampleModal'));
        modal.show();
    };
    const formData = new FormData();
    formData.append("job_id",id);
    request.send(formData);

};



document.addEventListener("DOMContentLoaded",()=>{

    document.getElementById("form-experience").onsubmit = () =>{

        const experience = document.getElementById("user_experience").value;
        console.log(experience);
        document.getElementById("user_experience").value = "";
        UpdateExperience(experience);
        return false;
    };

});

const UpdateExperience = (experience) =>{

    const CSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new XMLHttpRequest();
    request.open("POST","exp-update");
    request.setRequestHeader("X-CSRFToken",CSRFToken);
    request.onload = () =>{

        const data = JSON.parse(request.responseText);
        if(data.status){
            document.querySelector("#exp").innerHTML = data.experience;
        }
    };

    const formData = new FormData();
    formData.append("experience",experience);
    request.send(formData);
}
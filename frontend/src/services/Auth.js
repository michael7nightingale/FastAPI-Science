import {meUser} from "@/services/UserService";

export function setUser(token){
    localStorage.user = token;
    meUser().then(response => {
        localStorage.userData = JSON.stringify(response.data);
    })

}



export function getHeaders(){
    let user = localStorage.user;
    let headers = {};
    if (user){
        headers['Authorization'] = `Token ${user}`;
    }
    return headers
}


export function logoutUser(){
    localStorage.removeItem("user");
    localStorage.removeItem("userData")
}

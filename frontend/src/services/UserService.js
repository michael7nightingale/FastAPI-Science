import axios from 'axios';


export function loginUser(username, password){
    let data = {
        username: username,
        password: password
    }

    let promise = axios.post(
         'http://localhost:8001/api/v1/auth/token/',
        data
    )
    return promise.then(response => response.data);
}



export function registerUser(email, username, password){
    let data = {
        email: email,
        username: username,
        password: password
    }
         let promise = axios.post(
         'http://localhost:8001/api/v1/auth/register/',
        data,{
             validateStatus: (status) => Boolean(status)
             }
         ).catch(
            function (){
                  alert("Data is invalid!")
            }
        );
        return promise.then(response => response.data);

}



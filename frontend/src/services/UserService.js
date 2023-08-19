import axios from 'axios';
import {getHeaders} from "@/services/Auth";
import {buildUrl} from "@/services/Base";


export function loginUser(username, password){
    let data = {
        username: username,
        password: password
    }
    return axios.post(
         buildUrl('auth/token/'),
        data
    )
}



export function registerUser(email, username, password){
    let data = {
        email: email,
        username: username,
        password: password
    }
    return axios.post(
        buildUrl('auth/register/'),
        data
    )

}


export function meUser(){
    return axios.get(
        buildUrl('auth/me/'),
        {
            headers: getHeaders()
        }
    )

}

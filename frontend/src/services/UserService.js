import axios from 'axios';
import {getHeaders} from "@/services/Auth";
import {buildUrl} from "@/services/Base";


export function loginUser(login, password){
    let data = {
        login: login,
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


export function getOauthProviderUrl(providerName){
    return axios.get(
        buildUrl(`auth/${providerName}/login`),
    )
}


export function getOauthCallbackToken(providerName, code){
    return axios.get(
        buildUrl(`auth/${providerName}/callback`),
        {
            params: {code: code}
        }
    )
}


export function activateUser(code){
    return axios.patch(
        buildUrl("auth/activation"),
        {code: code},
    )
}

import {buildUrl} from "@/services/Base";
// import {getHeaders} from "@/services/Auth";
import axios from "axios";
import {getHeaders} from "@/services/Auth";


export function getProblemsList(){
    return axios.get(buildUrl("problems/all"));
}


export function createProblem(data){
    return axios.post(
        buildUrl("problems/create"),
        data,
        {
            headers: getHeaders()
        }
    );
}


export function getProblem(problemId){
    return axios.get(buildUrl(`problems/detail/${problemId}`));
}


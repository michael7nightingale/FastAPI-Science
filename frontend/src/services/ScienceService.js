import axios from 'axios';
import {getHeaders} from "@/services/Auth";
import {buildUrl} from "@/services/Base";


function getScienceList(){
    let promise = axios.get(
        buildUrl('sciences/'),
         {
             headers: getHeaders()
         }
         );

    return promise.then((response) => response.data);
}

export function getScienceDetail(slug){
     let promise = axios.get(
         buildUrl(`sciences/science/${slug}`),
         {
             headers: getHeaders()
         }
         );
     return promise.then(response => response.data);
}

export function getCategoryDetail(slug){
     let promise = axios.get(
         buildUrl(`sciences/category/${slug}`),
         {
             headers: getHeaders()
         }
         );
     return promise.then(response => response.data);
}


export function getSpecialCategoryDetail(slug){
     let promise = axios.get(
         buildUrl(`sciences/special-category/${slug}`),
         {
             headers: getHeaders()
         }
         );
     return promise.then(response => response.data);
}


export function getFormulaDetail(slug){
     let promise = axios.get(
         buildUrl(`sciences/formula/${slug}`),
         {
             headers: getHeaders()
         }
         );
     return promise.then(response => response.data);
}


export function countResult(slug, storage, numsComma, findMark){
    let data = {
        data: storage,
        numsComma: parseInt(numsComma),
        findMark: findMark
    };
    let promise = axios.post(
        buildUrl(`sciences/formula/${slug}`),
        data,
        {
             headers: getHeaders()
         }
    );
    return promise.then(response => response.data);
}


export function postPlot(storage){
    let promise = axios.post(
        buildUrl(`sciences/special-category/plots`),
        storage,
        {
             headers: getHeaders()
         }
    );
    return promise.then(response => response.data);
}


export function downloadPlot(filename){
    let data = {filename: filename};
    return axios.post(
        buildUrl(`sciences/special-category/plots/download`),
        data,
        {
             headers: getHeaders(),
            responseType: "blob"
         }
    );
}

// function getCategoryList(scienceSlug){
//     let promise = axios.get(`http://localhost:8001/api/v1/sciences/category/${scienceSlug}`);
//     return promise.then((response) => response.data);
// }


export {
    getScienceList,

}
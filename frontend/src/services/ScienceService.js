import axios from 'axios';


function getScienceList(){
    let promise = axios.get('http://localhost:8001/api/v1/sciences/');
    return promise.then((response) => response.data);
}

export function getScienceDetail(slug){
     let promise = axios.get(`http://localhost:8001/api/v1/sciences/science/${slug}`);
     return promise.then(response => response.data);
}

export function getCategoryDetail(slug){
     let promise = axios.get(`http://localhost:8001/api/v1/sciences/category/${slug}`);
     return promise.then(response => response.data);
}

export function getFormulaDetail(slug){
     let promise = axios.get(`http://localhost:8001/api/v1/sciences/formula/${slug}`);
     return promise.then(response => response.data);
}


export function countResult(slug, storage, numsComma, findMark){
    let data = {
        data: storage,
        numsComma: parseInt(numsComma),
        findMark: findMark
    };
    let promise = axios.post(
        `http://localhost:8001/api/v1/sciences/formula/${slug}`,
        data
    );
    return promise.then(response => response.data);
}


// function getCategoryList(scienceSlug){
//     let promise = axios.get(`http://localhost:8001/api/v1/sciences/category/${scienceSlug}`);
//     return promise.then((response) => response.data);
// }

export {
    getScienceList,

}
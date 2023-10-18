let baseUrl = 'http://localhost:1337/api/v1/'

export function buildUrl(path){
    return baseUrl.concat(path);
}

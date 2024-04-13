const baseUrl = 'https://ping.astrum.studio/api/'
const staticUrl = 'https://ping.astrum.studio/static/'


export function buildStaticUrl(path){
    return staticUrl.concat(path);
}


export function buildUrl(path){
    return baseUrl.concat(path);
}

import {buildUrl} from "@/services/Base";
import {getHeaders} from "@/services/Auth";
import axios from "axios";


export function getHistoryList() {
    return axios
        .get(
            buildUrl("cabinet/history"),
            {
                headers: getHeaders()
            }
        );

}


export function deleteHistory() {
      return axios
        .delete(
            buildUrl("cabinet/history"),
            {
                headers: getHeaders()
            }
        );
}


export function downloadHistory(filename, extension){
    let data = {
        filename: filename,
        extension: extension
    }
    return axios
        .post(
            buildUrl("cabinet/history/download"),
            data,
            {
                headers: getHeaders(),
                responseType: "blob"
            }
        )

}

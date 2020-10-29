export default function getErrMsg(error) {
    if (error.response) {
        if (error.response.status == 422) {
            const detail = error.response.data.detail;
            return `${detail[0].loc[1]}: ${detail[0].msg}`
        } 
        if (error.response.status == 403) {
            return error.response.data.detail
        }
    }
    return ''
}
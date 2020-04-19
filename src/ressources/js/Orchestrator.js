class Orchestrator {
    constructor() {
        this.serverUrl = "http://localhost:80";
    }

    makeAjaxCall(url, methodType) {
        return new Promise(function (resolve, reject) {
            let xhr = new XMLHttpRequest();
            xhr.open(methodType, url, true);
            xhr.send();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        console.log("xhr done successfully");
                        let resp = xhr.responseText;
                        console.log("data ajax", resp)
                        let respJson = JSON.parse(resp);
                        resolve(respJson);
                    } else {
                        reject(xhr.status);
                        console.log("xhr failed");
                    }
                } else {
                    console.log("xhr processing going on");
                }
            };
            console.log("request sent succesfully");
        });
    }

    get_data(route, params, callback) {

        /* Pipeline :
            - Launch treatment and save id_job
                -> while result unavailable : retry get result
            - Callback to write result
        */
        const complete_route = new Routes(this.serverUrl.concat('/', route), params).get_route();
        this.launch_treatment(complete_route)
            .then(result => this.check_result(result))
            .then(result => callback(result));
    }

    launch_treatment(url){
        return new Promise(function (resolve, reject) {
            this.makeAjaxCall(url, "GET").then( function (dict_result) {
                console.log("h", dict_result)
                resolve(dict_result["id_job"]);
            });
        }.bind(this));
    }

    get_job_result(id_job) {
        console.log("start job_result, id_job=" + id_job);
        const complete_route = new Routes(this.serverUrl.concat('/job/result?id=', id_job)).get_route();
        return new Promise(function (resolve, reject) {
            this.makeAjaxCall(complete_route, "GET").then(function (ajax_result) {
                resolve(ajax_result[id_job])
            })
        }.bind(this));
    }

    check_result(id_job) {
        return this.get_job_result(id_job).then(function(result) {
            if (result === "Started") {
                 // run the operation again
                 return this.check_result(id_job);
            } else {
                console.log("fin", result)
                return result;
            }
        }.bind(this));
    }


        /*if (ajax_result[id_job] !== undefined){
                    if (ajax_result[id_job] !== "Started"){

                        // Job finish
                        resolve(ajax_result[id_job])

                    }else {
                        // Job not finish
                        setTimeout(function () { reject(id_job); }, 1000);
                    }
                }else{
                    console.log("job didn't start")
                    resolve("ERROR SERVER JOB NOT FOUND")
                }

            });*/


}
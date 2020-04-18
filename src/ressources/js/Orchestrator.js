class Orchestrator {
    constructor() {
        this.ServeurUrl = "http://localhost:80";
    }

    ajax_request(route, callback) {
        let response = '';
        let xhr = new XMLHttpRequest();
        if (!xhr) {
            console.log('Abandon :( Impossible de créer une instance de XMLHTTP');
            return false;
        }
        xhr.onreadystatechange = function () {
            try {
                if (this.readyState === XMLHttpRequest.DONE) {
                    if (this.status === 200) {
                        console.log('SERVER REPLY IS OK');
                        response = this.responseText;
                        console.log(response);
                        callback(JSON.parse(response));
                    } else {
                        console.log('SERVER REPLY IS NOT OK'.concat(' erreur : ', this.responseText));
                    }
                } else {
                    console.log('SERVER REPLY IS NOT YET READY...')
                }
            } catch (e) {
                alert("Une exception s’est produite : " + e.description);
            }
            return response;
        };
        xhr.open('GET', route);
        xhr.send();
        return xhr.onreadystatechange;
    }

    get_data(route, params, callback){
        const complete_route = new Routes(this.ServeurUrl.concat('/', route), params);
        let id_job = this.ajax_request(complete_route, {
            (e) =>
        });
        console.log(id_job);
        //GET ID_JOB
        //check result is ready
        //
    }
}
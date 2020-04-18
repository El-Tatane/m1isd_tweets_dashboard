class Routes {
    constructor(url, values) {
        this.url = url;
        this.values = values;
    }

    get_route() {
        let route = this.url;
        let bool = true;
        for (const param in this.values) {
            if (bool) {
                let x = param.concat('=', this.values[param]);
                route = route.concat('?', x);
                bool = false;
            } else {
                let x = param.concat('=', this.values[param]);
                route = route.concat('&', x);
            }
        }
        return route;
    }
}
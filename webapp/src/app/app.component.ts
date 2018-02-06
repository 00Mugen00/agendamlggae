import {Component, OnInit} from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import {CategoriaService} from './services/categoria.service';
import {AbstractService} from "./services/abstract.service";

@Component({
    selector: 'my-app',
    templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

    userLoggedIn: boolean;
    private routerUrl: string;
    private textoBuscar: string = "";
    private urlInicioSesion = `${AbstractService.BASE_URL}/session`;
    private iframe = false;

    constructor(private categoriaService: CategoriaService, private router: Router) {
        let query = window.location.search.substr(1).split("&").map(e => e.split("=")).reduce((x, e) => {
            x[e[0]] = e[1];
            return x;
        }, {});
        if(query['token']) {
            window.localStorage.setItem('token', query['token']);
        }
        if(query['iwp']) {
            this.iframe = true;
        }
    }

    ngOnInit() {
        this.userLoggedIn = Boolean(window.localStorage.getItem('token'));
        this.router.events.subscribe(e => {
            if(e instanceof NavigationEnd) {
                this.routerUrl = (<NavigationEnd>e).urlAfterRedirects;
                if(this.routerUrl.startsWith("/nbuscar/")) {
                    this.textoBuscar = decodeURIComponent(this.routerUrl.substr(9));
                }
            }
        });
    }

    logout(event: Event) {
        event.preventDefault();
        window.localStorage.removeItem("token");
        window.location.assign(process.env.BASE_URL || "http://localhost:8080/");
    }

    buscar() {
        this.router.navigateByUrl(`/nbuscar/${encodeURIComponent(this.textoBuscar)}`);
    }
}

import { Component, Input } from '@angular/core';
import { Comentario } from "../../interfaces/comentario";

@Component({
    selector: 'comentario',
    templateUrl: './comentario.component.html',
    styleUrls: [ './comentario.component.scss' ]
})
export class ComentarioComponent {

    @Input() delete: Function;
    @Input() comentario: Comentario;

    leStyles() {
        return {
            'background-image': `url('${this.comentario.creador.image}')`
        };
    }

}
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AbstractService } from './abstract.service';
import { Comentario } from '../interfaces/comentario';
import { Evento } from "../interfaces/evento";

@Injectable()
export class ComentarioService extends AbstractService {
    constructor(http: HttpClient){
        super(http);
    }

    obtenerComentariosDeEvento(evento: Evento) {
        return this.get<Comentario[]>('comentario', evento.id);
    }

    comentar(evento: Evento, comentario: Comentario) {
        return this.put<Comentario[]>('comentario', evento.id, comentario);
    }

    quitarComentario(evento: Evento) {
        return this.delete<{deleted: boolean}>('comentario', evento.id);
    }
}
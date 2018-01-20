import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { CategoriaService } from '../../services/categoria.service';
import { EventoService } from '../../services/evento.service';
import { UsuarioService } from '../../services/usuario.service';
import { Evento, eventoVacio } from '../../interfaces/evento';
import { FotosDeEvento, fotosDeEventoVacio } from '../../interfaces/fotosDeEvento';
import { Foto } from '../../interfaces/foto';
import { Comentario } from "../../interfaces/comentario";
import { ComentarioService } from "../../services/comentario.service";

@Component({
  selector: 'app-verEvento',
  templateUrl: './verEvento.component.html',
  styleUrls: ['./verEvento.component.scss']
})
export class VerEventoComponent implements OnInit {

  errorResponse: HttpErrorResponse;
  id: string;
  evento: Evento;
  nombreCreador: string;
  fotosDeEvento: FotosDeEvento;
  fotos: Foto[];
  private comentarios: Comentario[];
  private validable: boolean = false;
  private editable: boolean = false;
  private borrable: boolean = false;

  constructor(private categoriaService: CategoriaService,
              private eventoService: EventoService,
              private usuarioService: UsuarioService,
              private comentarioService: ComentarioService,
              route: ActivatedRoute) {
                this.id = route.snapshot.params['id'];
                this.evento = eventoVacio();
                this.fotosDeEvento = fotosDeEventoVacio();
              }

  ngOnInit(){
    this.eventoService.buscarEvento(this.id).subscribe((resultado)=>{
      this.evento = resultado;
      this.usuarioService.obtenerUsuarioDeLaSesion().subscribe(usuario => {
        this.validable = !this.evento.validado && usuario.tipo == 3;
        this.editable = this.evento.creador === usuario.id || usuario.tipo == 3;
        this.borrable = usuario.tipo === 3;
      });
      this.usuarioService.buscarUsuario(this.evento.creador).subscribe((resultado2)=>{
          this.nombreCreador = resultado2.nombre;
      },(errorResponse) =>{
        this.errorResponse = errorResponse;
      });
      this.comentarioService.obtenerComentariosDeEvento(this.evento).subscribe(comentarios => {
        this.comentarios = comentarios;
      }, error => this.errorResponse = error);
    },(errorResponse) =>{
      this.errorResponse = errorResponse;
    });
    this.eventoService.buscarFotosParaEvento(this.id).subscribe((resultado3)=>{
      this.fotosDeEvento = resultado3;
      this.fotos = this.fotosDeEvento.fotos;
    },(errorResponse) =>{
      this.errorResponse = errorResponse;
    });
  }

  validar(){
    this.eventoService.validarEvento(this.id).subscribe((resultado)=>{
      console.log(resultado);
    },(errorResponse) =>{
      this.errorResponse = errorResponse;
    });
  }

  eliminar() {
    this.eventoService.borrarEvento(this.id).subscribe(
        null,
        error => this.errorResponse = error
    );
  }

  eliminarComentario(comentario: Comentario) {
    this.comentarioService.quitarComentario(this.evento).subscribe(() => {
      this.comentarios = this.comentarios.filter(c => c.creador.id !== comentario.creador.id);
    }, error => this.errorResponse = error);
  }

}

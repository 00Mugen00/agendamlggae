import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AbstractService } from './abstract.service';

@Injectable()
export class MeGustaService extends AbstractService{
  constructor(http: HttpClient){
    super(http);
    console.log('Conectado a MeGustaService');
  }

  crearMeGusta(id: string){
    return this.put<{me_gusta: boolean}>('megusta', id, {});
  }

  eliminarMeGusta(id: string) {
    return this.delete<{deleted: boolean}>('megusta', id);
  }
}

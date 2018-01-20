export interface Comentario {
    id: string,
    creador: {
        id: string,
        nombre: string,
        image: string
    },
    fecha: string,
    texto: string
}
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PokemonService {
  private baseUrl = 'https://pokeapi.co/api/v2/pokemon';

  constructor(private http: HttpClient) {}

  // Busca 'limit' pokemons (padrão 30), mapeando para {id, name, image, types[], stats[]}
  getPokemons(limit: number = 30): Observable<any[]> {
    const calls = [];
    for (let i = 1; i <= limit; i++) {
      calls.push(this.http.get(`${this.baseUrl}/${i}`));
    }

    return forkJoin(calls).pipe(
      map((items: any[]) =>
        items.map(p => ({
          id: p.id,
          name: p.name,
          image:
            p.sprites?.other?.['official-artwork']?.front_default ||
            p.sprites?.front_default ||
            '', // fallback
          types: p.types.map((t: any) => t.type.name),
          stats: p.stats.map((s: any) => ({ name: s.stat.name, value: s.base_stat }))
        }))
      )
    );
  }
}

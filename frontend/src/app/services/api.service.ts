import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8080';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getPokemons(limit: number = 151, offset: number = 0): Observable<any> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get(`${this.apiUrl}/pokemons?limit=${limit}&offset=${offset}`, { headers });
  }

  // NOVO MÉTODO: para buscar detalhes de um Pokémon pela URL que a primeira API retorna
  getPokemonDetailsByUrl(url: string): Observable<any> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    // Nós não usamos a apiUrl aqui porque a URL já vem completa da PokeAPI
    return this.http.get(url, { headers });
  }

  // NOVO MÉTODO: para buscar a lista de todos os tipos
  getAllTypes(): Observable<any> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get(`${this.apiUrl}/types`, { headers });
  }
}
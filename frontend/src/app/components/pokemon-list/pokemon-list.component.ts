import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { forkJoin, switchMap } from 'rxjs';

@Component({
  selector: 'app-pokemon-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pokemon-list.component.html',
  styleUrls: ['./pokemon-list.component.scss']
})
export class PokemonListComponent implements OnInit {
  allPokemons: any[] = [];
  filteredPokemons: any[] = [];
  types: string[] = ['Todos os Tipos', 'Normal', 'Fire', 'Water', 'Electric'];
  
  selectedType: string = 'Todos os Tipos';
  loading: boolean = true;
  errorMessage: string = '';

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getPokemons(100).pipe(
      switchMap((response: any[]) => {
        const detailRequests = response.map(p => this.apiService.getPokemonDetailsByUrl(p.url));
        return forkJoin(detailRequests);
      })
    ).subscribe({
      next: (detailedPokemons) => {
        this.allPokemons = detailedPokemons.map(p => this.transformPokemonData(p));
        this.filteredPokemons = this.allPokemons;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Não foi possível carregar os Pokémon. Verifique seu login.';
        this.loading = false;
        console.error(err);
      }
    });
  }

  transformPokemonData(p: any) {
    return {
      id: p.id,
      name: p.name,
      image: p.sprites.front_default,
      types: p.types.map((t: any) => t.type.name),
      stats: p.stats
    };
  }

  filterPokemons(type: string): void {
    this.selectedType = type;
    if (type === 'Todos os Tipos') {
      this.filteredPokemons = this.allPokemons;
    } else {
      this.filteredPokemons = this.allPokemons.filter(p => p.types.includes(type.toLowerCase()));
    }
  }
  
  formatId = (id: number) => `#${id.toString().padStart(3, '0')}`;
  
  statValue = (pokemon: any, statName: string) => {
    const stat = pokemon.stats.find((s: any) => s.stat.name === statName);
    return stat ? stat.base_stat : 0;
  };
}
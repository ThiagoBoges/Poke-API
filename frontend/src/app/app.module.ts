import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { PokemonListComponent } from './components/pokemon-list/pokemon-list.component';

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    AppComponent,              
    PokemonListComponent      
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}

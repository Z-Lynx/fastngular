import { NgModule } from '@angular/core';
import { HomeComponent } from './home/home.component';
import { CommonModule } from '@angular/common';
import { TopBarComponent } from '../top-bar/top-bar.component';
import { PageRoutingModule } from './page-routing.module';
import { FootballListComponent } from './home/football-list/football-list.component';
import { CarouselModule } from 'ngx-bootstrap/carousel';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ReactiveFormsModule } from '@angular/forms';
import { QuanlysanbongModule } from './quanly/quanly.module';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import { SideBarComponent } from '../side-bar/side-bar.component';
import { SlickCarouselModule } from 'ngx-slick-carousel';
import { FootballContentComponent } from './home/football-content/football-content.component';

@NgModule({
  declarations: [
    HomeComponent,
    TopBarComponent,
    FootballListComponent,
    LoginComponent,
    RegisterComponent,
    NavBarComponent,
    SideBarComponent,
    FootballContentComponent,
  ],
  // Import the ReactiveFormsModule
  imports: [
    CommonModule,
    PageRoutingModule,
    CarouselModule.forRoot(),
    ReactiveFormsModule,
    SlickCarouselModule
  ],
  exports: [
    HomeComponent,
    TopBarComponent,
    FootballListComponent,
    LoginComponent,
    RegisterComponent,
    NavBarComponent,
    SideBarComponent
  ],
})
export class PageModule {}

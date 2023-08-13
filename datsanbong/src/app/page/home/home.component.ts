import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FootballField } from './football-field.model';
import { FootballFieldService } from './football-field.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit {
  footballFields: FootballField[] = [];
  imageSlides = [
    { id: 1, imageUrl: 'assets/image/1.jpg' },
    { id: 2, imageUrl: 'assets/image/2.jpg' },
    { id: 3, imageUrl: 'assets/image/3.jpg' },
    { id: 4, imageUrl: 'assets/image/4.jpg' },
  ];

  slickConfig: any = {
    slidesToShow: 3,
    slidesToScroll: 1,
  };
  constructor(private footballFieldService: FootballFieldService) {}

  ngOnInit(): void {
    this.getFootballFields();

  }

  getFootballFields(): void {
    this.footballFieldService
      .getFootballFields()
      .subscribe((fields: FootballField[]) => {
        this.footballFields = fields;
      });
  }
}

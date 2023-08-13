import { Component, OnInit } from '@angular/core';
import { FootballField } from '../football-field.model';
import { FootballFieldService } from '../football-field.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-football-content',
  templateUrl: './football-content.component.html',
})
export class FootballContentComponent implements OnInit {
  football: FootballField | undefined;
  id_ft: number = 0;

  imageSlides: { id: number; imageUrl: string }[] = [];

  constructor(
    private footballFieldService: FootballFieldService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.id_ft = Number(params.get('footballId'));
      this.footballFieldService
        .getFootballFields()
        .subscribe((fields: FootballField[]) => {
          // This code should be moved inside the subscribe block
          const index = fields.findIndex((item) => item.id === this.id_ft);
          this.football = fields[index];

          this.imageSlides = this.football.danh_sach_hinh_anh
            .split(';')
            .map((imageUrl, index) => ({
              id: index + 1,
              imageUrl,
            }));
          console.log(this.imageSlides)
        });

      console.log(this.football);
    });
  }
}

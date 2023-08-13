import { Component, Input } from '@angular/core';
import { FootballField } from '../football-field.model';

@Component({
  selector: 'app-football-list',
  templateUrl: './football-list.component.html',
  styleUrls: ['football-list.component.scss'],
})
export class FootballListComponent {
  @Input() football: FootballField | undefined;
  image: string | undefined;

  ngOnInit(): void {
    if (this.football && this.football.danh_sach_hinh_anh) {
      this.image = this.football.danh_sach_hinh_anh.split(";")[0];
    } else {
      this.image = '';
    }
  }
}

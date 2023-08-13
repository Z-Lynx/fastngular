import { Component, OnInit } from '@angular/core';
import { DoanhNghiepField } from './doanhnghiep-field.model';
import { DoanhNghiepFieldService } from './doanhnghiep-field.service';

@Component({
  selector: 'app-doanhNghiep',
  templateUrl: './doanhnghiep.component.html',
})
export class DoanhNghiepComponent implements OnInit {
  doanhNghiepFields: DoanhNghiepField[] = [];

  constructor(private doanhNghiepFieldService: DoanhNghiepFieldService) {}

  ngOnInit(): void {
    this.getFootballFields();
  }

  getFootballFields(): void {
    this.doanhNghiepFieldService
      .getDoanhNghiepFields()
      .subscribe((fields: DoanhNghiepField[]) => {
        this.doanhNghiepFields = fields;
      });
  }
}

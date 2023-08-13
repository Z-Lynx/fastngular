import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { QuanlysanbongRoutingModule } from './quanly-routing.module';
import { QuanlyComponent } from './quanly.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { PageModule } from '../page.module';
import { QuanlysanbongComponent } from './quanlysanbong/quanlysanbong.component';
import { DoanhNghiepComponent } from './doanhnghiep/doanhnghiep.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    QuanlyComponent,
    DashboardComponent,
    QuanlysanbongComponent,
    DoanhNghiepComponent,
  ],
  imports: [PageModule, CommonModule, FormsModule, QuanlysanbongRoutingModule],
})
export class QuanlysanbongModule {}

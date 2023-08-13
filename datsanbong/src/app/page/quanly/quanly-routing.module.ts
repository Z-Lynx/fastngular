import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { QuanlyComponent } from './quanly.component';
import { QuanlysanbongComponent } from './quanlysanbong/quanlysanbong.component';
import { DoanhNghiepComponent } from './doanhnghiep/doanhnghiep.component';

const routes: Routes = [
  {
    path:'',
    pathMatch: 'full',
    redirectTo: 'sanbong',
  },
  
  {
    path:'',
    component:QuanlyComponent,
    children:[
      {
        path:'doanhnghiep',
        component:DoanhNghiepComponent
      },
      {
        path:'sanbong',
        component:QuanlysanbongComponent
      }
    ]
  },
  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuanlysanbongRoutingModule { }

import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
})
export class SideBarComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit(): void {
    this.setActiveLink(this.router.url.split('/')[2]);
  }
  selectedLink: string | null = null;

  setActiveLink(linkName: string) {
    this.selectedLink = linkName;
    console.log(linkName);
  }
}

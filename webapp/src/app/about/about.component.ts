import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { SearchBarServiceService } from '../search-bar-service.service';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {
  
  hasQuery$: Observable<Boolean>;
  
  constructor(private searchBarService: SearchBarServiceService) { }

  ngOnInit(): void {
    this.hasQuery$ = this.searchBarService.hasQuery;
  }

}

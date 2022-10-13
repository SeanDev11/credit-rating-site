import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { SearchBarServiceService } from '../search-bar-service.service';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss']
})
export class InfoComponent implements OnInit {

  hasQuery$: Observable<Boolean>;
  
  constructor(private searchBarService: SearchBarServiceService) { }


  ngOnInit(): void {
    this.hasQuery$ = this.searchBarService.hasQuery;
  }

}

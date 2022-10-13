import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { CombinedRatings } from '../ratings.service';
import { SearchBarServiceService } from '../search-bar-service.service';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent implements OnInit {

  currentCompany$: Observable<CombinedRatings>;
  hasQuery$: Observable<Boolean>;

  constructor(private searchBarService: SearchBarServiceService) { }

  ngOnInit(): void {
    this.currentCompany$ = this.searchBarService.currentCompany;
    this.hasQuery$ = this.searchBarService.hasQuery;
  }

}

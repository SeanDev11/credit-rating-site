import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { RatingsService, MY, CombinedRatings } from '../ratings.service';
import { SearchBarServiceService } from '../search-bar-service.service';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {

  //@Output() public currentCompanyMY = new EventEmitter<MY>();

  //@Output() public hasQueryOut = new EventEmitter<Boolean>();

  currentCompany$: Observable<CombinedRatings>;
  hasQuery$: Observable<Boolean>;

  myRatings:Array<CombinedRatings> = [];
  //hasQuery:Boolean = false;
  
  searchBoxText:string = "";

  constructor(private ratingsService: RatingsService, private searchBarService: SearchBarServiceService,
              private router: Router)
  { 
    //this.hasQueryOut.emit(this.hasQuery);
  }

  getSearchResults(event: any) {
    let query: string = event.target.value;
    
    let matchSpaces:any = query.match(/\s*/);
    if (matchSpaces[0] === query) {
      this.myRatings = [];
      //this.hasQuery = false;
      //this.hasQueryOut.emit(this.hasQuery);
      this.searchBarService.setHasQuery(false);
      return;
    }

    this.ratingsService.searchCompanies(query.trim()).subscribe(results => {
      this.myRatings = results;
      //this.hasQuery = true;
      //this.hasQueryOut.emit(this.hasQuery);
      this.searchBarService.setHasQuery(true)
      console.log(results);
    });
  }

  displayCompany(event: any, rating: CombinedRatings) {
    // Set search bar text
    this.searchBoxText = '';
    this.myRatings = [];
    //this.hasQuery = false;
    //this.hasQueryOut.emit(this.hasQuery);
    this.searchBarService.setHasQuery(false)
    console.log("Displaying...")
    this.searchBarService.setCurrentCompany(rating);
    //this.currentCompanyMY.emit(rating);
    console.log(rating);
    this.router.navigate(['']);
  }
  
  ngOnInit(): void {
    this.currentCompany$ = this.searchBarService.currentCompany;
    this.hasQuery$ = this.searchBarService.hasQuery;
  }
}

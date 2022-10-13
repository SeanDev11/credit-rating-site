import { Component, OnInit, Input } from '@angular/core';
import { CombinedRatings, SAP } from '../ratings.service';

@Component({
  selector: 'app-sandp-data',
  templateUrl: './sandp-data.component.html',
  styleUrls: ['./sandp-data.component.scss']
})
export class SandpDataComponent implements OnInit {

  @Input() public currentCompany: CombinedRatings = {
    ratingsMY: [],
    ratingsSAP: []
  };
  
  columnsToDisplay: string[] = ['rating', 'ratingType', 'outlook', 'ratingDate', 'outlookDate', 'lastReviewDate'];

  columnNames: {[key: string]: string} = {
    rating: 'Rating',
    ratingType: 'Type',
    outlook: 'Outlook',
    ratingDate: 'Rating Date',
    outlookDate: 'Outlook Date',
    lastReviewDate: 'Last Review Date'
  };

  dateColumns: Set<string> = new Set(['ratingDate', 'outlookDate', 'lastReviewDate']);

  constructor() { }

  ngOnInit(): void {
  }

}

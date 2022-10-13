import { Component, OnInit, Input } from '@angular/core';
import { MY, CombinedRatings } from '../ratings.service';
//import { DataSource } from '@angular/cdk/table';

@Component({
  selector: 'app-moody-data',
  templateUrl: './moody-data.component.html',
  styleUrls: ['./moody-data.component.scss']
})
export class MoodyDataComponent implements OnInit {

  @Input() public currentCompany: CombinedRatings = {
    ratingsMY: [],
    ratingsSAP: []
  };

  columnsToDisplay: string[] = ['rating', 'ratingType', 'action', 'date'];

  columnNames: {[key: string]: string} = {
    rating: 'Rating',
    ratingType: 'Type',
    action: 'Action',
    date: 'Date'
  };

  constructor() { }

  ngOnInit(): void {
  }

}
